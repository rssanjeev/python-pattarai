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
    
    # Pattern to match CREATE TABLE statements
    # Matches: CREATE [OR REPLACE] TABLE schema.table_name
    table_pattern = re.compile(
        r'CREATE\s+(?:OR\s+REPLACE\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)',
        re.IGNORECASE
    )
    
    # Process all SQL files
    for filename in os.listdir(directory):
        if filename.lower().endswith('.sql'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Find all CREATE TABLE statements
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
    conn = snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        authenticator='externalbrowser'
    )
    return conn

def get_table_ddls(tables_dict: Dict[str, List[str]], output_dir: str = 'ddl_output') -> None:
    """
    Get DDL statements for specified tables in schemas
    
    Args:
        tables_dict: Dictionary with schema names as keys and list of tables as values
                    Example: {'SCHEMA1': ['TABLE1', 'TABLE2'], 'SCHEMA2': ['TABLE3']}
        output_dir: Directory to save DDL files
    """
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
                    ddl = cursor.fetchone()[0]
                    
                    # Write DDL to file
                    filename = f"{output_dir}/{schema}_{table}_{timestamp}.sql"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(ddl)
                    print(f"✓ DDL extracted for {schema}.{table}")
                    
                except Exception as e:
                    print(f"❌ Error processing {schema}.{table}: {str(e)}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Execute the analysis
tables = extract_tables_from_sql_files()

# Display results
if tables:
    print("Tables by Schema:")
    for schema, table_list in tables.items():
        print(f"'{schema}': {table_list}")
else:
    print("No tables found or directory doesn't exist")

if __name__ == "__main__":
    # Dictionary of schemas and their tables
    tables_to_extract = {
        'SCHEMA1': ['TABLE1', 'TABLE2'],
        'SCHEMA2': ['TABLE3']
    }
