This script iterates through the "tgdata.db" database associated with the Potato Chat application. Specifically, this script will take a known user ID as found in the "tgdata.db/contacts_v32" table as well as the "org.potatochat.potatoenterprise.plist" file, and run through the "tgdata.db/channel_messages_v32" table in the "data" column. This column stores BLOB data which is currently not completely benchamrked/decoded. I am working on the parsing of this data, however I have learned several things so far about the data:

The user ID for a particular group message can be found consistently at offset 0x44 for 4 bytes. This script will take the user ID as an integer and search the offset of each BLOB for the little endian hex and spit out BLOB files associated with that user ID for individual examination.

It will also append the chat ID the post was associated with into the filename. The chat ID is found at offset 0x0c for 4 bytes, big endian. The chat IDs match the chat threads listed in the "shareDialogList.db" database. In this way you can correlate the BLOBs to specific chats.

If the post is an image being sent, the image ID (in iOS, filename saved to ~/Shared/~/Documents/Files/) is found at offset 0x86 for 8 bytes, little endian.

In my actual case, this boiled 50k+ entries down to around 14 entries that I could focus on. This is very much a work in progress, I hope to eventually get this dataset parsed as the protobuf it clearly is. Would welcome help. I am not working on any sort of user interface at this stage since the translation isn't complete, but I would love to map the rest of the BLOB out and ideally contribute to a project such as the LEAPPs. If you have help to offer or if this can be accomplished by an existing tool, please let me know.
