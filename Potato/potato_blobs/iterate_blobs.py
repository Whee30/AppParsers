import sqlite3
#import xlsxwriter
from datetime import datetime

connection = sqlite3.connect('tgdata.db', uri=True)
# this line will output the table into a dictionary where each column can be called
# it will require that the column name be called by using: variable['columnName']
connection.row_factory = sqlite3.Row
cur = connection.cursor()
cur.execute("SELECT data FROM channel_messages_v32")

rows = ()
rows = cur.fetchall()

user_ids = []
group_ids = []

for each_row in rows:
    # Retrieve the BLOB data
    blob_data = each_row[0]
    offset = 68  # Define the offset (adjust as needed)
    num_bytes = 4  # Number of bytes to extract

    group_chat_id = blob_data[12:16]
    group_chat_int = int.from_bytes(group_chat_id, byteorder='little', signed=True)
    group_ids.append(group_chat_int)

    # Extract four bytes starting from the offset
    extracted_bytes = blob_data[offset:offset + num_bytes]
    extracted_int = int.from_bytes(extracted_bytes, byteorder='little')
    user_ids.append(extracted_int)

for index, each_id in enumerate(user_ids):
    if each_id == 91399161:
        entry = index + 1
        filename = str(entry) + '_' + str(group_ids[index])
        print(f"Match found in row: {index + 1}")
        with open(filename, 'wb') as file:
            file.write(rows[index][0])



#print(rows)
#print(user_ids)