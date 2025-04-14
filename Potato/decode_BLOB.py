import sys
import datetime

# Check if the user provided the target file as an argument
if len(sys.argv) != 2:
    print("Usage: python script.py <target file>")
    sys.exit(1)

# Get the target file from the command-line arguments
target_file = sys.argv[1]

print(f"The target file is: {target_file}")


def iterate_pattern(input_file):
    #blob_data = input_file.read()
    working_length = 1
    working_offset = 0
    data_type = 0
    data_length = 0

    # one byte length of title
    # variable length title in ASCII
    # one byte data type
    # 0x01 = 1 byte
    # 0x02 = 4 bytes
    # 0x03 = 8 bytes
    # 0x06 = Variable payload
    # Next byte declares length of payload
    # variable length payload

    while True:
        # Get the length of the title
        title_length = int.from_bytes(input_file.read(1), byteorder="little")
        
        if not title_length:
            break

        ASCII_title = file.read(title_length).decode('utf-8', errors='replace')

        # Get the data type and then apply the corresponding payload length
        data_type = int.from_bytes(input_file.read(1), byteorder='little')
        if data_type == 1:
            d_t = "Str"
            data_length = int.from_bytes(input_file.read(1), byteorder="little")
        elif data_type == 2:
            d_t = "Int"
            data_length = 4
        elif data_type == 3:
            d_t = "Int"
            data_length = 8
        elif data_type ==4:
            d_t = "Unk"
            print("unknown data type of 4")
        elif data_type == 6:
            d_t = "Varint"
            data_length = get_variable_length(file)
            # data_length = int.from_bytes(input_file.read(1), byteorder="little")
        else:
            print(f"Unsupported data type of {data_type} encountered. Program exiting.")

        payload_data = input_file.read(data_length)
        # Format and hex characters fro presentation
        formatted_bytes = ' '.join(f'{byte:02X}' for byte in payload_data)

        if d_t == "Int":
            print(f"{ASCII_title}, data type '{d_t}':")
            print(f"\tHex: {formatted_bytes}")
            print(f"\tDecimal (LE): {int.from_bytes(payload_data, byteorder='little')}")
            if ASCII_title == 'd':
                print(f"\tDate: {datetime.datetime.fromtimestamp(int.from_bytes(payload_data, byteorder='little'), datetime.UTC)})")
            elif ASCII_title == "fi":
                print(f"\tUser ID: {int.from_bytes(payload_data, byteorder='little')}")
            elif ASCII_title == "ti" or ASCII_title == "ci":
                group_ID = int.from_bytes(payload_data[0:4], byteorder="little", signed=True)
                print(f"\tFirst four bytes = Group ID: {abs(group_ID)}")
            elif ASCII_title == 'i':
                print(f"\tMessage {int.from_bytes(payload_data, byteorder='little')} within the group chat.")
                
            print('')
        if d_t == "Varint":
            print(f"{ASCII_title}, data type '{d_t}':")
            print(f"\tHex: {formatted_bytes}")
            # print(f"\tASCII: {payload_data.decode('utf-8', errors='replace')}")
            if ASCII_title == "sk":
                group_ID = int.from_bytes(payload_data[0:4], byteorder="little", signed=True)
                print(f"\tFirst four bytes = Group ID: {abs(group_ID)}")
            print('')
        if d_t == "Str":
            print(f"{ASCII_title}, data type '{d_t}':")
            print(f"\tASCII: {payload_data.decode('utf-8', errors='replace')}")
            print('')        





def get_variable_length(file):
    value = 0
    shift = 0

    while True:
        byte = file.read(1)  # Read one byte from the file
        if not byte:
            raise EOFError("Unexpected end of file while decoding varint")

        byte = ord(byte)  # Convert byte to integer
        value |= (byte & 0x7F) << shift  # Combine the lower 7 bits
        shift += 7

        if (byte & 0x80) == 0:  # MSB is 0, end of varint
            break

    return value

with open(target_file, "rb") as file:
    iterate_pattern(file)