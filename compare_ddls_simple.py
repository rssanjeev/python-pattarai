import os
import re
from collections import defaultdict
from typing import Dict, List, Set, Optional
from dataclasses import dataclass

@dataclass
class Column:
    """Represents a table column with its properties"""
    name: str
    data_type: str
    nullable: bool = True
    default_value: Optional[str] = None
    
    def __eq__(self, other):
        if not isinstance(other, Column):
            return False
        return (self.name.upper() == other.name.upper() and 
                self.data_type.upper() == other.data_type.upper())
    
    def __hash__(self):
        return hash((self.name.upper(), self.data_type.upper()))
    
    def __str__(self):
        return f"{self.name} {self.data_type}"

@dataclass
class TableSchema:
    """Represents a table schema with its columns"""
    schema_name: str
    table_name: str
    columns: List[Column]
    is_view: bool = False
    
    def get_column_names(self) -> Set[str]:
        """Return set of column names (case-insensitive)"""
        return {col.name.upper() for col in self.columns}

def parse_ddl_columns(ddl_content: str, table_name: str = "", debug: bool = True) -> List[Column]:
    """
    Parse DDL content and extract column definitions with detailed debugging
    """
    columns = []
    
    if debug:
        print(f"\n🔍 DEBUG: Parsing {table_name}")
        print(f"DDL content (first 300 chars):\n{ddl_content[:300]}...")
        print("-" * 50)
    
    # Find the CREATE statement and extract the column definitions
    create_match = re.search(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+[^\(]+\s*\((.*?)\)\s*;?', 
                            ddl_content, re.IGNORECASE | re.DOTALL)
    
    if not create_match:
        # Try alternative pattern
        create_match = re.search(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+[^\(]+\s*\((.*)', 
                                ddl_content, re.IGNORECASE | re.DOTALL)
    
    if not create_match:
        if debug:
            print("❌ No CREATE statement match found")
        return columns
    
    columns_section = create_match.group(1)
    if debug:
        print(f"✅ Found CREATE statement")
        print(f"Columns section (first 300 chars):\n{columns_section[:300]}...")
        print("-" * 50)
    
    # Handle closing parenthesis
    paren_count = 0
    last_valid_pos = len(columns_section)
    
    for i, char in enumerate(columns_section):
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
            if paren_count < 0:
                last_valid_pos = i
                break
    
    columns_section = columns_section[:last_valid_pos]
    
    if debug:
        print(f"After parenthesis cleanup (first 300 chars):\n{columns_section[:300]}...")
        print("-" * 50)
    
    # Split by comma, handling nested parentheses
    column_definitions = []
    current_def = ""
    paren_count = 0
    
    for char in columns_section:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        elif char == ',' and paren_count == 0:
            if current_def.strip():
                column_definitions.append(current_def.strip())
            current_def = ""
            continue
        current_def += char
    
    # Add the last column definition
    if current_def.strip():
        column_definitions.append(current_def.strip())
    
    if debug:
        print(f"Found {len(column_definitions)} column definitions:")
        for i, col_def in enumerate(column_definitions):
            print(f"  {i+1}: {col_def[:100]}{'...' if len(col_def) > 100 else ''}")
        print("-" * 50)
    
    # Parse each column definition
    parsed_count = 0
    for col_def in column_definitions:
        col_def = col_def.strip()
        if not col_def:
            continue
            
        # Skip constraints and comments
        if any(keyword in col_def.upper() for keyword in ['CONSTRAINT', 'PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'INDEX', 'CHECK']) or col_def.startswith('--'):
            if debug:
                print(f"Skipping constraint/comment: {col_def[:50]}...")
            continue
        
        # Check if this is a materialized view (columns without data types) or table (columns with data types)
        if "MATERIALIZED VIEW" in ddl_content.upper():
            # For materialized views, just extract column name
            col_match = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*$', col_def)
            if col_match:
                col_name = col_match.group(1).strip()
                columns.append(Column(
                    name=col_name,
                    data_type="UNKNOWN",  # Materialized views don't specify data types in definition
                    nullable=True,
                    default_value=None
                ))
                parsed_count += 1
                if debug:
                    print(f"✅ Parsed MV column {parsed_count}: {col_name}")
            else:
                if debug:
                    print(f"❌ Failed to parse MV column: {col_def[:50]}...")
        else:
            # For tables, extract column name and data type
            col_match = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z0-9_()]+(?:\([^)]*\))?)\s*(.*)?', col_def)
            
            if col_match:
                col_name = col_match.group(1).strip()
                data_type = col_match.group(2).strip()
                modifiers = col_match.group(3).strip() if col_match.group(3) else ""
                
                nullable = "NOT NULL" not in modifiers.upper()
                default_match = re.search(r'DEFAULT\s+([^,\s]+(?:\([^)]*\))?)', modifiers, re.IGNORECASE)
                default_value = default_match.group(1) if default_match else None
                
                columns.append(Column(
                    name=col_name,
                    data_type=data_type,
                    nullable=nullable,
                    default_value=default_value
                ))
                
                parsed_count += 1
                if debug:
                    print(f"✅ Parsed table column {parsed_count}: {col_name} {data_type}")
            else:
                if debug:
                    print(f"❌ Failed to parse table column: {col_def[:50]}...")
    
    if debug:
        print(f"\n🎯 Final result: {len(columns)} columns parsed successfully")
        print("=" * 60)
    
    return columns

def extract_schemas_from_ddl_files(ddl_directory: str, target_tables: List[str]) -> Dict[str, Dict[str, TableSchema]]:
    """Extract schemas for specific tables from DDL files"""
    table_schemas = defaultdict(dict)
    
    print(f"\n📁 Scanning DDL directory: {ddl_directory}")
    
    for table_name in target_tables:
        filename = f"{table_name}.sql"
        file_path = os.path.join(ddl_directory, filename)
        
        if not os.path.exists(file_path):
            print(f"⚠️  DDL file not found: {filename}")
            continue
            
        print(f"\n📄 Processing DDL file: {filename}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content by schema sections
            schema_sections = re.split(r'-- SCHEMA: ([A-Za-z_][A-Za-z0-9_]*)', content)
            
            for i in range(1, len(schema_sections), 2):
                schema_name = schema_sections[i].strip()
                schema_content = schema_sections[i + 1] if i + 1 < len(schema_sections) else ""
                
                print(f"  🏷️  Processing schema: {schema_name}")
                
                # Extract DDL statement for this schema
                ddl_match = re.search(r'(CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+.*?)(?=-- SCHEMA:|-- End of DDL|$)', 
                                    schema_content, re.IGNORECASE | re.DOTALL)
                
                if ddl_match:
                    ddl_statement = ddl_match.group(1).strip()
                    columns = parse_ddl_columns(ddl_statement, f"{schema_name}.{table_name}")
                    is_view = 'VIEW' in ddl_statement.upper() and 'MATERIALIZED' in ddl_statement.upper()
                    
                    table_schemas[table_name][schema_name] = TableSchema(
                        schema_name=schema_name,
                        table_name=table_name,
                        columns=columns,
                        is_view=is_view
                    )
                    
                    print(f"     ✅ Found {len(columns)} columns in {schema_name}.{table_name}")
                else:
                    print(f"     ❌ No DDL statement found for {schema_name}.{table_name}")
                    
        except Exception as e:
            print(f"❌ Error processing file {filename}: {str(e)}")
    
    return table_schemas

def extract_schemas_from_sql_files(sql_directory: str, target_tables: List[str]) -> Dict[str, Dict[str, TableSchema]]:
    """Extract schemas for specific tables from SQL files"""
    table_schemas = defaultdict(dict)
    
    print(f"\n📁 Scanning SQL directory: {sql_directory}")
    
    # Pattern to match CREATE statements
    create_pattern = re.compile(
        r'(CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\));?',
        re.IGNORECASE | re.DOTALL
    )
    
    for filename in os.listdir(sql_directory):
        if not filename.lower().endswith('.sql'):
            continue
            
        file_path = os.path.join(sql_directory, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all CREATE statements
            matches = create_pattern.findall(content)
            
            for match in matches:
                create_statement = match[0]  # Full CREATE statement
                full_table_name = match[1]   # Schema.table_name
                columns_section = match[2]   # Column definitions
                
                if '.' in full_table_name:
                    schema_name, table_name = full_table_name.split('.', 1)
                    schema_name = schema_name.strip().upper()
                    table_name = table_name.strip().upper()
                    
                    # Only process target tables
                    if table_name not in target_tables:
                        continue
                    
                    print(f"📄 Found {table_name} in {filename}")
                    print(f"  🏷️  Schema: {schema_name}")
                    
                    # Use the original CREATE statement for parsing (preserves MATERIALIZED VIEW vs TABLE)
                    ddl_statement = f"{create_statement}({columns_section})"
                    columns = parse_ddl_columns(ddl_statement, f"{schema_name}.{table_name}")
                    
                    # Determine if it's a view based on the original CREATE statement
                    is_view = 'MATERIALIZED VIEW' in create_statement.upper()
                    
                    table_schemas[table_name][schema_name] = TableSchema(
                        schema_name=schema_name,
                        table_name=table_name,
                        columns=columns,
                        is_view=is_view
                    )
                    
                    print(f"     ✅ Found {len(columns)} columns in {schema_name}.{table_name}")
                    
        except Exception as e:
            print(f"❌ Error processing file {filename}: {str(e)}")
    
    return table_schemas

def compare_specific_tables(ddl_schemas: Dict[str, Dict[str, TableSchema]], 
                           sql_schemas: Dict[str, Dict[str, TableSchema]],
                           target_tables: List[str]) -> None:
    """Compare schemas for specific tables with detailed highlighting"""
    print(f"\n🔍 Comparing Schemas for Target Tables")
    print("=" * 80)
    
    # Track summary statistics
    total_tables = len(target_tables)
    tables_with_issues = 0
    total_differences = 0
    summary_differences = []
    
    for table_name in target_tables:
        print(f"\n📋 Table: {table_name}")
        print("-" * 60)
        
        ddl_table = ddl_schemas.get(table_name, {})
        sql_table = sql_schemas.get(table_name, {})
        
        if not ddl_table and not sql_table:
            print(f"❌ Table {table_name} not found in either source")
            tables_with_issues += 1
            summary_differences.append(f"{table_name}: Not found in either source")
            continue
        elif not ddl_table:
            print(f"❌ Table {table_name} found in SQL files but not in DDL files")
            tables_with_issues += 1
            summary_differences.append(f"{table_name}: Only in STORM files")
            continue
        elif not sql_table:
            print(f"❌ Table {table_name} found in DDL files but not in SQL files")
            tables_with_issues += 1
            summary_differences.append(f"{table_name}: Only in DDL files")
            continue
        
        # Get all schemas for this table
        all_schemas = set(ddl_table.keys()) | set(sql_table.keys())
        table_has_issues = False
        table_differences = []
        
        for schema_name in sorted(all_schemas):
            ddl_schema = ddl_table.get(schema_name)
            sql_schema = sql_table.get(schema_name)
            
            print(f"\n  🏷️  Schema: {schema_name}")
            
            if ddl_schema and sql_schema:
                ddl_columns = ddl_schema.get_column_names()
                sql_columns = sql_schema.get_column_names()
                
                print(f"     📊 DDL (table_ddls) columns ({len(ddl_columns)}): {', '.join(sorted(ddl_columns))}")
                print(f"     📁 STORM columns ({len(sql_columns)}): {', '.join(sorted(sql_columns))}")
                
                if ddl_columns == sql_columns:
                    print(f"     ✅ Column sets match ({len(ddl_columns)} columns)")
                else:
                    print(f"     ❌ Column sets differ:")
                    table_has_issues = True
                    
                    missing_in_ddl = sql_columns - ddl_columns
                    missing_in_sql = ddl_columns - sql_columns
                    
                    if missing_in_ddl:
                        print(f"        🆕 Missing in DDL (present in STORM): {', '.join(sorted(missing_in_ddl))}")
                        table_differences.append(f"{schema_name}: +{', '.join(sorted(missing_in_ddl))}")
                        total_differences += len(missing_in_ddl)
                    
                    if missing_in_sql:
                        print(f"        ➖ Missing in STORM (present in DDL): {', '.join(sorted(missing_in_sql))}")
                        table_differences.append(f"{schema_name}: -{', '.join(sorted(missing_in_sql))}")
                        total_differences += len(missing_in_sql)
                    
                    # Show detailed column-by-column comparison
                    print(f"\n     📊 Detailed Column Comparison:")
                    print(f"     {'Column Name':<20} {'DDL':<8} {'STORM':<8} {'Status'}")
                    print(f"     {'-'*20} {'-'*8} {'-'*8} {'-'*15}")
                    
                    all_column_names = sorted(ddl_columns | sql_columns)
                    for col_name in all_column_names:
                        in_ddl = "✅" if col_name in ddl_columns else "❌"
                        in_storm = "✅" if col_name in sql_columns else "❌"
                        
                        if col_name in missing_in_ddl:
                            status = "🆕 NEW in STORM"
                        elif col_name in missing_in_sql:
                            status = "🗑️ REMOVED"
                        else:
                            status = "✅ MATCH"
                        
                        print(f"     {col_name:<20} {in_ddl:<8} {in_storm:<8} {status}")
            
            elif ddl_schema:
                print(f"     ❌ Found in DDL files only ({len(ddl_schema.columns)} columns)")
                table_has_issues = True
                table_differences.append(f"{schema_name}: Only in DDL")
            elif sql_schema:
                print(f"     ❌ Found in SQL files only ({len(sql_schema.columns)} columns)")
                table_has_issues = True
                table_differences.append(f"{schema_name}: Only in STORM")
        
        if not table_has_issues:
            print(f"  🎉 All schemas match for {table_name}")
        else:
            print(f"\n  📝 Summary for {table_name}: Differences found - see details above")
            tables_with_issues += 1
            summary_differences.append(f"{table_name}: {'; '.join(table_differences)}")
    
    # Print overall summary
    print(f"\n\n📊 OVERALL SUMMARY")
    print("=" * 80)
    print(f"📋 Total tables analyzed: {total_tables}")
    print(f"✅ Tables matching: {total_tables - tables_with_issues}")
    print(f"❌ Tables with differences: {tables_with_issues}")
    print(f"🔢 Total column differences: {total_differences}")
    
    if summary_differences:
        print(f"\n📝 Summary of all differences:")
        for diff in summary_differences:
            print(f"  • {diff}")
    else:
        print(f"\n🎉 All tables match perfectly!")

if __name__ == "__main__":
    print("🔍 DDL Schema Comparison Tool - ALL TABLES")
    print("=" * 80)
    
    # Directories
    ddl_directory = 'table_ddls'
    sql_directory = r'C:\Users\Sanjeevs\OneDrive - Kraft Group LLC\Documents\storm'
    
    # Auto-discover target tables from DDL directory
    target_tables = []
    if os.path.exists(ddl_directory):
        for filename in os.listdir(ddl_directory):
            if filename.lower().endswith('.sql'):
                table_name = filename[:-4].upper()  # Remove .sql extension
                target_tables.append(table_name)
    
    target_tables.sort()  # Sort for consistent output
    
    print(f"🎯 Target tables ({len(target_tables)}): {', '.join(target_tables)}")
    print(f"📁 DDL Directory: {ddl_directory}")
    print(f"📁 SQL Directory: {sql_directory}")
    
    if not target_tables:
        print("❌ No DDL files found in the table_ddls directory!")
        exit(1)
    
    # Extract schemas from both sources
    ddl_schemas = extract_schemas_from_ddl_files(ddl_directory, target_tables)
    sql_schemas = extract_schemas_from_sql_files(sql_directory, target_tables)
    
    # Compare the specific tables
    compare_specific_tables(ddl_schemas, sql_schemas, target_tables)
