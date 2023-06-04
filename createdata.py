import database

# You can alternatively run the `create_database.sql` query to achieve te same, cause basically that is what this script does
with open('create_database.sql', 'r') as file:
    database.cursor.execute(''.join(file.readlines()))

print('Sample data created and added the database successfully.')
    