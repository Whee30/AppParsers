This is a small assortment of scripts pointed at the "Potato Chat" app. The application is an offshoot of Telegram which popped up recently on my radar and needed some research.

decode_BLOB.py
  attempts to parse through the BLOBs as extracted from tgdata.db / channel_conversations_v32. This script loses its way currently when decoding certain variable length integers.
  There are some offsets that are broken when interpreting the varints. But effectively the benchmark goes:
  1 byte for length of key
  x bytes for ASCII key
  1 byte for data type (str/int/varint so far)
  based on type, 4 bytes, 8 bytes or variable length from this point
  and repeat...
  Interpretations are included wherever they are "known", this is a script under flux however and is subject to change with new research

iterate_blobs.py
  After identifying a suspect or user of interest, this will iterate through tgdata.db and export the BLOBs from the channel_messages_v32 table. Could easily be pointed at other tables as needed. Currently the user ID is hardcoded, not dynamic.

parse_logs.py
  This script iterates line by line through the application logs for a specific string and spits out instances. Usedul for certain indicators of a file being downloaded

parse_shareDialogList.py
  This script parses the shareDialogList.db and spits out a formatted version of the data therein. Group and Individual chats a user is part of... 
  This is the least necessary as this database holds some easily readable data, but here it is if anyone else finds it useful.

/sample_BLOBs/
  contains some raw BLOBs to test out decode_BLOB.py with.
