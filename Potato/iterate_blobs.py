import sqlite3
from datetime import datetime
import argparse
import sys
import os

# Declare placeholder variables
user_ids = []
group_ids = []
message_id = []
output_dir = ''

user_input = argparse.ArgumentParser(description="Call the script, target your tgdata.db database and specify an output directory. Optionally provide a user ID OR a group ID to target one of those.")

# Define the expected flag and argument
user_input.add_argument("-d", "--database", required=True, help="Path to the input file")
user_input.add_argument("-o", "--output", required=True, help="Path to the output directory")

parse_method = user_input.add_mutually_exclusive_group(required=False)
parse_method.add_argument("-u", "--user", required=False, help="Optional user ID")
parse_method.add_argument("-c", "--chat", required=False, help="Optional chat ID")

# Parse the command-line arguments
args = user_input.parse_args()

if not args.database:
    print("Error: a database must be specified. A specific user OR a specific chat may also be specified by using -u OR -c, respectively.")
    print("Usage: python script.py -d <database file> -o <output directory>")
    sys.exit(1)

connection = sqlite3.connect(args.database, uri=True)
connection.row_factory = sqlite3.Row
cur = connection.cursor()

# Choose the table and column here
cur.execute("SELECT mid, data FROM channel_messages_v32")

rows = ()
rows = cur.fetchall()

if not os.path.exists(str(args.output)) or not os.path.isdir(str(args.output)):
    os.mkdir(str(args.output))

output_dir = args.output

for mid, data in rows:
    # Retrieve the BLOB data
    blob_data = data
    offset = 68  # user ID is found at offset 0x44 for 4 bytes
    num_bytes = 4  # Number of bytes to extract

    group_id = blob_data[12:16] # chat ID is found at offset 0x0c for 4 bytes
    group_int = abs(int.from_bytes(group_id, byteorder='little', signed=True))
    
    # Extract four bytes starting from the offset
    extracted_bytes = blob_data[offset:offset + num_bytes]
    extracted_int = int.from_bytes(extracted_bytes, byteorder='little')

    # Not currently being used    
    #group_ids.append(group_int)
    #user_ids.append(extracted_int)
    #message_id.append(mid)
    
    if args.chat: # iterate all of the BLOBs from a specific chat
        init_filepath = os.path.join(output_dir, 'group_' + str(group_int))
        if group_int == abs(int(args.chat)):
            if not os.path.exists(init_filepath) or not os.path.isdir(init_filepath):
                os.mkdir(init_filepath)
            filename = 'group_' + str(group_int) + '_' + str(mid) + '_user_' + str(extracted_int) # filenames will be [group ID]_[database entry]
            filepath = os.path.join(init_filepath, filename)
            with open(filepath, 'wb') as file: # extract the BLOBs for further examination 
                file.write(data)
    elif args.user: # Iterate all of the BLOBs from a specific user
        init_filepath = os.path.join(output_dir, 'user_' + str(extracted_int))
        if extracted_int == abs(int(args.user)):
            if not os.path.exists(init_filepath) or not os.path.isdir(init_filepath):
                os.mkdir(init_filepath)
            filename = 'user_' + str(extracted_int) + '_group_' + str(group_int) + '_' + str(mid) # filenames will be [group ID]_[database entry]
            filepath = os.path.join(init_filepath, filename)
            with open(filepath, 'wb') as file: # extract the BLOBs for further examination 
                file.write(data)
    else: # iterate all of the blobs from the database
        init_filepath = os.path.join(output_dir, 'group_' + str(group_int))
        if not os.path.exists(init_filepath) or not os.path.isdir(init_filepath):
            os.mkdir(init_filepath)
        filename = 'group_' + str(group_int) + '_user_' + str(extracted_int) + '_' + str(mid) # filenames will be [group ID]_[database entry]
        filepath = os.path.join(init_filepath, filename)
        with open(filepath, 'wb') as file: # extract the BLOBs for further examination 
            file.write(data)
