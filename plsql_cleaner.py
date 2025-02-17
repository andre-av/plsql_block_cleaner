import re

def extract_declare_begin_blocks(sql_file_path):
    
    print("Opening SQL File.")
    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_text = file.read()

    print("Beginning extraction of declare blocks.")
    # Regular expression pattern to capture DECLARE blocks.
    declare_pattern = r"DECLARE\s+(.*?)(?=\s+BEGIN)"  # Non-greedy match up to BEGIN.

    # Find all matches (using DOTALL to match across multiple lines).
    declare_blocks = re.findall(declare_pattern, sql_text, re.DOTALL | re.IGNORECASE)

    print("Beginning extraction of begin blocks.")
    # Regular expression pattern to capture BEGIN...END blocks.
    begin_pattern = r"BEGIN\s+(.*?)(?=\s+END;)"  # Capture everything between BEGIN and END;.

    # Find all matches (using DOTALL to match across multiple lines).
    begin_blocks = re.findall(begin_pattern, sql_text, re.DOTALL | re.IGNORECASE)

    print("Block extraction done.")
    return declare_blocks, begin_blocks


# === WORK IN PROGRESS, needs more work for skipping CURSORs properly. === 
# def process_declare_section(section):
#     """
#     Process each DECLARE section, ensuring that variables are only declared once.
#     """
#     lines = section.strip().splitlines()
#     new_lines = []
#     declared_variables = {}
    
#     for line in lines:
#         line = line.strip()
#         if line:  # Avoid empty lines
#             # Extract variable and type (assuming standard DECLARE syntax)
#             match = re.match(r"(\w+)\s+(\w+)", line)  # (variable, type)
#             if match:
#                 var_name, var_type = match.groups()

#                 if var_name == "CURSOR": # Ignore CURSORs
#                     continue

#                 if var_name in declared_variables and var_type != declared_variables[var_name]:
#                     print(f"varname: {var_name}, vartype: {var_type}, existing_vartype: {declared_variables[var_name]}")
#                     raise Exception(f"{var_name} is declared multiple times, with DIFFERENT types. Edit the file and change its name or type accordingly.")
                
#                 # Check if the variable has already been declared
#                 if var_name not in declared_variables:
#                     declared_variables[var_name] = var_type  # Add to dictionary of declared variables
#                     new_lines.append(f"  {line}")  # Keep the line if variable is unique
                    
#     return new_lines


def create_sql_block(declare_blocks, begin_blocks):


    # DECLARE Block.
    print("Creating final DECLARE block.")
    sql_code = "DECLARE\n"
    
    for section in declare_blocks:
        lines = section.strip().splitlines()
        for line in lines:
            sql_code += f"  {line.strip()}\n"
        sql_code += "\n"

    # BEGIN Block.
    print("Creating final BEGIN block.")
    sql_code += "BEGIN\n"

    for section in begin_blocks:
        lines = section.strip().splitlines()
        for line in lines:
            sql_code += f"  {line.strip()}\n"
        sql_code += "-- ===\n"

    sql_code += "END;\n/\n"

    print("Returning final code.")
    return sql_code


def write_to_sql_file(output_file_path, sql_script):
    print("Creating SQL File.")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(sql_script)

# === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === 

initial_sql_file = "add_your_sql_here.sql"
clean_sql_file = "clean_sql.sql"

# Extract DECLARE and BEGIN-END blocks.
declare_blocks, begin_blocks = extract_declare_begin_blocks(initial_sql_file)

# Create one-block PL/SQL file.
oneblock_sql = create_sql_block(declare_blocks, begin_blocks)

write_to_sql_file(clean_sql_file, oneblock_sql)

