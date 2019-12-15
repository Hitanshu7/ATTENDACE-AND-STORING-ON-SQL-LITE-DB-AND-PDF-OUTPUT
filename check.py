import pyodbc
from datetime import datetime, timedelta
update_data = """ UPDATE RfidTimestamps SET EndTime=?, isEntry=? WHERE (RfidCode,isEntry)=(?,?);"""
check_entry_data = """ SELECT * FROM RfidTimestamps WHERE (RfidCode,Date,isEntry)=(?,?,?); """
insert_data = """ INSERT INTO RfidTimestamps ( RfidCode, Date, StartTime, isEntry,UserName) VALUES ( ?,?,?,?,? );"""
#user_name=("SELECT UserName FROM RfidUsers WHERE RfidCode=?", (rfidcode,))
def create_table_connection():
    server='s18.winhost.com'
    database= 'DB_128266_adsdb'
    username = 'DB_128266_adsdb_user'
    password = 'Mafs@2012'
    print(pyodbc.drivers())
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    try:
        c = conn.cursor()
        print("Connected")  
        return conn
    except Error as e:
        print(e)
    #c.execute("SELECT * from UmasUsers where DisplayName='Hitanshu Rami' OR DisplayName='Prashant Kumar'")
    #row = c.fetchone()
    #while row:
    #    print(row)
    #    row = c.fetchone()

def data_entry(conn, rfidcode):
    
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    #is_teacher = validate_rfidcode(rfidcode)
    c = conn.cursor()
    username=c.execute("SELECT UserName FROM RfidUsers WHERE RfidCode=?", (rfidcode,))
    user_name=username.fetchone()
    print(user_name[0])
    
    #print(user_name)
   
    c.execute(""" SELECT * FROM RfidTimestamps WHERE (RfidCode,Date,isEntry)=(?,?,?); """, (rfidcode,date,1))
##    c.execute(" SELECT * FROM RfidTimestamps WHERE (RfidCode,Date,isEntry)=(?,?,?); ", (rfidcode, date, 1))
##    row = c.fetchall()
##    if row:
##        c.execute(update_data, (time, 0, rfidcode, 1))
##    else:
##        c.execute(insert_data, (rfidcode, date, time, 1, user_name[0]))
##        conn.commit()    
def main():
    c = create_table_connection()
    rfidcode = ""
    while rfidcode is not "q":
        rfidcode = input("Scan the  ID:")
        if rfidcode != "q" and rfidcode != "p" and rfidcode != "r" and rfidcode != "":
            data_entry(c, rfidcode)
        elif rfidcode is "p":
            str_date = datetime.now().strftime("%b-%Y")
            pdf_generation(str_date, c)
        elif rfidcode is 'r':
            name = input('Enter database month as (Aug-2019):').strip()
            if name is not 'q':
                file_name = "library-" + name + ".db"
                conn = sqlite3.connect(file_name)
                c = conn.cursor()
                pdf_generation(name, c)
                c.close()
                c = create_table_connection() 
if __name__ == "__main__":
    main()  
