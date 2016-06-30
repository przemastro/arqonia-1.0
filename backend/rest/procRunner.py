import sys
import pyodbc
import os
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('../resources/ConfigFile.properties')
dbAddress = config.get('DatabaseSection', 'database.address');

reload(sys)
sys.setdefaultencoding('utf8')

#-----------------------------------------------Process data in Staging Table-------------------------------------------
def procRunner():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_Ids = ("select distinct(Id) from stg.StagingObservations where (status='new' and active=1) or (status='deleted' and active=1) order by id desc")
        cursor.execute(get_Ids)
        getIds = cursor.fetchall()
        getIds = [g[0] for g in getIds]

        for i in getIds:
           i=str(i)
           runObservationsDelta = ("exec bi.observationsDelta @observationId="+i)
           cursor.execute(runObservationsDelta)
           cnx.commit()

        Log = False
        while(Log != True):
            get_Log = ("select LastLoad from log.log where ObservationId="+i+" and Message='Completed'")
            cursor.execute(get_Log)
            Log = cursor.fetchone()
            Log = str(Log[0])
            if(Log):
                fn = open('api.py', 'a')
                fn.write(" ")
                fn.seek(-1, os.SEEK_END)
                fn.truncate()
                fn.close()
                break
            else:
                continue


        cursor.close()

    except:
        print 'errors'
    else:
        cnx.close()


#--------------------------------------------------soft delete observation----------------------------------------------
def deleteObservation(id):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        id=str(id)
        removeObservation = ("update stg.stagingObservations set active=1, status='deleted' where id="+id)
        cursor.execute(removeObservation)
        cnx.commit()


        cursor.close()

    except:
        print 'errors'
    else:
        cnx.close()