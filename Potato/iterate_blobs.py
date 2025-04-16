import sqlite3
from datetime import datetime
import argparse
import sys

user_input = argparse.ArgumentParser(description="Call the script, target your tgdata.db database and specify an output directory. Optionally provide a user ID OR a group ID to target one of those.")

# Define the expected flag and argument
user_input.add_argument("-d", "--database", required=True, help="Path to the input file")
user_input.add_argument("-o", "--output", required=True, help="Path to the output directory")

parse_method = user_input.add_mutually_exclusive_group(required=False)
parse_method.add_argument("-u", "--user", required=False, help="Optional user ID")
parse_method.add_argument("-c", "--chat", required=False, help="Optional chat ID")

# Parse the command-line arguments
args = user_input.parse_args()

if not args.file:
    print("Error: a database must be specified. A specific user OR a specific chat may also be specified by using -u OR -c, respectively.")
    print("Usage: python script.py -d <database file> -o <output directory>")
    sys.exit(1)

connection = sqlite3.connect(user_input.file, uri=True)
connection.row_factory = sqlite3.Row
cur = connection.cursor()
# Choose the table and column here
cur.execute("SELECT data FROM channel_messages_v32")

rows = ()
rows = cur.fetchall()

user_ids = []
group_ids = []

for each_row in rows:
    # Retrieve the BLOB data
    blob_data = each_row[0]
    offset = 68  # user ID is found at offset 0x44 for 4 bytes
    num_bytes = 4  # Number of bytes to extract

    group_chat_id = blob_data[12:16] # chat ID is found at offset 0x0c for 4 bytes
    group_chat_int = int.from_bytes(group_chat_id, byteorder='little', signed=True)
    group_ids.append(group_chat_int)

    # Extract four bytes starting from the offset
    extracted_bytes = blob_data[offset:offset + num_bytes]
    extracted_int = int.from_bytes(extracted_bytes, byteorder='little')
    user_ids.append(extracted_int)



if user_input.user: # Iterate all of the BLOBs from a specific user
    for index, each_id in enumerate(user_ids):
        if each_id == user_input.user: # Optional user ID supplied by -u/--user flag
            entry = index + 1
            filename = str(entry) + '_' + str(group_ids[index]) # filenames will be [database entry #]_[group ID]
            print(f"Match found in row: {index + 1}")
            with open(filename, 'wb') as file: # extract the BLOBs for further examination 
                file.write(rows[index][0])
                
elif user_input.chat: # iterate all of the BLOBs from a specific chat
    for index, each_id in enumerate(user_ids):
        if each_id == user_input.user: # Optional user ID supplied by -u/--user flag
            entry = index + 1
            filename = str(entry) + '_' + str(group_ids[index]) # filenames will be [database entry #]_[group ID]
            print(f"Match found in row: {index + 1}")
            with open(filename, 'wb') as file: # extract the BLOBs for further examination 
                file.write(rows[index][0])
                
else: # iterate all of the blobs from the database
    for index, each_id in enumerate(user_ids):
        if each_id == user_input.user: # Optional user ID supplied by -u/--user flag
            entry = index + 1
            filename = str(entry) + '_' + str(group_ids[index]) # filenames will be [database entry #]_[group ID]
            print(f"Match found in row: {index + 1}")
            with open(filename, 'wb') as file: # extract the BLOBs for further examination 
                file.write(rows[index][0])
