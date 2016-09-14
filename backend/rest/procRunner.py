import sys
import pyodbc
import os
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('../resources/env.properties')
dbAddress = config.get('DatabaseConnection', 'database.address');
queries = ConfigParser.RawConfigParser()
queries.read('../resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()

reload(sys)
sys.setdefaultencoding('utf8')

#--------------------------------------run DB bi.observationsDelta procedure--------------------------------------------
def procRunner():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()


        get_Ids = (queries.get('DatabaseQueries', 'database.getIdsFromStagingObservations'))
        getIds = fetch_all(get_Ids)

        for i in getIds:
           i=str(i)
           runObservationsDelta = (queries.get('DatabaseQueries', 'database.runObservationsDelta')+i)
           cursor.execute(runObservationsDelta)
           cnx.commit()

        Log = False
        while(Log != True):
            get_Log = (queries.get('DatabaseQueries', 'database.getLogFromLog')+i+" order by id desc")
            Log = str(fetch_one(get_Log))
            if(Log):
                break
            else:
                continue
        cursor.close()
    except:
        print 'errors in procRunner function'
    else:
        cnx.close()

#--------------------------------------run DB bi.observationsDeltaPersonalized procedure--------------------------------
def procPersonalizedRunner(email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        email = str(email)


        get_Ids = (queries.get('DatabaseQueries', 'database.getPersonalizedIdsFromStagingObservations') + "'" + email + "' order by id desc")
        getIds = fetch_all(get_Ids)

        for i in getIds:
            i=str(i)
            runObservationsDelta = (queries.get('DatabaseQueries', 'database.runObservationsDeltaPersonalized')+i)
            cursor.execute(runObservationsDelta)
            cnx.commit()

        Log = False
        while(Log != True):
            get_Log = (queries.get('DatabaseQueries', 'database.getLogFromLog')+i+" order by id desc")
            Log = str(fetch_one(get_Log))
            if(Log):
                break
            else:
                continue
        cursor.close()
    except:
        print 'errors in procRunner function'
    else:
        cnx.close()

#--------------------------------------------------------Remove Observation---------------------------------------------
def deleteObservation(id):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        id=str(id)
        removeObservation = (queries.get('DatabaseQueries', 'database.removeObservation')+id)
        cursor.execute(removeObservation)
        cnx.commit()
        cursor.close()

    except:
        print 'errors in deleteObservation function'
    else:
        cnx.close()

#-----------------------------------------------------------------------------------------------------------------------
def fetch_one(get_value):
    cursor.execute(get_value)
    Value = cursor.fetchone()
    Value = Value[0]
    return Value

def fetch_all(get_value):
    cursor.execute(get_value)
    Value = cursor.fetchall()
    Value = [oc[0] for oc in Value]
    return Value