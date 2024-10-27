from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from pathlib import Path

# Type mapping from schema to Python types
TYPE_MAPPING = {
    'text': str,
    'number': float,
    'bool': bool,
    'json': Dict[str, Any],
    'date': datetime,
    'file': List[str],  # Assuming file fields store paths/urls as strings
    'relation': str,    # Relations will store the ID as string
}

def convert_type(field_type: str) -> str:
    """Convert schema type to Python type annotation string."""
    python_type = TYPE_MAPPING.get(field_type, Any)
    return f"Optional[{python_type.__name__}]"

def sanitize_field_name(name: str) -> str:
    """Ensure field name is a valid Python identifier."""
    if name.isidentifier():
        return name
    # Replace invalid characters with underscore
    return ''.join(c if c.isalnum() else '_' for c in name)

def generate_dataclass_code(schema: Dict[str, Any], ignored_tables: set = None) -> str:
    """Generate Python dataclass code from schema definition."""
    if ignored_tables is None:
        ignored_tables = set()
    
    output = [
        "from dataclasses import dataclass, field",
        "from typing import Optional, List, Dict, Any",
        "from datetime import datetime",
        "\n"
    ]
    
    for collection in schema:
        if collection['name'] in ignored_tables:
            continue
            
        class_name = ''.join(word.capitalize() for word in collection['name'].split('_'))
        class_fields = []
        
        # Add ID field
        class_fields.append("    id: Optional[str] = None")
        
        # Process schema fields
        for field_def in collection['schema']:
            field_name = sanitize_field_name(field_def['name'])
            field_type = convert_type(field_def['type'])
            
            # Add field with type annotation
            class_fields.append(f"    {field_name}: {field_type} = None")
        
        # Generate the dataclass
        dataclass_code = [
            f"@dataclass",
            f"class {class_name}:",
            f"    \"\"\"Generated from collection: {collection['name']}\"\"\"",
            *class_fields,
            "\n"
        ]
        
        output.extend(dataclass_code)
    
    return '\n'.join(output)

def main(schema_path: str, output_path: str = None, ignored_tables: set = None):
    """
    Generate Python dataclasses from a PocketBase schema JSON file.
    
    Args:
        schema_path: Path to the schema JSON file
        output_path: Optional path to write the generated code
        ignored_tables: Set of table names to ignore
    """
    # Read schema
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Generate code
    generated_code = generate_dataclass_code(schema, ignored_tables)
    
    # Output handling
    if output_path:
        with open(output_path, 'w') as f:
            f.write(generated_code)
        print(f"Generated dataclasses written to {output_path}")
    else:
        print(generated_code)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert PocketBase schema to Python dataclasses")
    parser.add_argument("schema_file", help="Path to the schema JSON file")
    parser.add_argument("-o", "--output", help="Output Python file path")
    parser.add_argument("-i", "--ignore", nargs="+", help="Tables to ignore")
    
    args = parser.parse_args()
    ignored = set(args.ignore) if args.ignore else set()
    
    main(args.schema_file, args.output, ignored)
