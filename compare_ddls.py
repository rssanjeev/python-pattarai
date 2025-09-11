import os
import re
from collections import defaultdict, namedtuple
from typing import Dict, List, Set, Optional, Tuple
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
    
    def get_column_set(self) -> Set[Column]:
        """Return set of columns for comparison"""
        return set(self.columns)
    
    def get_column_names(self) -> Set[str]:
        """Return set of column names (case-insensitive)"""
        return {col.name.upper() for col in self.columns}

def parse_ddl_columns(ddl_content: str) -> List[Column]:
    """
    Parse DDL content and extract column definitions
    
    Args:
        ddl_content: DDL statement content
        
    Returns:
        List of Column objects
    """
    columns = []
    
    # Find the CREATE statement and extract the column definitions
    create_match = re.search(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+.*?\s*\((.*?)\);?', 
                            ddl_content, re.IGNORECASE | re.DOTALL)
    
    if not create_match:
        return columns
    
    columns_section = create_match.group(1)
    
    # Split by comma, but be careful about commas inside parentheses (for data types like VARCHAR(100))
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
    
    # Parse each column definition
    for col_def in column_definitions:
        col_def = col_def.strip()
        if not col_def:
            continue
            
        # Skip constraints and other non-column definitions
        if any(keyword in col_def.upper() for keyword in ['CONSTRAINT', 'PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'INDEX', 'CHECK']):
            continue
        
        # Extract column name and data type
        # Pattern: COLUMN_NAME DATA_TYPE [NOT NULL] [DEFAULT value]
        col_match = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z0-9_()]+(?:\([^)]*\))?)\s*(.*)?', col_def)
        
        if col_match:
            col_name = col_match.group(1).strip()
            data_type = col_match.group(2).strip()
            modifiers = col_match.group(3).strip() if col_match.group(3) else ""
            
            # Check for NOT NULL
            nullable = "NOT NULL" not in modifiers.upper()
            
            # Extract default value
            default_match = re.search(r'DEFAULT\s+([^,\s]+(?:\([^)]*\))?)', modifiers, re.IGNORECASE)
            default_value = default_match.group(1) if default_match else None
            
            columns.append(Column(
                name=col_name,
                data_type=data_type,
                nullable=nullable,
                default_value=default_value
            ))
    
    return columns

def extract_schemas_from_ddl_files(ddl_directory: str) -> Dict[str, Dict[str, TableSchema]]:
    """
    Extract table schemas from DDL files
    
    Args:
        ddl_directory: Directory containing DDL files
        
    Returns:
        Dictionary: {table_name: {schema_name: TableSchema}}
    """
    table_schemas = defaultdict(dict)
    
    if not os.path.exists(ddl_directory):
        print(f"❌ Directory {ddl_directory} not found")
        return table_schemas
    
    for filename in os.listdir(ddl_directory):
        if not filename.endswith('.sql'):
            continue
            
        table_name = filename.replace('.sql', '')
        file_path = os.path.join(ddl_directory, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content by schema sections
            schema_sections = re.split(r'-- SCHEMA: ([A-Za-z_][A-Za-z0-9_]*)', content)
            
            for i in range(1, len(schema_sections), 2):
                schema_name = schema_sections[i].strip()
                schema_content = schema_sections[i + 1] if i + 1 < len(schema_sections) else ""
                
                # Extract DDL statement for this schema
                ddl_match = re.search(r'(CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+.*?);', 
                                    schema_content, re.IGNORECASE | re.DOTALL)
                
                if ddl_match:
                    ddl_statement = ddl_match.group(1)
                    columns = parse_ddl_columns(ddl_statement)
                    is_view = 'VIEW' in ddl_statement.upper() and 'MATERIALIZED' in ddl_statement.upper()
                    
                    table_schemas[table_name][schema_name] = TableSchema(
                        schema_name=schema_name,
                        table_name=table_name,
                        columns=columns,
                        is_view=is_view
                    )
                    
        except Exception as e:
            print(f"❌ Error processing file {filename}: {str(e)}")
    
    return table_schemas

def extract_schemas_from_sql_files(sql_directory: str) -> Dict[str, Dict[str, TableSchema]]:
    """
    Extract table schemas from original SQL files
    
    Args:
        sql_directory: Directory containing original SQL files
        
    Returns:
        Dictionary: {table_name: {schema_name: TableSchema}}
    """
    table_schemas = defaultdict(dict)
    
    if not os.path.exists(sql_directory):
        print(f"❌ Directory {sql_directory} not found")
        return table_schemas
    
    # Pattern to match CREATE statements
    create_pattern = re.compile(
        r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+VIEW|TABLE)\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\);?',
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
                full_table_name = match[0]
                columns_section = match[1]
                
                if '.' in full_table_name:
                    schema_name, table_name = full_table_name.split('.', 1)
                    schema_name = schema_name.strip().upper()
                    table_name = table_name.strip().upper()
                    
                    # Create full DDL statement for parsing
                    ddl_statement = f"CREATE TABLE {full_table_name} ({columns_section})"
                    columns = parse_ddl_columns(ddl_statement)
                    
                    # Determine if it's a view based on the original pattern
                    is_view = not table_name.endswith('_HISTORY')
                    
                    table_schemas[table_name][schema_name] = TableSchema(
                        schema_name=schema_name,
                        table_name=table_name,
                        columns=columns,
                        is_view=is_view
                    )
                    
        except Exception as e:
            print(f"❌ Error processing file {filename}: {str(e)}")
    
    return table_schemas

