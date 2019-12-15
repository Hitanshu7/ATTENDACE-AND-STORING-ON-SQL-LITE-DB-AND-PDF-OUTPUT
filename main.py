import sqlite3
from datetime import datetime
from sqlite3 import Error
from reportlab.pdfgen import canvas
import constants
import os
from espeakng import ESpeakNG

if not os.path.exists("media"):
    os.mkdir("media")

if not os.path.exists("database"):
    os.mkdir("database")

if not os.path.exists("pdfs"):
    os.mkdir("pdfs")

def exportPdf(fileName, connectionObject, student_count, teacher_count):
    """
    This function consists of logic for generation of pdf
    """
    c = canvas.Canvas(fileName)
    databaseResults = connectionObject.fetchall()
    labels = ["id: ", "sap: ", "   Date: ", "   In: ", "   out: ", "is_in: ", "  is_teacher:"]
    y_pos = [x for x in range(750, 0, -30)]
    teacher = "Teachers Count: {}".format(teacher_count)
    student = "Students Count: {}".format(student_count)
    for i, data in enumerate(databaseResults):
        dataStringList = [labels[j] + str(entry) for j, entry in enumerate(data)]
        for j in range(-2, 1):
            dataStringList.pop(j)
        if i % 25 == 0 and i != 0:
            c.showPage()
        c.drawString(100, y_pos[i % 25], " ".join(dataStringList))
    if (i+1) % 25 == 0 and i != 0:
        c.showPage()
    c.drawString(100, y_pos[(i+1) % 25], teacher)
    c.drawString(100, y_pos[(i+2) % 25], student)
    c.save()


def validate_sap_id(sap_id):
    """
    Validation of the SAP_ID to be entered by ID Card Scanner
    """
    size = len(sap_id)
    if size == 7 and sap_id[0] is not '0' and sap_id[0] == '9':
        return '1' + sap_id, 1
    elif size == 3 and sap_id[0] is not '0':
        return sap_id, 1
    elif size == 11:
        return sap_id, 0
    else:
        esng = ESpeakNG()
        esng.say("Try again")
        return None, -1


def create_table_connection():
    """
    Create Table and establish connection
    """
    str_date = datetime.now().strftime("%b-%Y")
    file_name = constants.path_to_database + "library-" + str_date + ".db"
    conn = sqlite3.connect(file_name)
    try:
        c = conn.cursor()
        c.execute(constants.create_table)
        return conn
    except Error as e:
        print(e)


def data_entry(conn, sap_id):
    """
    Entry of SAP_ID and check if entry already exists with Out time as none
    then update it else create a new entry.Also checks if entered SAP_ID is of student
    or teacher
    """
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    sap_id, is_teacher = validate_sap_id(sap_id)
    c = conn.cursor()
    if sap_id is not None:
        c.execute(constants.check_entry_data, (sap_id, date, 1))
        row = c.fetchall()

        if is_teacher == -1:
            return
        else:
            if row:
                c.execute(constants.update_data, (time, 0, sap_id, 1))
            else:
                c.execute(constants.insert_data, (sap_id, date, time, 1, is_teacher))
            conn.commit()


def pdf_generation(str_date, conn):
    """
    Trigger exportPdf function and add count of students and teachers to pdf
    """
    file_name = constants.path_to_pdfs + "library-" + str_date + ".pdf"
    p = conn.execute(constants.retrieve_all_data)
    total_count = len([row for row in p])
    count = conn.execute(constants.count_insertion, (1,))
    teacher_count = len([row for row in count])
    student_count = total_count - teacher_count
    p = conn.execute(constants.retrieve_all_data)
    exportPdf(file_name, p, student_count, teacher_count)


# Main function to start the system
def main():
    c = create_table_connection()
    sap_id = ""
    while sap_id is not "q":
        sap_id = input("Enter the SAP ID:")

        if sap_id not in ['q','p','r','']:
            data_entry(c, sap_id)
        elif sap_id is "p":
            str_date = datetime.now().strftime("%b-%Y")
            pdf_generation(str_date, c)
        elif sap_id is 'r':
            name = input('Enter database month\nfor example Aug-2019:').strip()
            if name is not 'q':
                file_name = "library-" + name + ".db"
                conn = sqlite3.connect(file_name)
                c = conn.cursor()
                pdf_generation(name, c)
                c.close()
                c = create_table_connection()


if __name__ == "__main__":
    main()
