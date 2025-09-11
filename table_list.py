import os
import re
from collections import defaultdict
import snowflake.connector
from typing import List, Dict
from datetime import datetime
from snowflake.connector.connection import SnowflakeConnection

def extract_tables_from_sql_files():
    directory = r"C:\Users\Sanjeevs\OneDrive - Kraft Group LLC\Documents\storm"
    tables_by_schema = defaultdict(list)
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} not found")
        return {}
    
    # Pattern to match CREATE TABLE and CREATE MATERIALIZED VIEW statements
    # Matches: CREATE [OR REPLACE] TABLE/MATERIALIZED VIEW schema.table_name
    table_pattern = re.compile(
        r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)',
        re.IGNORECASE
    )
    
    # Process all SQL files
    for filename in os.listdir(directory):
        if filename.lower().endswith('.sql'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Find all CREATE TABLE and CREATE MATERIALIZED VIEW statements
                    matches = table_pattern.findall(content)
                    
                    for match in matches:
                        if '.' in match:
                            schema, table = match.split('.', 1)
                            schema = schema.strip().upper()
                            table = table.strip().upper()
                            
                            if table not in tables_by_schema[schema]:
                                tables_by_schema[schema].append(table)
                                
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    # Sort schemas and tables for consistent output
    result = {}
    for schema in sorted(tables_by_schema.keys()):
        result[schema] = sorted(tables_by_schema[schema])
    
    return result

def get_snowflake_connection() -> SnowflakeConnection:
    """Create and return Snowflake connection using external browser authentication"""
    # Validate required environment variables
    account = 'KRAFTSPORTSGROUP'
    warehouse = 'KAGR_DEV_WAREHOUSE'
    database = 'EAGLESDEV_DBT'
    
    if not account:
        raise ValueError("DBT_SNOWFLAKE_ACCOUNT environment variable is not set")
    if not warehouse:
        raise ValueError("DBT_SNOWFLAKE_WAREHOUSE environment variable is not set")
    if not database:
        raise ValueError("DBT_SNOWFLAKE_DATABASE environment variable is not set")
    
    conn = snowflake.connector.connect(
        account=account,
        user='SanjeevS@kagr.com',
        warehouse=warehouse,
        database=database,
        authenticator='externalbrowser'
    )
    return conn

def extract_ddls_grouped_by_table(tables_dict: Dict[str, List[str]], output_dir: str = 'ddl_output') -> bool:
    """
    Extract DDL statements grouped by object name. Each object gets its own SQL file
    containing DDLs from all schemas where that object exists.
    Objects ending with '_HISTORY' are treated as tables, others as materialized views.
    
    Args:
        tables_dict: Dictionary with schema names as keys and list of object names as values
        output_dir: Directory to save DDL files
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = None
    cursor = None
    
    try:
        print(f"\n🔄 Extracting DDLs grouped by table name into '{output_dir}' directory...")
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Group tables by table name across all schemas
        tables_by_name = defaultdict(list)
        for schema_name, table_list in tables_dict.items():
            for table_name in table_list:
                tables_by_name[table_name].append(schema_name)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_unique_tables = len(tables_by_name)
        processed_count = 0
        success_count = 0
        
        print(f"Found {total_unique_tables} unique object names across {len(tables_dict)} schemas")
        
        for table_name, schema_list in tables_by_name.items():
            processed_count += 1
            print(f"\n📄 [{processed_count}/{total_unique_tables}] Processing object: {table_name}")
            print(f"   Found in schemas: {', '.join(schema_list)}")
            
            # Create file for this table (without timestamp)
            filename = f"{output_dir}/{table_name}.sql"
            table_success = False
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    # Write header
                    f.write(f"-- DDL Export for Object: {table_name}\n")
                    f.write(f"-- Generated on: {timestamp}\n")
                    f.write(f"-- Found in schemas: {', '.join(schema_list)}\n")
                    f.write("-- " + "="*60 + "\n\n")
                    
                    ddl_found = False
                    
                    for schema_name in schema_list:
                        print(f"   🔍 Extracting DDL from {schema_name}.{table_name}...")
                        
                        try:
                            # Determine object type based on naming convention
                            object_type = 'TABLE' if table_name.endswith('_HISTORY') else 'VIEW'
                            
                            # Verify object exists (check both tables and views)
                            if object_type == 'TABLE':
                                cursor.execute(f"SHOW TABLES LIKE '{table_name}' IN SCHEMA {schema_name}")
                            else:
                                cursor.execute(f"SHOW VIEWS LIKE '{table_name}' IN SCHEMA {schema_name}")
                                
                            if not cursor.fetchone():
                                print(f"   ⚠️  {object_type.title()} {schema_name}.{table_name} not found")
                                f.write(f"-- WARNING: {object_type.title()} {schema_name}.{table_name} not found\n\n")
                                continue
                            
                            # Get DDL for object (table or materialized view)
                            cursor.execute(f"SELECT GET_DDL('{object_type}', '{schema_name}.{table_name}')")
                            result = cursor.fetchone()
                            
                            if result and result[0]:
                                ddl = result[0]
                                
                                # Modify DDL to include schema name
                                if object_type == 'TABLE':
                                    # Replace "TABLE table_name" with "TABLE schema.table_name"
                                    ddl_with_schema = ddl.replace(
                                        f"TABLE {table_name}",
                                        f"TABLE {schema_name}.{table_name}"
                                    )
                                else:
                                    # Replace "VIEW table_name" with "VIEW schema.table_name"
                                    ddl_with_schema = ddl.replace(
                                        f"VIEW {table_name}",
                                        f"VIEW {schema_name}.{table_name}"
                                    )
                                
                                # Write schema section header
                                f.write(f"-- SCHEMA: {schema_name}\n")
                                f.write(f"-- {object_type.title()}: {schema_name}.{table_name}\n")
                                f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                f.write("-- " + "-"*50 + "\n\n")
                                
                                # Write DDL with schema
                                f.write(ddl_with_schema)
                                f.write("\n\n")
                                f.write("-- " + "."*50 + "\n\n")
                                
                                ddl_found = True
                                table_success = True
                                print(f"   ✅ DDL extracted from {schema_name}.{table_name} ({object_type})")
                            else:
                                print(f"   ⚠️  No DDL returned for {schema_name}.{table_name}")
                                f.write(f"-- WARNING: No DDL returned for {schema_name}.{table_name}\n\n")
                                
                        except Exception as e:
                            print(f"   ❌ Error processing {schema_name}.{table_name}: {str(e)}")
                            f.write(f"-- ERROR processing {schema_name}.{table_name}: {str(e)}\n\n")
                    
                    if not ddl_found:
                        f.write(f"-- ERROR: No DDL found for object {table_name} in any schema\n")
                        print(f"   ❌ No DDL found for {table_name} in any schema")
                    
                    f.write(f"-- End of DDL export for object: {table_name}\n")
                    f.write("-- " + "="*60 + "\n")
                
                if table_success:
                    success_count += 1
                    print(f"   ✅ File created: {filename}")
                else:
                    print(f"   ⚠️  File created but no DDLs extracted: {filename}")
                    
            except Exception as e:
                print(f"   ❌ Error creating file for {table_name}: {str(e)}")
        
        print(f"\n✅ DDL extraction completed!")
        print(f"   📁 Output directory: {output_dir}")
        print(f"   📊 Successfully processed: {success_count}/{total_unique_tables} tables")
        print(f"   📈 Success rate: {(success_count/total_unique_tables*100):.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during DDL extraction: {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def extract_all_ddls_to_single_file(tables_dict: Dict[str, List[str]], output_file: str = 'all_tables_ddl.sql') -> bool:
    """
    Extract DDL statements for all tables and write them to a single SQL file
    
    Args:
        tables_dict: Dictionary with schema names as keys and list of tables as values
        output_file: Name of the output SQL file
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = None
    cursor = None
    
    try:
        print(f"\n🔄 Extracting DDLs for all tables into '{output_file}'...")
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_tables = sum(len(tables) for tables in tables_dict.values())
        processed_count = 0
        success_count = 0
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"-- DDL Export for All Tables\n")
            f.write(f"-- Generated on: {timestamp}\n")
            f.write(f"-- Total schemas: {len(tables_dict)}\n")
            f.write(f"-- Total tables: {total_tables}\n")
            f.write("-- " + "="*60 + "\n\n")
            
            for schema_name, table_list in tables_dict.items():
                print(f"\n📂 Processing schema: {schema_name}")
                f.write(f"-- SCHEMA: {schema_name}\n")
                f.write("-- " + "-"*50 + "\n\n")
                
                for table_name in table_list:
                    processed_count += 1
                    try:
                        print(f"   [{processed_count}/{total_tables}] Extracting {schema_name}.{table_name}...")
                        
                        # Verify table exists
                        cursor.execute(f"SHOW TABLES LIKE '{table_name}' IN SCHEMA {schema_name}")
                        if not cursor.fetchone():
                            print(f"   ⚠️  Table {schema_name}.{table_name} not found")
                            f.write(f"-- WARNING: Table {schema_name}.{table_name} not found\n\n")
                            continue
                        
                        # Get DDL for table
                        cursor.execute(f"SELECT GET_DDL('TABLE', '{schema_name}.{table_name}')")
                        result = cursor.fetchone()
                        
                        if result and result[0]:
                            ddl = result[0]
                            
                            # Write table DDL with formatting
                            f.write(f"-- Table: {schema_name}.{table_name}\n")
                            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(ddl)
                            f.write("\n\n")
                            f.write("-- " + "."*50 + "\n\n")
                            
                            success_count += 1
                            print(f"   ✅ DDL extracted for {schema_name}.{table_name}")
                        else:
                            print(f"   ⚠️  No DDL returned for {schema_name}.{table_name}")
                            f.write(f"-- WARNING: No DDL returned for {schema_name}.{table_name}\n\n")
                            
                    except Exception as e:
                        print(f"   ❌ Error processing {schema_name}.{table_name}: {str(e)}")
                        f.write(f"-- ERROR processing {schema_name}.{table_name}: {str(e)}\n\n")
                
                f.write(f"-- End of schema: {schema_name}\n")
                f.write("-- " + "="*60 + "\n\n")
        
        print(f"\n✅ DDL extraction completed!")
        print(f"   📄 Output file: {output_file}")
        print(f"   📊 Successfully processed: {success_count}/{total_tables} tables")
        print(f"   📈 Success rate: {(success_count/total_tables*100):.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during DDL extraction: {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_table_ddls(tables_dict: Dict[str, List[str]], output_dir: str = 'ddl_output') -> None:
    """
    Get DDL statements for specified tables in schemas
    
    Args:
        tables_dict: Dictionary with schema names as keys and list of tables as values
                    Example: {'SCHEMA1': ['TABLE1', 'TABLE2'], 'SCHEMA2': ['TABLE3']}
        output_dir: Directory to save DDL files
    """
    conn = None
    cursor = None
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for schema, tables in tables_dict.items():
            print(f"\nProcessing schema: {schema}")
            
            for table in tables:
                try:
                    # Verify table exists
                    cursor.execute(f"SHOW TABLES LIKE '{table}' IN SCHEMA {schema}")
                    if not cursor.fetchone():
                        print(f"⚠️ Table {schema}.{table} not found")
                        continue
                    
                    # Get DDL for table
                    cursor.execute(f"SELECT GET_DDL('TABLE', '{schema}.{table}')")
                    result = cursor.fetchone()
                    if result:
                        ddl = result[0]
                        
                        # Write DDL to file
                        filename = f"{output_dir}/{schema}_{table}_{timestamp}.sql"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(ddl)
                        print(f"✓ DDL extracted for {schema}.{table}")
                    else:
                        print(f"⚠️ No DDL returned for {schema}.{table}")
                    
                except Exception as e:
                    print(f"❌ Error processing {schema}.{table}: {str(e)}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Execute the analysis
tables = extract_tables_from_sql_files()

# Display results
if tables:
    print("Tables by Schema:")
    for schema, table_list in tables.items():
        print(f"'{schema}': {table_list}")
    
    # Extract DDLs grouped by table name
    success = extract_ddls_grouped_by_table(tables, 'table_ddls')
    
    if success:
        print("\n🎉 All DDLs have been successfully extracted, grouped by table name in 'table_ddls' directory")
    else:
        print("\n❌ DDL extraction failed")
else:
    print("No tables found or directory doesn't exist")

if __name__ == "__main__":
    # Dictionary of schemas and their tables
    tables_to_extract = {
        'SCHEMA1': ['TABLE1', 'TABLE2'],
        'SCHEMA2': ['TABLE3']
    }
