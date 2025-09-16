import os
import re
import snowflake.connector
from typing import List, Optional
from datetime import datetime
from snowflake.connector.connection import SnowflakeConnection

def get_snowflake_connection() -> SnowflakeConnection:
    """Create and return Snowflake connection using external browser authentication"""
    account = 'KRAFTSPORTSGROUP'
    warehouse = 'KAGR_DEV_WAREHOUSE'
    database = 'EAGLESDEV_DBT'
    
    conn = snowflake.connector.connect(
        account=account,
        user='SanjeevS@kagr.com',
        warehouse=warehouse,
        database=database,
        authenticator='externalbrowser'
    )
    return conn

def parse_sql_file(file_path: str) -> List[str]:
    """
    Parse a SQL file and extract individual DDL statements
    
    Args:
        file_path: Path to the SQL file
        
    Returns:
        List of DDL statements
    """
    ddl_statements = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove comments and empty lines for parsing
        lines = content.split('\n')
        sql_lines = []
        
        for line in lines:
            # Skip comment lines and empty lines
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('--'):
                continue
            sql_lines.append(line)
        
        if sql_lines:
            # Join all non-comment lines and split by semicolon
            sql_content = '\n'.join(sql_lines)
            
            # Split by semicolon but be careful about semicolons in strings
            statements = []
            current_statement = ""
            in_string = False
            escape_next = False
            
            for char in sql_content:
                if escape_next:
                    current_statement += char
                    escape_next = False
                    continue
                    
                if char == '\\':
                    escape_next = True
                    current_statement += char
                    continue
                    
                if char == "'" and not escape_next:
                    in_string = not in_string
                    
                if char == ';' and not in_string:
                    statement = current_statement.strip()
                    if statement:
                        statements.append(statement)
                    current_statement = ""
                else:
                    current_statement += char
            
            # Add the last statement if it doesn't end with semicolon
            if current_statement.strip():
                statements.append(current_statement.strip())
                
            ddl_statements.extend(statements)
            
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {str(e)}")
        
    return ddl_statements

