import re
import traceback
import time


def extract_declare_begin_blocks(sql_file_path):
    
    print("Opening SQL File.")
    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_text = file.read()

    print("Beginning extraction of declare blocks.")
    # Regular expression pattern to capture DECLARE blocks.
    declare_pattern = r"DECLARE\s+(.*?)(?=\s+BEGIN)"  # Non-greedy match up to BEGIN.
    # declare_pattern = r"((?:--[^\n]*\n|/\*.*?\*/\s*)*)DECLARE\s+(.*?)(?=\s+BEGIN)"  # TODO retrieve comments INBETWEEN PL/SQL blocks.


    # Find all matches (using DOTALL to match across multiple lines).
    declare_blocks = re.findall(declare_pattern, sql_text, re.DOTALL | re.IGNORECASE)

    print("Beginning extraction of begin blocks.")
    # Regular expression pattern to capture BEGIN...END blocks.
    begin_pattern = r"BEGIN\s+(.*?)(?=\s+END;)"  # Capture everything between BEGIN and END;.

    # Find all matches (using DOTALL to match across multiple lines).
    begin_blocks = re.findall(begin_pattern, sql_text, re.DOTALL | re.IGNORECASE)

    print("Block extraction done.")
    return declare_blocks, begin_blocks


# Process each DECLARE section, ensure that variables are only declared once.
def process_declare_section(section):

    print("Removing duplicate declarations in final DECLARE block.")

    processed_lines = []
    declared_variables = {}
    
    for line in section:
        line = line.strip() # Remove extra spaces/newlines.

        match = re.match(r"(\w+)\s+(\w+).*;", line) 

        # If it's not a variable, or is a cursor, or a new-line continuation of a cursor, preserve as-is.
        if line.upper().startswith("CURSOR") or not match: 
            processed_lines.append(line)
            continue

        # Extract variable and type (assuming standard DECLARE syntax).
        if match:
            var_name, var_type = match.groups()

            if var_name in declared_variables and var_type != declared_variables[var_name]:
                print(f"\n === === ERROR! === ===")
                print(f"Variable {var_name} is declared multiple times, with DIFFERENT types.\nEdit the file and change its name or type accordingly.")
                print(f"- Variable: {var_name}")
                print(f"- Existing variable type: {declared_variables[var_name]}")
                print(f"- New variable type found: {var_type} ")
                input("\nProgram stopped prematurely. Press ENTER to exit.")  # Preventing window from closing immediately.
                raise Exception(f"{var_name} is declared multiple times, with DIFFERENT types. Edit the file and change its name or type accordingly.")

            
            # Check if the variable has     already been declared
            if var_name not in declared_variables:
                declared_variables[var_name] = var_type  # Add to dictionary of declared variables
                processed_lines.append(f"  {line}")  # Keep the line if variable is unique

    return processed_lines


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
        sql_code += "\n-- ===\n"

    sql_code += "END;\n/\n"

    print("Returning final code.")
    return sql_code


def write_to_sql_file(output_file_path, sql_script):
    print("Creating SQL File.")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(sql_script)


def run_program():
    print("")
    initial_sql_file = "add_your_sql_here.sql"
    clean_sql_file = "clean_sql.sql"

    # Extract DECLARE and BEGIN-END blocks.
    declare_blocks, begin_blocks = extract_declare_begin_blocks(initial_sql_file)

    # Remove variable duplicates. Check if there are duplicate variables with different types.
    declare_blocks = process_declare_section(declare_blocks)

    # Create one-block PL/SQL file.
    oneblock_sql = create_sql_block(declare_blocks, begin_blocks)

    write_to_sql_file(clean_sql_file, oneblock_sql)

    print("\nSuccessful. Closing in 2s.")
    time.sleep(2)


# === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === === 

run_program()