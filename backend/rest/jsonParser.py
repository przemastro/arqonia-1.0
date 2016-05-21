import mysql.connector
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')
from mysql.connector import errorcode

#-----------------------------------------insert new employee to tablelist----------------------------------------------
def json_parser(name, lastName, dateOfBirth, address, grossIncome, netIncome):
 try:
    cnx = mysql.connector.connect(user='root',
                                  database='testApp')

    cursor = cnx.cursor()

    get_lastId = ("select id from testapp.tablelist order by id desc limit 1")
    cursor.execute(get_lastId)
    lastId = cursor.fetchone()

    if lastId is None:
       lastId = 1
    else:
       lastId = lastId[0] + 1

    lastId = str(lastId)
    name = str(name)
    lastName = str(lastName)
    dateOfBirth = str(dateOfBirth)
    address = str(address)
    grossIncome = str(grossIncome)
    netIncome = str(netIncome)

    insert_employee = ("insert into testapp.tablelist(id, Name, LastName, DateOfBirth, Address, GrossIncome, NetIncome) "
                       "values("+lastId+",'"+name+"', '"+lastName+"', '"+dateOfBirth+"', '"+address+"', '"+grossIncome+"', '"+netIncome+"')")

    print insert_employee

    cursor.execute(insert_employee)
    cnx.commit()

    cursor.close()

 except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
 else:
    cnx.close()

#----------------------------------------------insert candidate's work to area------------------------------------------
def json_candidate(name):
    try:
        cnx = mysql.connector.connect(user='root',
                                      database='testApp')

        cursor = cnx.cursor()

        get_lastId = ("select id from testapp.area order by id desc limit 1")
        cursor.execute(get_lastId)
        lastId = cursor.fetchone()
        if lastId is None:
           lastId = 1
        else:
            lastId = lastId[0] + 1

        lastId = str(lastId)
        name = str(name)
        name = re.escape(name)

        insert_text = ("insert into testapp.area(id, area) "
                       "values("+lastId+",'"+name+"')")

        print insert_text

        cursor.execute(insert_text)
        cnx.commit()

        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

#----------------------------------------------------insert uploaded file-----------------------------------------------
def json_file(fileName, fileType):
    try:
        cnx = mysql.connector.connect(user='root',
                                      database='testApp')

        cursor = cnx.cursor()

        get_lastId = ("select id from testapp.uploadedfile order by id desc limit 1")
        cursor.execute(get_lastId)
        lastId = cursor.fetchone()
        if lastId is None:
            lastId = 1
        else:
            lastId = lastId[0] + 1

        lastId = str(lastId)
        fileName = str(fileName)
        fileName = re.escape(fileName)
        fileType = str(fileType)
        fileType = re.escape(fileType)

        insert_text = ("insert into testapp.uploadedFile(id, fileName, fileType) "
                       "values("+lastId+",'"+fileName+"','"+fileType+"')")

        print insert_text

        cursor.execute(insert_text)
        cnx.commit()

        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()