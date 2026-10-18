# DATABASE FOLDER
# SUMMARY:
This is the folder that will contain all files pertaining to the database.
The database itself will have a small collection of tables, all of which will be linked to the user table.
For the functional prototype we will require the following tables:
- Users
- Sheets
- Entries

These tables will follow the following rules:
- A user will be defined with a USER ID, a user name, and a hashed password which will be use for authentication
- A sheet will be defined with a Sheet ID, a foreign key (the user who owns the sheet), type (which for the prototype will be unused/the same across all sheets), and sheet data
- An entry will be defined with an Entry ID, name, several different (and optional) types, and an author foreign key, along with any custom user data as well. That is to say,
an entry will have several different, predefined categories such as type, but also a catch all section at the end with any non predefined type, like user notes. 
