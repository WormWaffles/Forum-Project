# Forum-Project

# Setting up the Database

This guide will help you set up a database on your local machine for use with your project.

## Prerequisites

- [DataGrip](https://www.jetbrains.com/datagrip/) installed on your machine
- Access to the `database_schema.sql` file
- pip install -r requirements.txt 

## Steps

1. Open your console in DataGrip
2. Paste the first line **ONLY THE FIRST LINE** of `database_schema.sql` into the console
3. Run the command by pressing alt enter
4. Change the dropdown in the top right of the console window (find the green play button and go right, its the second to last drop down) to the name of the database (e.g. barhive)
5. Copy the two tables, one by one, from the `database_schema.sql` file and paste them into the console
6. Run each command by pressing alt enter
7. Enter the database credentials in the `.env.sample` file
8. Change the file name to `.env`

*NOTE: If you see the option to "introspect schema", click that*

Congratulations! You have now set up your database on your local machine.
