import time
import schedule
import openpyxl
import os
from mysql.connector import connect


def create_row():
    conn = connect(host="172.105.112.190",user="talha",passwd="T@lha123%")
    cursor = conn.cursor()
    data = []
    cursor.execute("""
                    select ride_id,car_service,(SELECT count(*) FROM test.ridesMongoActive where ride_status='FINISHED' and test.ridesMongoActive.event_time between DATE_SUB(Now(),INTERVAL 1 Hour) and now()) as "Number of DriversRIdes",
                        (SELECT count(*) FROM test.ridesMongoActive where ride_status='FINISHED' and test.ridesMongoActive.event_time between DATE_SUB(Now(),INTERVAL 1 HOUR) and now())as "Number of CustomerRides",
                        phone,driver_phone 
                    from test.ridesMongoActive
                    inner join test.driversMongoSql
	                    on test.ridesMongoActive.driver_id = test.driversMongoSql.id
                    where test.ridesMongoActive.event_time between DATE_SUB(Now(),INTERVAL 1 Hour) and now();
                    """)
    row_data = []
    for cur in cursor.fetchall():
        for c in cur:
            row_data.append(c)
        data.append(row_data)
        row_data = []
    return data


# switch = 0
column_names = ["Ride_id","car_service","Number of DriversRIdes","Number of CustomerRides","phone","driver_phone"]
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
schedule.every().hour.do(generate_report)
#schedule.every(1).minutes.do(generate_report)
while True:
    schedule.run_pending()
    time.sleep(1)


# generate_report()
