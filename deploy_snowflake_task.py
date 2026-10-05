import os
from engine.snowflake_session import get_snowflake_session

def deploy_pipeline_task():
    print("[Deploy] Connecting to Snowflake to deploy automated task...")
    session = get_snowflake_session()
    
    print("[Deploy] Registering Snowpark Stored Procedure for the Data Flow...")
    
    # Define the stored procedure logic that runs inside Snowflake natively
    def riskguard_automated_pipeline_sp(session):
        # This code runs natively inside Snowflake
        import time
        
        # 1. Extract flagged customers
        df = session.sql("SELECT CUSTOMER_ID FROM CUSTOMER LIMIT 1").to_pandas()
        target_customer = "C1007"
        if not df.empty:
            target_customer = df['CUSTOMER_ID'].iloc[0]
            
        # Normally, you would call Cortex Search and LLM functions directly via session.sql() here
        # For example: 
        # session.sql(f"SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-8b', 'Analyze {target_customer}')")
        
        return f"Successfully processed pipeline for {target_customer}"

    # Register the stored procedure
    # In a real environment, you'd specify packages=['snowflake-snowpark-python'] and stage_location
    try:
        session.sproc.register(
            func=riskguard_automated_pipeline_sp,
            name="RISKGUARD_AUTOMATED_PIPELINE",
            replace=True,
            is_permanent=False, # Set to True for production with a stage
            packages=['snowflake-snowpark-python', 'pandas']
        )
        print("[Deploy] Stored Procedure RISKGUARD_AUTOMATED_PIPELINE registered successfully.")
    except Exception as e:
        print(f"[Deploy] Note: Emulator mode might not support SP registration. Real Snowflake required. Error: {e}")

    # Create the Snowflake Task to run the procedure every 10 minutes
    print("[Deploy] Creating Snowflake Task to run every 10 minutes...")
    task_sql = """
    CREATE OR REPLACE TASK RISKGUARD_HOURLY_PIPELINE_TASK
      WAREHOUSE = COMPUTE_WH
      SCHEDULE = '10 MINUTE'
    AS
      CALL RISKGUARD_AUTOMATED_PIPELINE();
    """
    
    try:
        session.sql(task_sql).collect()
        
        # Tasks are created suspended by default, so we resume it
        session.sql("ALTER TASK RISKGUARD_HOURLY_PIPELINE_TASK RESUME").collect()
        
        print("[Deploy] ✅ Snowflake Task RISKGUARD_HOURLY_PIPELINE_TASK successfully created and started!")
        print("[Deploy] The pipeline is now running natively inside Snowflake Data Cloud.")
    except Exception as e:
        print(f"[Deploy] Note: Emulator mode might not support Task creation. Real Snowflake required. Error: {e}")


if __name__ == "__main__":
    deploy_pipeline_task()
