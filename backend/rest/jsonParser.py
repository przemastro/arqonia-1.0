import sys
import re
import pyodbc
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read('../resources/ConfigFile.properties')
dbAddress = config.get('DatabaseSection', 'database.address');

reload(sys)
sys.setdefaultencoding('utf8')

#-----------------------------------------insert new observation to tablelist-------------------------------------------
def json_parser(name, startDate, endDate, uPhotometry, vPhotometry, bPhotometry):
 try:
     cnx = pyodbc.connect(dbAddress)
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
     insert_observation = ''

     getIds = 3
     for counter in range(1,getIds):
        print counter
        if counter < getIds-1:
           counter = str(counter)
           observation = "SELECT "+lastId+","+counter+",'"+name+"','"+startDate+"','"+endDate+"',2720.81478,-6.68,2720.81478,-6.44,2720.81478,-6.14,'new',1 UNION ALL "
           insert_observation = insert_observation + observation
        else:
           counter = str(counter)
           observation = "SELECT "+lastId+","+counter+",'"+name+"','"+startDate+"','"+endDate+"',2720.81478,-6.68,2720.81478,-6.44,2720.81478,-6.14,'new',1"
           insert_observation = insert_observation + observation



     insert_observation = "SET NOCOUNT ON ;with cte (ID,RowId,StarName,StartDate,EndDate,uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime," \
                          "bPhotometry,Status,Active) as (" + insert_observation + ") INSERT INTO stg.stagingObservations (ID,RowId,StarName,StartDate,EndDate," \
                          "uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime,bPhotometry,Status,Active) select * from cte GO"

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
        cnx = pyodbc.connect(dbAddress)
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