def execute_ddl_statement(cursor, statement: str, schema: Optional[str] = None) -> bool:
    """
    Execute a single DDL statement
    
    Args:
        cursor: Snowflake cursor
        statement: DDL statement to execute
        schema: Optional schema to set before execution
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Set schema if provided
        if schema:
            cursor.execute(f"USE SCHEMA {schema}")
            
        # Execute the DDL statement
        cursor.execute(statement)
        return True
        
    except Exception as e:
        print(f"❌ Error executing statement: {str(e)}")
        print(f"   Statement: {statement[:100]}...")
        return False

def execute_ddls_from_directory(ddl_directory: str = 'table_ddls', target_schemas: Optional[List[str]] = None, dry_run: bool = False) -> None:
    """
    Execute DDL statements from all SQL files in a directory
    
    Args:
        ddl_directory: Directory containing DDL files
        target_schemas: List of schemas to execute DDLs for (None = all schemas)
        dry_run: If True, only parse and show statements without executing
    """
    if not os.path.exists(ddl_directory):
        print(f"❌ Directory {ddl_directory} not found")
        return
        
    conn = None
    cursor = None
    
    try:
        if not dry_run:
            print("🔄 Connecting to Snowflake...")
            conn = get_snowflake_connection()
            cursor = conn.cursor()
            print("✅ Connected to Snowflake")
        else:
            print("🔍 DRY RUN MODE - No statements will be executed")
            
        sql_files = [f for f in os.listdir(ddl_directory) if f.endswith('.sql')]
        
        if not sql_files:
            print(f"❌ No SQL files found in {ddl_directory}")
            return
            
        print(f"\n📁 Found {len(sql_files)} SQL files")
        
        total_statements = 0
        successful_statements = 0
        failed_statements = 0
        
        for file_name in sorted(sql_files):
            file_path = os.path.join(ddl_directory, file_name)
            object_name = file_name.replace('.sql', '')
            
            print(f"\n📄 Processing file: {file_name}")
            
            # Parse DDL statements from file
            statements = parse_sql_file(file_path)
            
            if not statements:
                print(f"   ⚠️  No DDL statements found in {file_name}")
                continue
                
            print(f"   📊 Found {len(statements)} DDL statement(s)")
            
            for i, statement in enumerate(statements, 1):
                total_statements += 1
                
                # Extract schema from statement if possible
                schema_match = re.search(r'(?:TABLE|VIEW)\s+([A-Za-z_][A-Za-z0-9_]*)\.[A-Za-z_][A-Za-z0-9_]*', statement, re.IGNORECASE)
                current_schema = schema_match.group(1) if schema_match else None
                
                # Check if we should execute this statement based on target schemas
                if target_schemas and current_schema and current_schema.upper() not in [s.upper() for s in target_schemas]:
                    print(f"   ⏭️  Skipping statement {i} (schema {current_schema} not in target list)")
                    continue
                
                print(f"   🔄 Executing statement {i} for schema: {current_schema or 'Unknown'}")
                
                if dry_run:
                    print(f"   📝 Statement: {statement[:100]}...")
                    successful_statements += 1
                else:
                    success = execute_ddl_statement(cursor, statement, current_schema)
                    if success:
                        successful_statements += 1
                        print(f"   ✅ Statement {i} executed successfully")
                    else:
                        failed_statements += 1
                        
        print(f"\n🎯 Execution Summary:")
        print(f"   📊 Total statements: {total_statements}")
        print(f"   ✅ Successful: {successful_statements}")
        print(f"   ❌ Failed: {failed_statements}")
        
        if not dry_run and failed_statements == 0 and successful_statements > 0:
            print("🎉 All DDL statements executed successfully!")
        elif dry_run:
            print("🔍 Dry run completed - ready for execution")
            
    except Exception as e:
        print(f"❌ Error during DDL execution: {str(e)}")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_single_ddl_file(file_path: str, target_schemas: Optional[List[str]] = None, dry_run: bool = False) -> None:
    """
    Execute DDL statements from a single SQL file
    
    Args:
        file_path: Path to the SQL file
        target_schemas: List of schemas to execute DDLs for (None = all schemas)
        dry_run: If True, only parse and show statements without executing
    """
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} not found")
        return
        
    conn = None
    cursor = None
    
    try:
        if not dry_run:
            print("🔄 Connecting to Snowflake...")
            conn = get_snowflake_connection()
            cursor = conn.cursor()
            print("✅ Connected to Snowflake")
        else:
            print("🔍 DRY RUN MODE - No statements will be executed")
            
        print(f"\n📄 Processing file: {os.path.basename(file_path)}")
        
        # Parse DDL statements from file
        statements = parse_sql_file(file_path)
        
        if not statements:
            print(f"   ⚠️  No DDL statements found in file")
            return
            
        print(f"   📊 Found {len(statements)} DDL statement(s)")
        
        successful_statements = 0
        failed_statements = 0
        
        for i, statement in enumerate(statements, 1):
            # Extract schema from statement if possible
            schema_match = re.search(r'(?:TABLE|VIEW)\s+([A-Za-z_][A-Za-z0-9_]*)\.[A-Za-z_][A-Za-z0-9_]*', statement, re.IGNORECASE)
            current_schema = schema_match.group(1) if schema_match else None
            
            # Check if we should execute this statement based on target schemas
            if target_schemas and current_schema and current_schema.upper() not in [s.upper() for s in target_schemas]:
                print(f"   ⏭️  Skipping statement {i} (schema {current_schema} not in target list)")
                continue
            
            print(f"   🔄 Executing statement {i} for schema: {current_schema or 'Unknown'}")
            
            if dry_run:
                print(f"   📝 Statement: {statement[:100]}...")
                successful_statements += 1
            else:
                success = execute_ddl_statement(cursor, statement, current_schema)
                if success:
                    successful_statements += 1
                    print(f"   ✅ Statement {i} executed successfully")
                else:
                    failed_statements += 1
                    
        print(f"\n🎯 Execution Summary:")
        print(f"   📊 Total statements processed: {len(statements)}")
        print(f"   ✅ Successful: {successful_statements}")
        print(f"   ❌ Failed: {failed_statements}")
        
        if not dry_run and failed_statements == 0 and successful_statements > 0:
            print("🎉 All DDL statements executed successfully!")
        elif dry_run:
            print("🔍 Dry run completed - ready for execution")
            
    except Exception as e:
        print(f"❌ Error during DDL execution: {str(e)}")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Example usage - you can modify these parameters as needed
    
    print("🚀 Snowflake DDL Executor")
    print("=" * 50)
    
    # Option 1: Execute all DDL files from directory (dry run first)
    print("\n1️⃣ Dry run - Execute all DDL files from 'table_ddls' directory:")
    execute_ddls_from_directory(r"C:\Users\Sanjeevs\OneDrive - Kraft Group LLC\Documents\storm", dry_run=True)
    
    # Option 2: Execute DDLs for specific schemas only (uncomment to use)
    # print("\n2️⃣ Execute DDLs for KAGR schema only:")
    # execute_ddls_from_directory('table_ddls', target_schemas=['KAGR'], dry_run=False)
    
    # Option 3: Execute a single DDL file (uncomment to use)
    # print("\n3️⃣ Execute single DDL file:")
    # execute_single_ddl_file('table_ddls/DIM_CUSTOMER_HISTORY.sql', dry_run=False)
    
    # Uncomment the line below to actually execute all DDLs (after reviewing dry run)
    # print("\n🔥 ACTUAL EXECUTION - Execute all DDL files:")
    # execute_ddls_from_directory('table_ddls', dry_run=False)
