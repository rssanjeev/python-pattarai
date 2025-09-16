#!/usr/bin/env python3

import os
import re
from datetime import datetime
from typing import List, Tuple

def extract_ddl_statements(file_path: str) -> List[Tuple[str, str, str]]:
    """
    Extract DDL statements from a SQL file
    
    Args:
        file_path: Path to the SQL file
        
    Returns:
        List of tuples (schema, object_name, ddl_statement)
    """
    ddl_statements = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match CREATE statements with schema.object_name
        create_pattern = re.compile(
            r'(CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)\s*\(.*?\));?',
            re.IGNORECASE | re.DOTALL
        )
        
        matches = create_pattern.findall(content)
        
        for match in matches:
            full_statement = match[0]  # Full CREATE statement
            full_object_name = match[1]  # Schema.object_name
            
            if '.' in full_object_name:
                schema_name, object_name = full_object_name.split('.', 1)
                schema_name = schema_name.strip().upper()
                object_name = object_name.strip().upper()
                
                # Clean up the statement - ensure it ends with semicolon
                clean_statement = full_statement.strip()
                if not clean_statement.endswith(';'):
                    clean_statement += ';'
                
                ddl_statements.append((schema_name, object_name, clean_statement))
                
    except Exception as e:
        print(f"❌ Error processing file {file_path}: {str(e)}")
        
    return ddl_statements

def consolidate_ddls(source_directory: str, output_file: str = 'consolidated_ddls.sql') -> None:
    """
    Consolidate all DDL statements from SQL files in a directory into a single file
    
    Args:
        source_directory: Directory containing SQL files
        output_file: Output file name for consolidated DDLs
    """
    if not os.path.exists(source_directory):
        print(f"❌ Source directory {source_directory} not found")
        return
    
    print(f"🔍 Scanning directory: {source_directory}")
    
    all_ddls = []
    processed_files = 0
    
    # Get all SQL files
    sql_files = [f for f in os.listdir(source_directory) if f.lower().endswith('.sql')]
    
    if not sql_files:
        print(f"❌ No SQL files found in {source_directory}")
        return
    
    print(f"📁 Found {len(sql_files)} SQL files")
    
    # Process each file
    for filename in sorted(sql_files):
        file_path = os.path.join(source_directory, filename)
        print(f"📄 Processing: {filename}")
        
        ddl_statements = extract_ddl_statements(file_path)
        
        if ddl_statements:
            all_ddls.extend(ddl_statements)
            print(f"   ✅ Extracted {len(ddl_statements)} DDL statement(s)")
            processed_files += 1
        else:
            print(f"   ⚠️  No DDL statements found")
    
    if not all_ddls:
        print("❌ No DDL statements found in any files")
        return
    
    print(f"\n📊 Summary:")
    print(f"   📁 Files processed: {processed_files}")
    print(f"   📄 Total DDL statements: {len(all_ddls)}")
    
    # Group by schema for better organization
    schema_groups = {}
    for schema, object_name, ddl in all_ddls:
        if schema not in schema_groups:
            schema_groups[schema] = []
        schema_groups[schema].append((object_name, ddl))
    
    print(f"   🏷️  Schemas found: {', '.join(sorted(schema_groups.keys()))}")
    
    # Write consolidated DDL file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("-- ============================================================\n")
            f.write("-- CONSOLIDATED DDL STATEMENTS\n")
            f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Source directory: {source_directory}\n")
            f.write(f"-- Total statements: {len(all_ddls)}\n")
            f.write(f"-- Schemas: {', '.join(sorted(schema_groups.keys()))}\n")
            f.write("-- ============================================================\n\n")
            
            # Write DDLs grouped by schema
            for schema in sorted(schema_groups.keys()):
                objects = schema_groups[schema]
                
                f.write(f"-- ============================================================\n")
                f.write(f"-- SCHEMA: {schema} ({len(objects)} objects)\n")
                f.write(f"-- ============================================================\n\n")
                
                for object_name, ddl in sorted(objects):
                    f.write(f"-- Object: {schema}.{object_name}\n")
                    f.write(f"-- --------------------------------------------------\n\n")
                    f.write(ddl)
                    f.write("\n\n")
                
                f.write(f"-- End of {schema} schema\n")
                f.write("-- ============================================================\n\n")
            
            # Write footer
            f.write("-- ============================================================\n")
            f.write("-- END OF CONSOLIDATED DDL STATEMENTS\n")
            f.write("-- ============================================================\n")
        
        print(f"\n✅ Consolidated DDL file created: {output_file}")
        
        # Show statistics by schema
        print(f"\n📊 Objects per schema:")
        for schema in sorted(schema_groups.keys()):
            count = len(schema_groups[schema])
            objects = [obj[0] for obj in schema_groups[schema]]
            print(f"   🏷️  {schema}: {count} objects")
            print(f"       📋 {', '.join(sorted(objects))}")
        
        file_size = os.path.getsize(output_file)
        print(f"\n📁 File size: {file_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Error writing consolidated file: {str(e)}")

