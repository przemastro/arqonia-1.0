import sys
import re
import pyodbc

reload(sys)
sys.setdefaultencoding('utf8')

#-----------------------------------------insert new observation to tablelist-------------------------------------------
def json_parser(name, startDate, endDate, uPhotometry, vPhotometry, bPhotometry):
 try:
     cnx = pyodbc.connect('Driver={SQL Server};Server=DESKTOP-4UP85UJ\SQLEXPRESS;Database=astro;Trusted_Connection=yes;uid=DESKTOP-4UP85UJ\Przemek;pwd=')
     #cnx = pyodbc.connect('Driver={SQL Server};Server=GPLPL0041\SQLEXPRESS;Database=Astro;Trusted_Connection=yes;uid=GFT\pwji;pwd=')
     cursor = cnx.cursor()

     get_lastId = ("select top 1 id from stg.StagingObservations order by id desc")
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

     insert_observation = ("Insert into stg.stagingObservations (id, RowId, StarName, StartDate, EndDate, uPhotometry, uPhotometryTime, vPhotometry, vPhotometryTime, bPhotometry, bPhotometryTime, Status, Active) "
                           "values ("+lastId+", 1, '"+name+"', '"+startDate+"', '"+endDate+"', '0.259254028383', '2721.7367', '0.259254028383', '2721.7367', '0.259254028383', '2721.7367', 'new', 1)")

     print insert_observation

     cursor.execute(insert_observation)
     cnx.commit()

     cursor.close()

 except:
   print 'errors'
 else:
   cnx.close()


#---------------------------------------------Update existing observation----------------------------------------------
def updateObservation(id, name, startDate, endDate, uPhotometry, vPhotometry, bPhotometry):
    try:
        cnx = pyodbc.connect('Driver={SQL Server};Server=DESKTOP-4UP85UJ\SQLEXPRESS;Database=astro;Trusted_Connection=yes;uid=DESKTOP-4UP85UJ\Przemek;pwd=')
        #cnx = pyodbc.connect('Driver={SQL Server};Server=GPLPL0041\SQLEXPRESS;Database=Astro;Trusted_Connection=yes;uid=GFT\pwji;pwd=')
        cursor = cnx.cursor()


        id = str(id)
        name = str(name)
        startDate = str(startDate)
        endDate = str(endDate)
        uPhotometry = str(uPhotometry)
        vPhotometry = str(vPhotometry)
        bPhotometry = str(bPhotometry)

        update_observation = ("Update stg.stagingObservations set starName='"+name+"', startDate='"+startDate+"', endDate='"+endDate+"', uPhotometry='0.259254028383', uPhotometryTime='2721.7367',"
                              "vPhotometry='0.259254028383', vPhotometryTime='2721.7367', bPhotometry='0.259254028383', bPhotometryTime='2721.7367', Status='new', active=1 where id="+id+"")

        print update_observation

        cursor.execute(update_observation)
        cnx.commit()

        cursor.close()

    except:
        print 'errors'
    else:
        cnx.close()