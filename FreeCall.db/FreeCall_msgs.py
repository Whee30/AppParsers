
# Create an new Excel file and add a worksheet
workbook = xlsxwriter.Workbook('FreeCall Messages.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})
word_wrap = workbook.add_format({'text_wrap': True})

# Set column widths and freeze top row
worksheet.set_column('A:C', 20)
worksheet.set_column('D:D', 100, word_wrap)
worksheet.set_column('E:E', 20)
worksheet.freeze_panes(1, 0)

# Define columns
worksheet.write(0,0,'Time', bold)
worksheet.write(0,1,'Sender', bold)
worksheet.write(0,2,'Recipient', bold)
worksheet.write(0,3,'Body', bold)
worksheet.write(0,4,'Conversation ID', bold)

i = 1
for each_row in rows:
      formatted = 0
      time_stamp = 0
      time_stamp = dateChanger(each_row['timeInterval'])
      conversation_id = 'NULL'
      if each_row['conversationID'] == None:
         conversation_id = 'NULL'
      else:
         conversation_id = each_row['conversationID']
      sent_received = ''
      if each_row['smsType'] == 0:
         sent_received = "Sent"
      elif each_row['smsType'] == 1:
         sent_received = "Received"
      else:
         sent_received = "Unknown"
      sender = ''
      recipient = ''
      if sent_received == 'Sent':
         sender = each_row['localNum']
         recipient = each_row['areaNum']
      elif sent_received == 'Received':
         sender = each_row['areaNum']
         recipient = each_row['localNum']
      else:
         sender = 'unknown'
         recipient = 'unknown'
      worksheet.write(i, 0, time_stamp)
      worksheet.write(i, 1, sender)
      worksheet.write(i, 2, recipient)
      worksheet.write(i, 3, each_row['smsText'])
      worksheet.write(i, 4, conversation_id)
      i = i + 1

workbook.close()
