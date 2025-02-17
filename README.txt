Andrei's PL/SQL cleaner. 
Run steps:
- Add your SQL code to "add_your_sql_here.sql".
- The bat file may be considered unsafe. If so, rightclick it, go to properties, unblock it.
- Considering you have python installed, run .bat file "run_me.bat". This will just run the command "py plsql_cleaner.py" for you.
- Your new cleaned code is now in clean_sql.sql
- NOTE: The new combined DECLARE block is not perfect yet. You have to: remove duplicates, take care of any variables that may have the same name but different types. 