def compare_table_schemas(ddl_schemas: Dict[str, Dict[str, TableSchema]], 
                         sql_schemas: Dict[str, Dict[str, TableSchema]]) -> None:
    """
    Compare table schemas between DDL files and SQL files
    
    Args:
        ddl_schemas: Schemas from DDL files
        sql_schemas: Schemas from SQL files
    """
    print("🔍 Comparing Table Schemas")
    print("=" * 80)
    
    all_tables = set(ddl_schemas.keys()) | set(sql_schemas.keys())
    
    total_tables = len(all_tables)
    matching_tables = 0
    issues_found = 0
    
    for table_name in sorted(all_tables):
        print(f"\n📋 Table: {table_name}")
        print("-" * 60)
        
        ddl_table = ddl_schemas.get(table_name, {})
        sql_table = sql_schemas.get(table_name, {})
        
        if not ddl_table and not sql_table:
            continue
        elif not ddl_table:
            print(f"❌ Table {table_name} found in SQL files but not in DDL files")
            issues_found += 1
            continue
        elif not sql_table:
            print(f"❌ Table {table_name} found in DDL files but not in SQL files")
            issues_found += 1
            continue
        
        # Get all schemas for this table
        all_schemas = set(ddl_table.keys()) | set(sql_table.keys())
        table_has_issues = False
        
        for schema_name in sorted(all_schemas):
            ddl_schema = ddl_table.get(schema_name)
            sql_schema = sql_table.get(schema_name)
            
            print(f"\n  🏷️  Schema: {schema_name}")
            
            if not ddl_schema and not sql_schema:
                continue
            elif not ddl_schema:
                print(f"     ❌ Schema {schema_name} found in SQL files but not in DDL files")
                table_has_issues = True
                continue
            elif not sql_schema:
                print(f"     ❌ Schema {schema_name} found in DDL files but not in SQL files")
                table_has_issues = True
                continue
            
            # Compare column sets
            ddl_columns = ddl_schema.get_column_names()
            sql_columns = sql_schema.get_column_names()
            
            if ddl_columns == sql_columns:
                print(f"     ✅ Column sets match ({len(ddl_columns)} columns)")
            else:
                print(f"     ❌ Column sets differ:")
                table_has_issues = True
                
                # Show missing columns
                missing_in_ddl = sql_columns - ddl_columns
                missing_in_sql = ddl_columns - sql_columns
                
                if missing_in_ddl:
                    print(f"        Missing in DDL: {', '.join(sorted(missing_in_ddl))}")
                
                if missing_in_sql:
                    print(f"        Missing in SQL: {', '.join(sorted(missing_in_sql))}")
                
                # Show column counts
                print(f"        DDL columns: {len(ddl_columns)}, SQL columns: {len(sql_columns)}")
        
        if not table_has_issues:
            matching_tables += 1
            print(f"  🎉 All schemas match for {table_name}")
        else:
            issues_found += 1
    
    # Summary
    print(f"\n📊 Comparison Summary")
    print("=" * 80)
    print(f"Total tables compared: {total_tables}")
    print(f"Tables with matching schemas: {matching_tables}")
    print(f"Tables with issues: {issues_found}")
    
    if issues_found == 0:
        print("🎉 All table schemas match perfectly!")
    else:
        print(f"⚠️  {issues_found} table(s) have schema differences that need attention")

