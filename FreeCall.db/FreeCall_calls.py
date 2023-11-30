import sqlite3
import xlsxwriter
from datetime import datetime

connection = sqlite3.connect('./FreeCall.db', uri=True)
# this line will output the table into a dictionary where each column can be called
# it will require that the column name be called by using: variable['columnName']
connection.row_factory = sqlite3.Row
cur = connection.cursor()
cur.execute("SELECT * FROM t_localCallLogs")

rows = {}
rows = cur.fetchall()

def dateChanger(inputValue):
   inputValueInt = int(inputValue)
   timeHolder = datetime.fromtimestamp(inputValueInt)
   formatted = timeHolder.strftime("%Y-%m-%d %H:%M:%S")
   return formatted

# Create an new Excel file and add a worksheet
workbook = xlsxwriter.Workbook('FreeCall Calls.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})
word_wrap = workbook.add_format({'text_wrap': True})

# Set column widths and freeze top row
worksheet.set_column('A:D', 20)
worksheet.freeze_panes(1, 0)

# Define columns
worksheet.write(0,0,'Caller', bold)
worksheet.write(0,1,'Recipient', bold)
worksheet.write(0,2,'Start', bold)
worksheet.write(0,3,'End', bold)

i = 1
for each_row in rows:
      formatted = 0
      time_start = 0
      time_start = dateChanger(each_row['start_time'])
      time_end = 0
      time_end = dateChanger(each_row['end_time'])
      caller = ''
      caller = each_row['local_num']
      recipient = ''
      recipient = each_row['remote_num']
      worksheet.write(i, 0, caller)
      worksheet.write(i, 1, recipient)
      worksheet.write(i, 2, time_start)
      worksheet.write(i, 3, time_end)
      i = i + 1

workbook.close()
