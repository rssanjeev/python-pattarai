#!/usr/bin/env python3

import os
import re
from storm_ddls_by_schema.compare_ddls_all import parse_ddl_columns

def test_ddl_parsing():
    # Read the DIM_DATE_HISTORY.sql file
    file_path = 'table_ddls/DIM_DATE_HISTORY.sql'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Testing DDL parsing for DIM_DATE_HISTORY...")
    print("=" * 60)
    
    # Split content by schema sections
    schema_sections = re.split(r'-- SCHEMA: ([A-Za-z_][A-Za-z0-9_]*)', content)
    
    for i in range(1, len(schema_sections), 2):
        schema_name = schema_sections[i].strip()
        schema_content = schema_sections[i + 1] if i + 1 < len(schema_sections) else ""
        
        print(f"\n🏷️ Schema: {schema_name}")
        
        # Extract DDL statement for this schema
        ddl_match = re.search(r'(CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+.*?)(?=-- SCHEMA:|-- End of DDL|$)', 
                            schema_content, re.IGNORECASE | re.DOTALL)
        
        if ddl_match:
            ddl_statement = ddl_match.group(1).strip()
            print(f"DDL Statement found (first 200 chars):")
            print(ddl_statement[:200] + "...")
            
            # Parse with debug enabled
            columns = parse_ddl_columns(ddl_statement, f"{schema_name}.DIM_DATE_HISTORY", debug=True)
            
            print(f"\nExtracted columns ({len(columns)}):")
            for i, col in enumerate(columns, 1):
                print(f"  {i:2d}. {col.name} - {col.data_type}")
            
            # Check specifically for DATEKEY
            datekey_found = any(col.name.upper() == 'DATEKEY' for col in columns)
            print(f"\nDATEKEY found: {'✅ YES' if datekey_found else '❌ NO'}")
        else:
            print("❌ No DDL statement found")

if __name__ == "__main__":
    test_ddl_parsing()
