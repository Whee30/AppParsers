import sqlite3
import datetime
import argparse
import sys
import os

# Declare placeholder variables
#user_ids = []
#group_ids = []
#message_id = []
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


def iterate_pattern(input_blob, trio, dest):
   blob_length = len(input_blob)
   working_length = 1
   working_offset = 0
   data_type = 0
   data_length = 0
   title_length = 1

   parsed_file = trio + '.txt'

   #dest_path = os.path.join(dest, parsed_file)
   
   with open(dest + '/' + parsed_file,"w") as outfile:

      # Walk through the BLOB according to the observed pattern. When EOF or unsupported data is hit, the loop will quit.
      while working_offset < blob_length:
         # Get the length of the title
         print(f"Postion {working_offset} of {blob_length}")
         title_length = int.from_bytes(input_blob[working_offset:working_offset + working_length])
         
         working_offset += working_length

         ASCII_title = input_blob[working_offset:working_offset + title_length].decode('utf-8', errors='replace')
         
         working_offset += title_length
         
         data_type = int.from_bytes(input_blob[working_offset:working_offset + 1])
         
         working_offset += 1
         
         # Get the data type and then apply the corresponding payload length
         if data_type == 1: # May be a varint.
            d_t = "Str"
            data_length = int.from_bytes(input_blob[working_offset:working_offset + 1])
            working_offset += 1
         elif data_type == 2: # Not a boolean, though some fields appear to use it that way.
            d_t = "Int"
            data_length = 4
         elif data_type == 3:
            d_t = "Int"
            data_length = 8
         elif data_type == 6: # The fun one... data type 1 may also be a varint, needs testing.
            d_t = "Varint"
            x = working_offset
            d = input_blob
            value, offset = decode_varint(d, x)
            working_offset = offset
            data_length = value
            #working_offset += 1
         else:
            print(f"Unsupported data type of {data_type} encountered. Program exiting.")
            break
         
         # Defines the length of the current payload.
         payload_data = input_blob[working_offset:working_offset + data_length]
         
         sanitized_data = ''.join(char if 32 <= ord(char) <= 126 else '.' for char in payload_data.decode('utf-8', errors='replace'))
         
         working_offset += data_length
         
         # Format hex characters into pairs, minus the \x
         formatted_bytes = ' '.join(f'{byte:02X}' for byte in payload_data)

         if d_t == "Int":
            outfile.write(f"{ASCII_title}, data type '{d_t}':\n")
            outfile.write(f"\tHex: {formatted_bytes}\n")
            outfile.write(f"\tDecimal (LE): {int.from_bytes(payload_data, byteorder='little')}\n")
            if ASCII_title == 'd': # These have been observed to be timestamps
               outfile.write(f"\tDate: {datetime.datetime.fromtimestamp(int.from_bytes(payload_data, byteorder='little'), datetime.UTC)}\n")
            elif ASCII_title == "fi": # The full value isn't understood, but the User ID is consistently found
               outfile.write(f"\tUser ID: {int.from_bytes(payload_data, byteorder='little')}\n")
            elif ASCII_title == "ti" or ASCII_title == "ci": # The full value isn't understood, but the Group ID is consistently found.
               group_ID = int.from_bytes(payload_data[0:4], byteorder="little", signed=True)
               outfile.write(f"\tFirst four bytes = Group ID: {abs(group_ID)}\n")
            elif ASCII_title == 'i': # This integer declares what position within the group chat the message belongs.
               outfile.write(f"\tMessage {int.from_bytes(payload_data, byteorder='little')} within the group chat.\n")
            elif ASCII_title == 'unr' and int.from_bytes(payload_data, byteorder='little') == 1: # Appears to reference "Unread" status. Addtl testing would be prudent.
               outfile.write("\tUnread = True\n") 
            elif ASCII_title == 'unr' and int.from_bytes(payload_data, byteorder='little') == 0:
               outfile.write("\tUnread = False\n")
            elif ASCII_title == 'out' and int.from_bytes(payload_data, byteorder='little') == 1: # Appears to reference "outgoing" status. Addtl testing would be prudent.
               outfile.write("\tOutgoing = True\n")
            elif ASCII_title == 'out' and int.from_bytes(payload_data, byteorder='little') == 0:
               outfile.write("\tOutgoing = False\n")
            outfile.write('\n')
               
         if d_t == "Varint":
            outfile.write(f"{ASCII_title}, data type '{d_t}':\n")
            outfile.write(f"\tHex: {formatted_bytes}\n")
            outfile.write(f"\tASCII: {sanitized_data}\n")
            if ASCII_title == "sk": # Contains the group ID
               group_ID = int.from_bytes(payload_data[0:4], byteorder="little", signed=True)
               outfile.write(f"\tFirst four bytes = Group ID: {abs(group_ID)}\n")
            outfile.write('\n')

         if d_t == "Str": # Needs to be tested as to whether or not the payload length is a varint. It is likely a varint.
            outfile.write(f"{ASCII_title}, data type '{d_t}':\n")
            outfile.write(f"\tASCII: {sanitized_data}\n")
            outfile.write('\n')      
            

# Copilot did the heavy lift for this function. It appears to work as I have manually verified calculations
# I'd be lying if I said I fully understood the syntax. Varints are easy on paper, less so here.
def decode_varint(source_data, offset):
   value = 0
   shift = 0
   while True:
      byte = source_data[offset]  # Read a byte at the current offset
      offset += 1  # Increment the offset for the next byte

      value |= (byte & 0x7F) << shift  # Mask the MSB and shift bits into place
      shift += 7  # Move to the next group of bits

      if (byte & 0x80) == 0:  # If MSB is 0, end of varint
         break
   return value, offset  # Return the varint value and updated offset


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
         with open(init_filepath + filename, 'wb') as file: # extract the BLOBs for further examination 
            file.write(data)
         iterate_pattern(blob_data, filename, init_filepath)
   elif args.user: # Iterate all of the BLOBs from a specific user
      init_filepath = os.path.join(output_dir, 'user_' + str(extracted_int))
      if extracted_int == abs(int(args.user)):
         if not os.path.exists(init_filepath) or not os.path.isdir(init_filepath):
            os.mkdir(init_filepath)
         filename = 'user_' + str(extracted_int) + '_group_' + str(group_int) + '_' + str(mid) # filenames will be [group ID]_[database entry]
         with open(init_filepath + '/' + filename, 'wb') as file: # extract the BLOBs for further examination 
            file.write(data)
         iterate_pattern(blob_data, filename, init_filepath)
   else: # iterate all of the blobs from the database
      init_filepath = os.path.join(output_dir, 'group_' + str(group_int))
      if not os.path.exists(init_filepath) or not os.path.isdir(init_filepath):
         os.mkdir(init_filepath)
      filename = 'group_' + str(group_int) + '_' + str(mid) + '_user_' + str(extracted_int)  # filenames will be [group ID]_[database entry]
      with open(init_filepath + filename, 'wb') as file: # extract the BLOBs for further examination 
         file.write(data)
      iterate_pattern(blob_data, filename, init_filepath)

   