def compare_specific_table(table_name: str, 
                          ddl_schemas: Dict[str, Dict[str, TableSchema]], 
                          sql_schemas: Dict[str, Dict[str, TableSchema]]) -> None:
    """
    Compare schemas for a specific table in detail
    
    Args:
        table_name: Name of the table to compare
        ddl_schemas: Schemas from DDL files
        sql_schemas: Schemas from SQL files
    """
    print(f"🔍 Detailed Comparison for Table: {table_name}")
    print("=" * 80)
    
    ddl_table = ddl_schemas.get(table_name, {})
    sql_table = sql_schemas.get(table_name, {})
    
    if not ddl_table and not sql_table:
        print(f"❌ Table {table_name} not found in either DDL or SQL files")
        return
    
    # Get all schemas for this table
    all_schemas = set(ddl_table.keys()) | set(sql_table.keys())
    
    for schema_name in sorted(all_schemas):
        print(f"\n📋 Schema: {schema_name}")
        print("-" * 40)
        
        ddl_schema = ddl_table.get(schema_name)
        sql_schema = sql_table.get(schema_name)
        
        if ddl_schema and sql_schema:
            print("DDL Columns:")
            for col in ddl_schema.columns:
                print(f"  • {col}")
            
            print("\nSQL Columns:")
            for col in sql_schema.columns:
                print(f"  • {col}")
                
            # Compare
            ddl_cols = ddl_schema.get_column_names()
            sql_cols = sql_schema.get_column_names()
            
            if ddl_cols == sql_cols:
                print(f"\n✅ Schemas match ({len(ddl_cols)} columns)")
            else:
                print(f"\n❌ Schemas differ:")
                missing_in_ddl = sql_cols - ddl_cols
                missing_in_sql = ddl_cols - sql_cols
                
                if missing_in_ddl:
                    print(f"  Missing in DDL: {', '.join(sorted(missing_in_ddl))}")
                if missing_in_sql:
                    print(f"  Missing in SQL: {', '.join(sorted(missing_in_sql))}")
        
        elif ddl_schema:
            print("❌ Found in DDL files only")
        elif sql_schema:
            print("❌ Found in SQL files only")

if __name__ == "__main__":
    print("🔍 DDL Schema Comparison Tool")
    print("=" * 80)
    
    # Directories
    ddl_directory = 'table_ddls'
    sql_directory = r'C:\Users\Sanjeevs\OneDrive - Kraft Group LLC\Documents\storm'
    
    print(f"📁 DDL Directory: {ddl_directory}")
    print(f"📁 SQL Directory: {sql_directory}")
    
    # Extract schemas from both sources
    print("\n🔄 Extracting schemas from DDL files...")
    ddl_schemas = extract_schemas_from_ddl_files(ddl_directory)
    print(f"✅ Found {len(ddl_schemas)} tables in DDL files")
    
    print("\n🔄 Extracting schemas from SQL files...")
    sql_schemas = extract_schemas_from_sql_files(sql_directory)
    print(f"✅ Found {len(sql_schemas)} tables in SQL files")
    
    # Compare all schemas
    compare_table_schemas(ddl_schemas, sql_schemas)
    
    # Example: Compare a specific table in detail (uncomment to use)
    # print("\n" + "="*80)
    # compare_specific_table("DIM_CUSTOMER_HISTORY", ddl_schemas, sql_schemas)
