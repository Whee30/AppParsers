import json
import sqlite3

### These parsers are works in progress. Testing is ongoing, verify any results received.
### This script parses the shareDialogList.db file. This database contains two rows in testing so far
### Row 1 appears to be a list of contacts
### Row 2 appears to be a list of chat threads, groups and channels currently subscribed to.
### This script will print the data out into a text file. The data is already fairly readable, this just makes it into a nice list.
### Need to do: correlate the userId from chat thread to userId from contact list


connection = sqlite3.connect('shareDialogList.db', uri=True)
connection.row_factory = sqlite3.Row
cur = connection.cursor()
# Choose the table and column here
cur.execute("SELECT * FROM share_dialog_list_users_v29")

rows = ()
rows = cur.fetchall()

contact_list = []
group_list = []

name_and_id = {}

for row in rows:
    if row['typeId'] == 1:
        json_contacts = row['userInfosJson']
        try:
            contact_list = json.loads(json_contacts)
        except json.JSONDecodeError:
            print(f"Error decoding JSON for row: {row}")

    elif row['typeId'] == 2:
        json_groups = row['userInfosJson']
        try:
            group_list = json.loads(json_groups)
        except json.JSONDecodeError:
            print(f"Error decoding JSON for row: {row}")

for friend in contact_list:
    name_and_id[friend['userId']] = f"{friend['firstName']} {friend['lastName']}"

with open('group_chats_and_contacts.txt','w') as file:
    file.write(f"The user has the following contacts:\n\n")
    for friend in contact_list:
        file.write(f"\t{friend['firstName']} {friend['lastName']} - user ID: {friend['userId']}\n")
    file.write('\n\nThe user is part of the following groups/channels:\n\n')
    for group in group_list:
        if group['typeId'] == 3:
            file.write(f'\tGroup name: {group['title']}, Group ID: {group['groupId']}\n')

    file.write('\n\nThe user is part of the following one-on-one chat threads:\n\n')
    for group in group_list:
        if group['typeId'] == 1:
            file.write(f'\tUser ID: {group['userId']}\n')
