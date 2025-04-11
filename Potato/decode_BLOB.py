import sys

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
        title_length = int.from_bytes(input_file.read(1), byteorder="little") # int.from_bytes(blob_data[working_offset:working_offset + 1], byteorder="little")

        if not title_length:
            break

        ASCII_title = file.read(title_length).decode()# blob_data[working_offset:working_offset + working_length].decode()

        # Get the data type and then apply the corresponding payload length
        data_type = int.from_bytes(input_file.read(1), byteorder="little")
        if data_type == 1:
            data_length = int.from_bytes(input_file.read(1), byteorder="little")
        elif data_type == 2:
            data_length = 4
        elif data_type == 3:
            data_length = 8
        elif data_type ==4:
            print("unknown data type of 4")
        elif data_type == 6:
            data_length = int.from_bytes(input_file.read(1), byteorder="little")
        else:
            print(f"Unsupported data type of {data_type} encountered. Program exiting.")

        payload_data = input_file.read(data_length)
        # Format and hex characters fro presentation
        formatted_bytes = ' '.join(f'{byte:02X}' for byte in payload_data)

        print(f"{ASCII_title}, data type {data_type}:")
        print(f"\tHex: {formatted_bytes}")
        print(f"\tDecimal (LE): {int.from_bytes(payload_data, byteorder="little")}")
        print(f"\tDecimal (BE): {int.from_bytes(payload_data, byteorder="big")}")
        print(f"\tASCII: {payload_data.decode('utf-8', errors='ignore')}")




def get_variable_length():
    print("uh oh")

with open(target_file, "rb") as file:
    iterate_pattern(file)