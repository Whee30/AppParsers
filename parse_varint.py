# Varint testing based on values from BLOBs

varint = b'\xf3\x01'
# F3 01
# 1111 0011, 0000 0001
# 111 0011, 000 0001
# 000 0001, 111 0011
# Decimal 243



def get_variable_length(file):
   value = 0
   shift = 0

   for byte in varint:
      
      byte = bin(byte)  # Convert byte to integer
      print(byte)
      value |= (byte & 0x7F) << shift  # Combine the lower 7 bits
      shift += 7

      if (byte & 0x80) == 0:  # MSB is 0, end of varint
         break
   print(value)
   return value
 
get_variable_length(varint)