def create_schema_specific_files(source_directory: str, output_directory: str = 'consolidated_by_schema') -> None:
    """
    Create separate consolidated files for each schema
    
    Args:
        source_directory: Directory containing SQL files
        output_directory: Directory to create schema-specific files
    """
    if not os.path.exists(source_directory):
        print(f"❌ Source directory {source_directory} not found")
        return
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"📁 Created output directory: {output_directory}")
    
    print(f"🔍 Scanning directory: {source_directory}")
    
    all_ddls = []
    sql_files = [f for f in os.listdir(source_directory) if f.lower().endswith('.sql')]
    
    # Process all files first
    for filename in sorted(sql_files):
        file_path = os.path.join(source_directory, filename)
        ddl_statements = extract_ddl_statements(file_path)
        all_ddls.extend(ddl_statements)
    
    if not all_ddls:
        print("❌ No DDL statements found")
        return
    
    # Group by schema
    schema_groups = {}
    for schema, object_name, ddl in all_ddls:
        if schema not in schema_groups:
            schema_groups[schema] = []
        schema_groups[schema].append((object_name, ddl))
    
    # Create file for each schema
    for schema in sorted(schema_groups.keys()):
        objects = schema_groups[schema]
        output_file = os.path.join(output_directory, f"{schema.lower()}_ddls.sql")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"-- ============================================================\n")
                f.write(f"-- DDL STATEMENTS FOR SCHEMA: {schema}\n")
                f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- Objects: {len(objects)}\n")
                f.write(f"-- ============================================================\n\n")
                
                f.write(f"-- Set schema context\n")
                f.write(f"USE SCHEMA {schema};\n\n")
                
                for object_name, ddl in sorted(objects):
                    f.write(f"-- Object: {object_name}\n")
                    f.write(f"-- --------------------------------------------------\n\n")
                    f.write(ddl)
                    f.write("\n\n")
                
                f.write(f"-- End of {schema} DDL statements\n")
            
            print(f"✅ Created {schema} DDL file: {output_file} ({len(objects)} objects)")
            
        except Exception as e:
            print(f"❌ Error creating {schema} file: {str(e)}")

if __name__ == "__main__":
    print("🔧 DDL Consolidation Tool")
    print("=" * 60)
    
    # Configuration
    storm_directory = r'C:\Users\Sanjeevs\OneDrive - Kraft Group LLC\Documents\storm'
    
    print(f"📁 Source directory: {storm_directory}")
    
    # Option 1: Create single consolidated file
    print(f"\n1️⃣ Creating single consolidated DDL file...")
    consolidate_ddls(storm_directory, 'consolidated_storm_ddls.sql')
    
    # Option 2: Create schema-specific files
    print(f"\n2️⃣ Creating schema-specific DDL files...")
    create_schema_specific_files(storm_directory, 'storm_ddls_by_schema')
    
    print(f"\n🎉 DDL consolidation completed!")
    print(f"📋 Output files:")
    print(f"   📄 consolidated_storm_ddls.sql - All DDLs in one file")
    print(f"   📁 storm_ddls_by_schema/ - Separate files per schema")
