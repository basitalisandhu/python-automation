import time
import schedule
import openpyxl
import os
from mysql.connector import connect


def create_row():
    conn = connect(host="127.0.0.1",user="root",password="12345678",database="logi")
    cursor = conn.cursor()
    data = []
    cursor.execute("""
                   SHOW TABLES FROM `logi`;
                    """)
    row_data = []
    for cur in cursor.fetchall():
        for c in cur:
            row_data.append(c)
        data.append(row_data)
        row_data = []
    return data


# switch = 0
column_names = ["Table Names"]
def generate_report():
    data = create_row()

    PATH = './tmp/log_file.xlsx'
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        wb = openpyxl.load_workbook('tmp/log_file.xlsx')
        sheet = wb["Sheet"]

        for row in data:
            sheet.append(row)
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(column_names)

        sheet = wb["Sheet"]

        for row in data:
            sheet.append(row)
    
    wb.save('tmp/log_file.xlsx')
# schedule.every().hour.do(generate_report)
# #schedule.every(1).minutes.do(generate_report)
# while True:
#     schedule.run_pending()
#     time.sleep(1)


generate_report()
