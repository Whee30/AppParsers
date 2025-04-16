import sys
import datetime



# Use this block to declare a block by running the program with the desired file through cmd: "script.py my_BLOB.bin"
# Check if the user provided the target file as an argument
#if len(sys.argv) != 2:
#    print("Usage: python script.py <target file>")
#    sys.exit(1)

#target_file = sys.argv[1]



# Use this block to explicitly declare a BLOB.
target_file = "sample_BLOBs/outgoing_image_reply_BLOB"

def iterate_pattern(input_file):
    blob_data = input_file.read()
    blob_length = len(blob_data)
    working_length = 1
    working_offset = 0
    data_type = 0
    data_length = 0
    title_length = 1

    # Walk through the BLOB according to the observed pattern. When EOF or unsupported data is hit, the loop will quit.
    while working_offset < blob_length:
        # Get the length of the title
        print(f"Postion {working_offset} of {blob_length}")
        title_length = int.from_bytes(blob_data[working_offset:working_offset + working_length])
        
        working_offset += working_length

        ASCII_title = blob_data[working_offset:working_offset + title_length].decode('utf-8', errors='replace')
        
        working_offset += title_length
        
        data_type = int.from_bytes(blob_data[working_offset:working_offset + 1])
        
        working_offset += 1
        
        # Get the data type and then apply the corresponding payload length
        if data_type == 1: # May be a varint.
            d_t = "Str"
            data_length = int.from_bytes(blob_data[working_offset:working_offset + 1])
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
            d = blob_data
            value, offset = decode_varint(d, x)
            working_offset = offset
            data_length = value
            #working_offset += 1
        else:
            print(f"Unsupported data type of {data_type} encountered. Program exiting.")
            break
        
        # Defines the length of the current payload.
        payload_data = blob_data[working_offset:working_offset + data_length]
        
        working_offset += data_length
        
        # Format hex characters into pairs, minus the \x
        formatted_bytes = ' '.join(f'{byte:02X}' for byte in payload_data)

        if d_t == "Int":
            print(f"{ASCII_title}, data type '{d_t}':")
            print(f"\tHex: {formatted_bytes}")
            print(f"\tDecimal (LE): {int.from_bytes(payload_data, byteorder='little')}")
            if ASCII_title == 'd': # These have been observed to be timestamps
                print(f"\tDate: {datetime.datetime.fromtimestamp(int.from_bytes(payload_data, byteorder='little'), datetime.UTC)})")
            elif ASCII_title == "fi": # The full value isn't understood, but the User ID is consistently found
                print(f"\tUser ID: {int.from_bytes(payload_data, byteorder='little')}")
            elif ASCII_title == "ti" or ASCII_title == "ci": # The full value isn't understood, but the Group ID is consistently found.
                group_ID = int.from_bytes(payload_data[0:4], byteorder="little", signed=True)
                print(f"\tFirst four bytes = Group ID: {abs(group_ID)}")
            elif ASCII_title == 'i': # This integer declares what position within the group chat the message belongs.
                print(f"\tMessage {int.from_bytes(payload_data, byteorder='little')} within the group chat.")
            elif ASCII_title == 'unr' and int.from_bytes(payload_data, byteorder='little') == 1: # Appears to reference "Unread" status. Addtl testing would be prudent.
                print("\tUnread = True") 
            elif ASCII_title == 'unr' and int.from_bytes(payload_data, byteorder='little') == 0:
                print("\tUnread = False")
            elif ASCII_title == 'out' and int.from_bytes(payload_data, byteorder='little') == 1: # Appears to reference "outgoing" status. Addtl testing would be prudent.
                print("\tOutgoing = True")
            elif ASCII_title == 'out' and int.from_bytes(payload_data, byteorder='little') == 0:
                print("\tOutgoing = False")
            print('')
            
        if d_t == "Varint":
            print(f"{ASCII_title}, data type '{d_t}':")
            print(f"\tHex: {formatted_bytes}")
            print(f"\tASCII: {payload_data.decode('utf-8', errors='replace')}")
            if ASCII_title == "sk": # Contains the group ID
                group_ID = int.from_bytes(payload_data[0:4], byteorder="little", signed=True)
                print(f"\tFirst four bytes = Group ID: {abs(group_ID)}")
            print('')

        if d_t == "Str": # Needs to be tested as to whether or not the payload length is a varint. It is likely a varint.
            print(f"{ASCII_title}, data type '{d_t}':")
            print(f"\tASCII: {payload_data.decode('utf-8', errors='replace')}")
            print('')      
            

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

# Now that everythign is established, lets iterate through the BLOB.
with open(target_file, "rb") as file:
    iterate_pattern(file)
