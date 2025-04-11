from mdb_parser import MDBParser, MDBTable

db = MDBParser(file_path="/potato_mdb/data.mdb")

# Get and print the database tables
print(db.)

# Get a table from the DB.
#table = db.get_table("MY_TABLE_NAME")

# Or you can use the MDBTable class.
#table = MDBTable(file_path="db.accdb", table="MY_TABLE_NAME")

# Get and print the table columns.
#print(table.columns)

# Iterate the table rows.
#for row in table:
#    print(row)