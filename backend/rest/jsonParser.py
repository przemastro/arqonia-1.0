import sys
import re
import pyodbc

reload(sys)
sys.setdefaultencoding('utf8')

#-----------------------------------------insert new employee to tablelist----------------------------------------------
def json_parser(name, startDate, endDate, uPhotometry, vPhotometry, bPhotometry):
 try:
    cnx = pyodbc.connect('Driver={SQL Server};Server=SAMSUNG-PC\SQLEXPRESS;Database=astro;Trusted_Connection=yes;uid=SAMSUNG-PC\SAMSUNG;pwd=')
    cursor = cnx.cursor()

    get_lastId = ("select top 1 id from dbo.StagingObservations order by id desc")
    cursor.execute(get_lastId)
    lastId = cursor.fetchone()

    if lastId is None:
       lastId = 1
    else:
       lastId = lastId[0] + 1

    lastId = str(lastId)
    name = str(name)
    startDate = str(startDate)
    endDate = str(endDate)
    uPhotometry = str(uPhotometry)
    vPhotometry = str(vPhotometry)
    bPhotometry = str(bPhotometry)

    insert_observation = ("insert into dbo.StagingObservations(id, Name, startDate, endDate, uPhotometry, vPhotometry, bPhotometry) "
                       "values("+lastId+",'"+name+"', '"+startDate+"', '"+endDate+"', '"+uPhotometry+"', '"+vPhotometry+"', '"+bPhotometry+"')")

    print insert_observation

    cursor.execute(insert_observation)
    cnx.commit()

    cursor.close()

 except:
   print 'errors'
 else:
   cnx.close()
