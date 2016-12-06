import simplejson as json
import pyodbc
import ast
import ConfigParser
import time
from flask import Flask, jsonify

config = ConfigParser.RawConfigParser()
config.read('../resources/env.properties')
dbAddress = config.get('DatabaseConnection', 'database.address');
queries = ConfigParser.RawConfigParser()
queries.read('../resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()

#-------------------------------------------table-list observations data------------------------------------------------
def json_data():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_IdFromObservationsSorted = queries.get('DatabaseQueries', 'database.getIdFromObservationsSorted');
        getIds = fetch_all(get_IdFromObservationsSorted)

        i = 0
        controller = ''
        if(len(getIds) != 0):
           for counter in getIds:
               id = str(counter)
               i = i + 1
               get_observationsOwners = (queries.get('DatabaseQueries', 'database.getObservationsOwners') + id)
               get_objectName = (queries.get('DatabaseQueries', 'database.getStarNameFromObservationsSorted') + id)
               get_StartDate = (queries.get('DatabaseQueries', 'database.getStartDateFromObservationsSorted') + id)
               get_EndDate = (queries.get('DatabaseQueries', 'database.getEndDateFromObservationsSorted') + id)
               get_UPhotometryFlag = (queries.get('DatabaseQueries', 'database.getUPhotometryFlagFromUPhotometrySorted') + id)
               get_UPhotometryFlux = (queries.get('DatabaseQueries', 'database.getUPhotometryFluxFromUPhotometrySorted') + id)
               get_UPhotometryTime = (queries.get('DatabaseQueries', 'database.getUPhotometryTimeFromUPhotometrySorted') + id)
               get_VPhotometryFlag = (queries.get('DatabaseQueries', 'database.getVPhotometryFlagFromVPhotometrySorted') + id)
               get_VPhotometryFlux = (queries.get('DatabaseQueries', 'database.getVPhotometryFluxFromVPhotometrySorted') + id)
               get_VPhotometryTime = (queries.get('DatabaseQueries', 'database.getVPhotometryTimeFromVPhotometrySorted') + id)
               get_BPhotometryFlag = (queries.get('DatabaseQueries', 'database.getBPhotometryFlagFromBPhotometrySorted') + id)
               get_BPhotometryFlux = (queries.get('DatabaseQueries', 'database.getBPhotometryFluxFromBPhotometrySorted') + id)
               get_BPhotometryTime = (queries.get('DatabaseQueries', 'database.getBPhotometryTimeFromBPhotometrySorted') + id)
               get_RPhotometryFlag = (queries.get('DatabaseQueries', 'database.getRPhotometryFlagFromRPhotometrySorted') + id)
               get_RPhotometryFlux = (queries.get('DatabaseQueries', 'database.getRPhotometryFluxFromRPhotometrySorted') + id)
               get_RPhotometryTime = (queries.get('DatabaseQueries', 'database.getRPhotometryTimeFromRPhotometrySorted') + id)
               get_IPhotometryFlag = (queries.get('DatabaseQueries', 'database.getIPhotometryFlagFromIPhotometrySorted') + id)
               get_IPhotometryFlux = (queries.get('DatabaseQueries', 'database.getIPhotometryFluxFromIPhotometrySorted') + id)
               get_IPhotometryTime = (queries.get('DatabaseQueries', 'database.getIPhotometryTimeFromIPhotometrySorted') + id)

               UPhotometry = str(fetch_one(get_UPhotometryFlag))
               if UPhotometry != 'null' and UPhotometry != '0':
                   UPhotometry = 'YES'
                   UPhotometryFlux = fetch_all_replace(get_UPhotometryFlux)
                   UPhotometryTime = fetch_all_replace(get_UPhotometryTime)
               else:
                   UPhotometry = 'NO'
                   UPhotometryFlux = 'No data available'
                   UPhotometryTime = 'No data available'

               VPhotometry = str(fetch_one(get_VPhotometryFlag))
               if VPhotometry != 'null' and VPhotometry != '0':
                   VPhotometry = 'YES'
                   VPhotometryFlux = fetch_all_replace(get_VPhotometryFlux)
                   VPhotometryTime = fetch_all_replace(get_VPhotometryTime)
               else:
                   VPhotometry = 'NO'
                   VPhotometryFlux = 'No data available'
                   VPhotometryTime = 'No data available'

               BPhotometry = str(fetch_one(get_BPhotometryFlag))
               if BPhotometry != 'null' and BPhotometry != '0':
                   BPhotometry = 'YES'
                   BPhotometryFlux = fetch_all_replace(get_BPhotometryFlux)
                   BPhotometryTime = fetch_all_replace(get_BPhotometryTime)
               else:
                   BPhotometry = 'NO'
                   BPhotometryFlux = 'No data available'
                   BPhotometryTime = 'No data available'

               RPhotometry = str(fetch_one(get_RPhotometryFlag))
               if RPhotometry != 'null' and RPhotometry != '0':
                   RPhotometry = 'YES'
                   RPhotometryFlux = fetch_all_replace(get_RPhotometryFlux)
                   RPhotometryTime = fetch_all_replace(get_RPhotometryTime)
               else:
                   RPhotometry = 'NO'
                   RPhotometryFlux = 'No data available'
                   RPhotometryTime = 'No data available'

               IPhotometry = str(fetch_one(get_IPhotometryFlag))
               if IPhotometry != 'null' and IPhotometry != '0':
                   IPhotometry = 'YES'
                   IPhotometryFlux = fetch_all_replace(get_IPhotometryFlux)
                   IPhotometryTime = fetch_all_replace(get_IPhotometryTime)
               else:
                   IPhotometry = 'NO'
                   IPhotometryFlux = 'No data available'
                   IPhotometryTime = 'No data available'

               object = {'id': id, 'name': str(fetch_one(get_objectName)), 'startDate': str(fetch_one(get_StartDate)), 'endDate': str(fetch_one(get_EndDate)),
                         'uPhotometry': UPhotometry, 'uPhotometryFlux': UPhotometryFlux, 'uPhotometryTime': UPhotometryTime,
                         'vPhotometry': VPhotometry, 'vPhotometryFlux': VPhotometryFlux, 'vPhotometryTime': VPhotometryTime,
                         'bPhotometry': BPhotometry, 'bPhotometryFlux': BPhotometryFlux, 'bPhotometryTime': BPhotometryTime,
                         'rPhotometry': RPhotometry, 'rPhotometryFlux': RPhotometryFlux, 'rPhotometryTime': RPhotometryTime,
                         'iPhotometry': IPhotometry, 'iPhotometryFlux': IPhotometryFlux, 'iPhotometryTime': IPhotometryTime, 'owner': str(fetch_one(get_observationsOwners))}

               controller = str(object) + ',' + controller

           controller = ast.literal_eval(controller[:-1])
           #controller = json.dumps(controller, skipkeys=True)

        cursor.close()
        if(i==1):
           observations = [controller]
        elif(i>1):
           observations = controller
        else:
           observations = [{'id': 'No Data', 'name': 'No Data', 'startDate': 'No Data', 'endDate': 'No Data',
                           'uPhotometry': '', 'uPhotometryFlux': '', 'uPhotometryTime': '',
                           'vPhotometry': '', 'vPhotometryFlux': '', 'vPhotometryTime': '',
                           'bPhotometry': '', 'bPhotometryFlux': '', 'bPhotometryTime': '',
                           'rPhotometry': '', 'rPhotometryFlux': '', 'rPhotometryTime': '',
                           'iPhotometry': '', 'iPhotometryFlux': '', 'iPhotometryTime': '', 'owner': 'No Data'}]

        json_data.jsonData = observations

    except:
        print 'errors json_data function'
    else:
        cnx.close()

#---------------------------------------------personal observations data------------------------------------------------
def userObservations(email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)

        getIds = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserIdFromObservationsSorted')), (email)).fetchall()]

        i = 0
        controller = ''
        for counter in getIds:
            id = str(counter)
            i = i + 1
            get_observationsOwners = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserObservationsOwners'), (id, email)).fetchone())[0]
            get_objectName = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserStarNameFromObservationsSorted'), (id, email)).fetchone())[0]
            get_objectType = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserObjectTypeFromObservationsSorted'), (id, email)).fetchone())[0]
            get_objectVerified = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserObjectVerifiedFromObservationsSorted'), (id, email)).fetchone())[0]
            get_StartDate = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserStartDateFromObservationsSorted'), (id, email)).fetchone())[0]
            get_EndDate = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserEndDateFromObservationsSorted'), (id, email)).fetchone())[0]
            get_statuses = (cursor.execute(queries.get('DatabaseQueries', 'database.getPersonalObservationsStatuses'), (id, email)).fetchone())[0]

            UPhotometry = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserUPhotometryFlagFromUPhotometrySorted'), (id, email)).fetchone())[0]
            if str(UPhotometry) != 'null' and str(UPhotometry) != '0':
                UPhotometry = 'YES'
                UPhotometryFlux = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserUPhotometryFluxFromUPhotometrySorted')), (id, email)).fetchall()])
                UPhotometryTime = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserUPhotometryTimeFromUPhotometrySorted')), (id, email)).fetchall()])
            else:
                UPhotometry = 'NO'
                UPhotometryFlux = 'No data available'
                UPhotometryTime = 'No data available'

            VPhotometry = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserVPhotometryFlagFromVPhotometrySorted'), (id, email)).fetchone())[0]
            if str(VPhotometry) != 'null' and str(VPhotometry) != '0':
                VPhotometry = 'YES'
                VPhotometryFlux = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserVPhotometryFluxFromVPhotometrySorted')), (id, email)).fetchall()])
                VPhotometryTime = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserVPhotometryTimeFromVPhotometrySorted')), (id, email)).fetchall()])
            else:
                VPhotometry = 'NO'
                VPhotometryFlux = 'No data available'
                VPhotometryTime = 'No data available'

            BPhotometry = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserBPhotometryFlagFromBPhotometrySorted'), (id, email)).fetchone())[0]
            if str(BPhotometry) != 'null' and str(BPhotometry) != '0':
                BPhotometry = 'YES'
                BPhotometryFlux = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserBPhotometryFluxFromBPhotometrySorted')), (id, email)).fetchall()])
                BPhotometryTime = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserBPhotometryTimeFromBPhotometrySorted')), (id, email)).fetchall()])
            else:
                BPhotometry = 'NO'
                BPhotometryFlux = 'No data available'
                BPhotometryTime = 'No data available'

            RPhotometry = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserRPhotometryFlagFromRPhotometrySorted'), (id, email)).fetchone())[0]
            if str(RPhotometry) != 'null' and str(RPhotometry) != '0':
                RPhotometry = 'YES'
                RPhotometryFlux = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserRPhotometryFluxFromRPhotometrySorted')), (id, email)).fetchall()])
                RPhotometryTime = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserRPhotometryTimeFromRPhotometrySorted')), (id, email)).fetchall()])
            else:
                RPhotometry = 'NO'
                RPhotometryFlux = 'No data available'
                RPhotometryTime = 'No data available'

            IPhotometry = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserIPhotometryFlagFromIPhotometrySorted'), (id, email)).fetchone())[0]
            if str(IPhotometry) != 'null' and str(IPhotometry) != '0':
                IPhotometry = 'YES'
                IPhotometryFlux = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserIPhotometryFluxFromIPhotometrySorted')), (id, email)).fetchall()])
                IPhotometryTime = replace([oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserIPhotometryTimeFromIPhotometrySorted')), (id, email)).fetchall()])
            else:
                IPhotometry = 'NO'
                IPhotometryFlux = 'No data available'
                IPhotometryTime = 'No data available'

            object = {'id': id, 'name': get_objectName, 'startDate': str(get_StartDate), 'endDate': str(get_EndDate),
                      'uPhotometry': UPhotometry, 'uPhotometryFlux': UPhotometryFlux, 'uPhotometryTime': UPhotometryTime,
                      'vPhotometry': VPhotometry, 'vPhotometryFlux': VPhotometryFlux, 'vPhotometryTime': VPhotometryTime,
                      'bPhotometry': BPhotometry, 'bPhotometryFlux': BPhotometryFlux, 'bPhotometryTime': BPhotometryTime,
                      'rPhotometry': RPhotometry, 'rPhotometryFlux': RPhotometryFlux, 'rPhotometryTime': RPhotometryTime,
                      'iPhotometry': IPhotometry, 'iPhotometryFlux': IPhotometryFlux, 'iPhotometryTime': IPhotometryTime,
                      'owner': get_observationsOwners, 'status': get_statuses,
                      'objectType': get_objectType, 'objectVerified': str(get_objectVerified)}

            controller = str(object) + ',' + controller

        controller = ast.literal_eval(controller[:-1])

        cursor.close()
        #case with one observation to produce array of object
        if(i==1):
            observations = [controller]
        else:
            observations = controller
        return observations

    except:
        print 'errors userObservations function'
    else:
        cnx.close()

#------------------------------------------------------Admin Panel data-------------------------------------------------
def json_load():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_LastLoadObservationId = (queries.get('DatabaseQueries', 'database.getLastLoadObservationIdFromStagingObservations'))
        get_LastLoadStarName = (queries.get('DatabaseQueries', 'database.getLastLoadStarNameFromStagingObservations'))
        get_LastLoadStartDate = (queries.get('DatabaseQueries', 'database.getLastLoadStartDateFromStagingObservations'))
        get_LastLoadEndDate = (queries.get('DatabaseQueries', 'database.getLastLoadEndDateFromStagingObservations'))

        flag = fetch_all(get_LastLoadObservationId)
        if(len(flag) != 0):
           lastLoad = [{'observationId': fetch_one(get_LastLoadObservationId), 'starName': fetch_one(get_LastLoadStarName),
                     'startDate': fetch_one(get_LastLoadStartDate), 'endDate': fetch_one(get_LastLoadEndDate)}]
        else:
            lastLoad = [{'observationId': '', 'starName': '', 'startDate': '', 'endDate': ''}]

        cursor.close()
        json_load.jsonLastLoad = lastLoad

    except:
        print 'errors json_load function'
    else:
        cnx.close()

#-----------------------------------------------------HR Diagram Range--------------------------------------------------
def json_hrDiagramRange():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        #B-V
        get_XMax = (queries.get('DatabaseQueries', 'database.getXMaxFromBVDiagramAvg'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getXMinFromBVDiagramAvg'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getYMaxFromVPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getYMinFromVPhotometrySorted'))
        json_hrDiagramRange.jsonBVDiagramRange = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]

        #U-B
        get_XMax = (queries.get('DatabaseQueries', 'database.getXMaxFromUBDiagramAvg'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getXMinFromUBDiagramAvg'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getYMaxFromBPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getYMinFromBPhotometrySorted'))
        json_hrDiagramRange.jsonUBDiagramRange = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]

        #R-I
        get_XMax = (queries.get('DatabaseQueries', 'database.getXMaxFromRIDiagramAvg'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getXMinFromRIDiagramAvg'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getYMaxFromIPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getYMinFromIPhotometrySorted'))
        json_hrDiagramRange.jsonRIDiagramRange = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]

        #V-I
        get_XMax = (queries.get('DatabaseQueries', 'database.getXMaxFromVIDiagramAvg'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getXMinFromVIDiagramAvg'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getYMaxFromIPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getYMinFromIPhotometrySorted'))
        json_hrDiagramRange.jsonVIDiagramRange = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]

        cursor.close()

    except:
        print 'errors json_hrDiagramRange function'
    else:
        cnx.close()

#--------------------------------------------------------HR Diagram data------------------------------------------------
def json_hrdiagram():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        #B-V
        get_VObservations = (queries.get('DatabaseQueries', 'database.getJoinedVObservationsFromVPhotometrySorted'))
        get_BVObservationsDifference = (queries.get('DatabaseQueries', 'database.getBVObservationsDifferenceFromBVDiagramAvg'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getStarNamesFromBVDiagramAvg'))
        json_hrdiagram.jsonBVDiagram = [{'bvObservationsDifference': fetch_all(get_BVObservationsDifference), 'vObservations': fetch_all(get_VObservations), 'starNames': fetch_all(get_StarNames)}]

        #U-B
        get_BObservations = (queries.get('DatabaseQueries', 'database.getJoinedBObservationsFromBPhotometrySorted'))
        get_UBObservationsDifference = (queries.get('DatabaseQueries', 'database.getUBObservationsDifferenceFromUBDiagramAvg'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getStarNamesFromUBDiagramAvg'))
        json_hrdiagram.jsonUBDiagram = [{'ubObservationsDifference': fetch_all(get_UBObservationsDifference), 'bObservations': fetch_all(get_BObservations), 'starNames': fetch_all(get_StarNames)}]

        #R-I
        get_IObservations = (queries.get('DatabaseQueries', 'database.getJoinedIForRIObservationsFromIPhotometrySorted'))
        get_RIObservationsDifference = (queries.get('DatabaseQueries', 'database.getRIObservationsDifferenceFromRIDiagramAvg'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getStarNamesFromRIDiagramAvg'))
        json_hrdiagram.jsonRIDiagram = [{'riObservationsDifference': fetch_all(get_RIObservationsDifference), 'iObservations': fetch_all(get_IObservations), 'starNames': fetch_all(get_StarNames)}]

        #V-I
        get_IObservations = (queries.get('DatabaseQueries', 'database.getJoinedIForVIObservationsFromIPhotometrySorted'))
        get_VIObservationsDifference = (queries.get('DatabaseQueries', 'database.getVIObservationsDifferenceFromVIDiagramAvg'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getStarNamesFromVIDiagramAvg'))
        json_hrdiagram.jsonVIDiagram = [{'viObservationsDifference': fetch_all(get_VIObservationsDifference), 'iObservations': fetch_all(get_IObservations), 'starNames': fetch_all(get_StarNames)}]

        cursor.close()

    except:
        print 'errors in json_hrdiagram function'
    else:
        cnx.close()


#-----------------------------------------------Personalized HR Diagram Range-------------------------------------------
def personalizedObservationsHRDiagramRange(hrDiagramType, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        hrDiagramType = str(hrDiagramType)
        email = str(email)
        #B-V
        if(hrDiagramType == 'B-V'):
           get_XMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMaxFromBVDiagramAvg'), (email)).fetchone())[0]
           get_XMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMinFromBVDiagramAvg'), (email)).fetchone())[0]
           get_YMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMaxFromVPhotometrySorted'), (email)).fetchone())[0]
           get_YMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMinFromVPhotometrySorted'), (email)).fetchone())[0]
           verify_hrDataRange(get_XMax, get_XMin, get_YMax, get_YMin)
           data = [{'XMax': get_XMax, 'XMin': get_XMin, 'YMax': get_YMax, 'YMin': get_YMin}]
        #U-B
        elif(hrDiagramType == 'U-B'):
           get_XMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMaxFromUBDiagramAvg'), (email)).fetchone())[0]
           get_XMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMinFromUBDiagramAvg'), (email)).fetchone())[0]
           get_YMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMaxFromBPhotometrySorted'), (email)).fetchone())[0]
           get_YMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMinFromBPhotometrySorted'), (email)).fetchone())[0]
           verify_hrDataRange(get_XMax, get_XMin, get_YMax, get_YMin)
           data = [{'XMax': get_XMax, 'XMin': get_XMin, 'YMax': get_YMax, 'YMin': get_YMin}]
        #R-I
        elif(hrDiagramType == 'R-I'):
           get_XMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMaxFromRIDiagramAvg'), (email)).fetchone())[0]
           get_XMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMinFromRIDiagramAvg'), (email)).fetchone())[0]
           get_YMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMaxFromIPhotometrySorted'), (email)).fetchone())[0]
           get_YMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMinFromIPhotometrySorted'), (email)).fetchone())[0]
           verify_hrDataRange(get_XMax, get_XMin, get_YMax, get_YMin)
           data = [{'XMax': get_XMax, 'XMin': get_XMin, 'YMax': get_YMax, 'YMin': get_YMin}]
        #V-I
        elif(hrDiagramType == 'V-I'):
           get_XMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMaxFromVIDiagramAvg'), (email)).fetchone())[0]
           get_XMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserXMinFromVIDiagramAvg'), (email)).fetchone())[0]
           get_YMax = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMaxFromIPhotometrySorted'), (email)).fetchone())[0]
           get_YMin = (cursor.execute(queries.get('DatabaseQueries', 'database.getUserYMinFromIPhotometrySorted'), (email)).fetchone())[0]
           verify_hrDataRange(get_XMax, get_XMin, get_YMax, get_YMin)
           data = [{'XMax': get_XMax, 'XMin': get_XMin, 'YMax': get_YMax, 'YMin': get_YMin}]

        return data
        cursor.close()

    except:
        print 'errors personalizedObservationsHRDiagramRange function'
    else:
        cnx.close()


#-------------------------------------------Personalized HR Diagram data------------------------------------------------
def personalizedObservationsHRDiagram(hrDiagramType, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        hrDiagramType = str(hrDiagramType)
        email = str(email)

        time.sleep(1)
        #B-V
        if(hrDiagramType == 'B-V'):
           get_VObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getJoinedUserVObservationsFromVPhotometrySorted')), (email)).fetchall()]
           get_BVObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserBVObservationsDifferenceFromBVDiagramAvg')), (email)).fetchall()]
           get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserStarNamesFromBVDiagramAvg')), (email)).fetchall()]
           verify_hrData(get_VObservations, get_BVObservationsDifference, get_StarNames)
           data = [{'abvObservationsDifference': get_BVObservationsDifference, 'cvObservations': get_VObservations, 'bstarNames': get_StarNames}]
        #U-B
        elif(hrDiagramType == 'U-B'):
           get_BObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getJoinedUserBObservationsFromBPhotometrySorted')), (email)).fetchall()]
           get_UBObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserUBObservationsDifferenceFromUBDiagramAvg')), (email)).fetchall()]
           get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserStarNamesFromUBDiagramAvg')), (email)).fetchall()]
           verify_hrData(get_BObservations, get_UBObservationsDifference, get_StarNames)
           data = [{'aubObservationsDifference': get_UBObservationsDifference, 'cbObservations': get_BObservations, 'bstarNames': get_StarNames}]
        #R-I
        elif(hrDiagramType == 'R-I'):
           get_IObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getJoinedUserIForRIObservationsFromIPhotometrySorted')), (email)).fetchall()]
           get_RIObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserRIObservationsDifferenceFromRIDiagramAvg')), (email)).fetchall()]
           get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserStarNamesFromRIDiagramAvg')), (email)).fetchall()]
           verify_hrData(get_IObservations, get_RIObservationsDifference, get_StarNames)
           data = [{'ariObservationsDifference': get_RIObservationsDifference, 'ciObservations': get_IObservations, 'bstarNames': get_StarNames}]
        #V-I
        elif(hrDiagramType == 'V-I'):
           get_IObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getJoinedUserIForVIObservationsFromIPhotometrySorted')), (email)).fetchall()]
           get_VIObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserVIObservationsDifferenceFromVIDiagramAvg')), (email)).fetchall()]
           get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserStarNamesFromVIDiagramAvg')), (email)).fetchall()]
           verify_hrData(get_IObservations, get_VIObservationsDifference, get_StarNames)
           data = [{'aviObservationsDifference': get_VIObservationsDifference, 'ciObservations': get_IObservations, 'bstarNames': get_StarNames}]

        return data
        cursor.close()

    except:
        print 'errors in personalizedObservationsHRDiagram function'
    else:
        cnx.close()

#---------------------------------------------------LC Diagram range----------------------------------------------------
def json_lcDiagramRange():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        #U
        get_XMax = (queries.get('DatabaseQueries', 'database.getLCXMaxFromUPhotometrySorted'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getLCXMinFromUPhotometrySorted'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getLCYMaxFromUPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getLCYMinFromUPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getLCStarNamesFromUPhotometrySorted'))
        json_lcDiagramRange.jsonLCUDiagramRange = [{'StarNames': fetch_all(get_StarNames), 'XMax': fetch_all(get_XMax), 'XMin': fetch_all(get_XMin), 'YMax': fetch_all(get_YMax), 'YMin': fetch_all(get_YMin)}]

        #V
        get_XMax = (queries.get('DatabaseQueries', 'database.getLCXMaxFromVPhotometrySorted'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getLCXMinFromVPhotometrySorted'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getLCYMaxFromVPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getLCYMinFromVPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getLCStarNamesFromVPhotometrySorted'))
        json_lcDiagramRange.jsonLCVDiagramRange = [{'StarNames': fetch_all(get_StarNames), 'XMax': fetch_all(get_XMax), 'XMin': fetch_all(get_XMin), 'YMax': fetch_all(get_YMax), 'YMin': fetch_all(get_YMin)}]

        #B
        get_XMax = (queries.get('DatabaseQueries', 'database.getLCXMaxFromBPhotometrySorted'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getLCXMinFromBPhotometrySorted'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getLCYMaxFromBPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getLCYMinFromBPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getLCStarNamesFromBPhotometrySorted'))
        json_lcDiagramRange.jsonLCBDiagramRange = [{'StarNames': fetch_all(get_StarNames), 'XMax': fetch_all(get_XMax), 'XMin': fetch_all(get_XMin), 'YMax': fetch_all(get_YMax), 'YMin': fetch_all(get_YMin)}]

        #R
        get_XMax = (queries.get('DatabaseQueries', 'database.getLCXMaxFromRPhotometrySorted'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getLCXMinFromRPhotometrySorted'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getLCYMaxFromRPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getLCYMinFromRPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getLCStarNamesFromRPhotometrySorted'))
        json_lcDiagramRange.jsonLCRDiagramRange = [{'StarNames': fetch_all(get_StarNames), 'XMax': fetch_all(get_XMax), 'XMin': fetch_all(get_XMin), 'YMax': fetch_all(get_YMax), 'YMin': fetch_all(get_YMin)}]

        #I
        get_XMax = (queries.get('DatabaseQueries', 'database.getLCXMaxFromIPhotometrySorted'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getLCXMinFromIPhotometrySorted'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getLCYMaxFromIPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getLCYMinFromIPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getLCStarNamesFromIPhotometrySorted'))
        json_lcDiagramRange.jsonLCIDiagramRange = [{'StarNames': fetch_all(get_StarNames), 'XMax': fetch_all(get_XMax), 'XMin': fetch_all(get_XMin), 'YMax': fetch_all(get_YMax), 'YMin': fetch_all(get_YMin)}]

        cursor.close()

    except:
        print 'errors json_lcDiagramRange function'
    else:
        cnx.close()

#------------------------------------------------------LC Diagram data--------------------------------------------------
def json_lcDiagram():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        #U
        get_UObservations = (queries.get('DatabaseQueries', 'database.getAllLCObservationsFromUPhotometrySorted'))
        get_UTimes = (queries.get('DatabaseQueries', 'database.getAllLCTimesFromUPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getAllLCStarNamesFromUPhotometrySorted'))
        json_lcDiagram.jsonLCUDiagram = [{'starNames': fetch_all(get_StarNames), 'uObservations': fetch_all(get_UObservations), 'uTimes': fetch_all(get_UTimes)}]

        #V
        get_VObservations = (queries.get('DatabaseQueries', 'database.getAllLCObservationsFromVPhotometrySorted'))
        get_VTimes = (queries.get('DatabaseQueries', 'database.getAllLCTimesFromVPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getAllLCStarNamesFromVPhotometrySorted'))
        json_lcDiagram.jsonLCVDiagram = [{'starNames': fetch_all(get_StarNames), 'vObservations': fetch_all(get_VObservations), 'vTimes': fetch_all(get_VTimes)}]

        #B
        get_BObservations = (queries.get('DatabaseQueries', 'database.getAllLCObservationsFromBPhotometrySorted'))
        get_BTimes = (queries.get('DatabaseQueries', 'database.getAllLCTimesFromBPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getAllLCStarNamesFromBPhotometrySorted'))
        json_lcDiagram.jsonLCBDiagram = [{'starNames': fetch_all(get_StarNames), 'bObservations': fetch_all(get_BObservations), 'bTimes': fetch_all(get_BTimes)}]

        #R
        get_RObservations = (queries.get('DatabaseQueries', 'database.getAllLCObservationsFromRPhotometrySorted'))
        get_RTimes = (queries.get('DatabaseQueries', 'database.getAllLCTimesFromRPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getAllLCStarNamesFromRPhotometrySorted'))
        json_lcDiagram.jsonLCRDiagram = [{'starNames': fetch_all(get_StarNames), 'rObservations': fetch_all(get_RObservations), 'rTimes': fetch_all(get_RTimes)}]

        #I
        get_IObservations = (queries.get('DatabaseQueries', 'database.getAllLCObservationsFromIPhotometrySorted'))
        get_ITimes = (queries.get('DatabaseQueries', 'database.getAllLCTimesFromIPhotometrySorted'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getAllLCStarNamesFromIPhotometrySorted'))
        json_lcDiagram.jsonLCIDiagram = [{'starNames': fetch_all(get_StarNames), 'iObservations': fetch_all(get_IObservations), 'iTimes': fetch_all(get_ITimes)}]

        cursor.close()

    except:
        print 'errors in json_lcDiagram function'
    else:
        cnx.close()


#-----------------------------------------------Personalized LC Diagram range-------------------------------------------
def personalizedLCDiagramRange(filter, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        filter = str(filter)
        email = str(email)

        #U
        if(filter == 'U'):
            get_XMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMaxFromUPhotometrySorted')), (email)).fetchall()]
            get_XMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMinFromUPhotometrySorted')), (email)).fetchall()]
            get_YMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMaxFromUPhotometrySorted')), (email)).fetchall()]
            get_YMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMinFromUPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromUPhotometrySorted')), (email)).fetchall()]
            data = [{'eStarNames': get_StarNames, 'aXMax': get_XMax, 'bXMin': get_XMin, 'cYMax': get_YMax, 'dYMin': get_YMin}]
        #V
        elif(filter == 'V'):
            get_XMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMaxFromVPhotometrySorted')), (email)).fetchall()]
            get_XMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMinFromVPhotometrySorted')), (email)).fetchall()]
            get_YMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMaxFromVPhotometrySorted')), (email)).fetchall()]
            get_YMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMinFromVPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromVPhotometrySorted')), (email)).fetchall()]
            data = [{'eStarNames': get_StarNames, 'aXMax': get_XMax, 'bXMin': get_XMin, 'cYMax': get_YMax, 'dYMin': get_YMin}]
        #B
        elif(filter == 'B'):
            get_XMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMaxFromBPhotometrySorted')), (email)).fetchall()]
            get_XMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMinFromBPhotometrySorted')), (email)).fetchall()]
            get_YMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMaxFromBPhotometrySorted')), (email)).fetchall()]
            get_YMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMinFromBPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromBPhotometrySorted')), (email)).fetchall()]
            data = [{'eStarNames': get_StarNames, 'aXMax': get_XMax, 'bXMin': get_XMin, 'cYMax': get_YMax, 'dYMin': get_YMin}]
        #R
        elif(filter == 'R'):
            get_XMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMaxFromRPhotometrySorted')), (email)).fetchall()]
            get_XMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMinFromRPhotometrySorted')), (email)).fetchall()]
            get_YMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMaxFromRPhotometrySorted')), (email)).fetchall()]
            get_YMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMinFromRPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromRPhotometrySorted')), (email)).fetchall()]
            data = [{'eStarNames': get_StarNames, 'aXMax': get_XMax, 'bXMin': get_XMin, 'cYMax': get_YMax, 'dYMin': get_YMin}]
        #I
        elif(filter == 'I'):
            get_XMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMaxFromIPhotometrySorted')), (email)).fetchall()]
            get_XMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCXMinFromIPhotometrySorted')), (email)).fetchall()]
            get_YMax = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMaxFromIPhotometrySorted')), (email)).fetchall()]
            get_YMin = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCYMinFromIPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromIPhotometrySorted')), (email)).fetchall()]
            data = [{'eStarNames': get_StarNames, 'aXMax': get_XMax, 'bXMin': get_XMin, 'cYMax': get_YMax, 'dYMin': get_YMin}]

        return data
        cursor.close()

    except:
        print 'errors personalizedLCDiagramRange function'
    else:
        cnx.close()


#--------------------------------------------Personalized LC Diagram data-----------------------------------------------
def personalizedLCDiagram(filter, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        filter = str(filter)
        email = str(email)

        time.sleep(1)
        #U
        if(filter == 'U'):
            get_UObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromUPhotometrySorted')), (email)).fetchall()]
            get_UTimes = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromUPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromUPhotometrySorted')), (email)).fetchall()]
            data = [{'cstarNames': get_StarNames, 'auObservations': get_UObservations, 'buTimes': get_UTimes}]
        #V
        elif(filter == 'V'):
            get_VObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromVPhotometrySorted')), (email)).fetchall()]
            get_VTimes = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromVPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromVPhotometrySorted')), (email)).fetchall()]
            data = [{'cstarNames': get_StarNames, 'avObservations': get_VObservations, 'bvTimes': get_VTimes}]
        #B
        elif(filter == 'B'):
            get_BObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromBPhotometrySorted')), (email)).fetchall()]
            get_BTimes = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromBPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromBPhotometrySorted')), (email)).fetchall()]
            data = [{'cstarNames': get_StarNames, 'abObservations': get_BObservations, 'bbTimes': get_BTimes}]
        #R
        elif(filter == 'R'):
            get_RObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromRPhotometrySorted')), (email)).fetchall()]
            get_RTimes = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromRPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromRPhotometrySorted')), (email)).fetchall()]
            data = [{'cstarNames': get_StarNames, 'arObservations': get_RObservations, 'brTimes': get_RTimes}]
        #I
        elif(filter == 'I'):
            get_IObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromIPhotometrySorted')), (email)).fetchall()]
            get_ITimes = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromIPhotometrySorted')), (email)).fetchall()]
            get_StarNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromIPhotometrySorted')), (email)).fetchall()]
            data = [{'cstarNames': get_StarNames, 'aiObservations': get_IObservations, 'biTimes': get_ITimes}]

        return data
        cursor.close()

    except:
        print 'errors in personalizedLCDiagram function'
    else:
        cnx.close()

#------------------------------------------------------Carousel Statistics----------------------------------------------
def json_statistics():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_NumberOfUsers = (queries.get('DatabaseQueries', 'database.getNumberOfUsers'))
        get_NumberOfFiles = (queries.get('DatabaseQueries', 'database.getNumberOfFiles'))
        get_NumberOfObjects = (queries.get('DatabaseQueries', 'database.getNumberOfObjects'))

        NumberOfUsers = fetch_one(get_NumberOfUsers)
        NumberOfFiles = fetch_one(get_NumberOfFiles)
        NumberOfObjects = fetch_one(get_NumberOfObjects)

        time.sleep(0.5)
        statistics = [{'numberOfUsers': NumberOfUsers, 'numberOfFiles': NumberOfFiles,
                                  'numberOfObjects': NumberOfObjects}]
        cursor.close()
        json_statistics.jsonStatistics = statistics

    except:
        print 'errors in json_hrdiagram function'
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


def fetch_all_replace(get_value):
    cursor.execute(get_value)
    Value = cursor.fetchall()
    Value = [u[0] for u in Value]
    Value = ans = ' '.join(Value).replace(' ', '\n')
    return Value

def replace(Value):
    Value = ans = ' '.join(Value).replace(' ', '\n')
    return Value

def verify_hrDataRange(get_XMax, get_XMin, get_YMax, get_YMin):
    looper=1
    while(looper<100):
        time.sleep(0.1)
        if (get_XMax != 'None' and get_XMin != 'None' and get_YMax != 'None' and get_YMin != 'None'):
            break
        else:
            looper = looper + 1
            continue

def verify_hrData(get_FilterObservations, get_FiltersObservationsDifference, get_StarNames):
    looper=1
    while(looper<100):
        time.sleep(0.1)
        if (get_FilterObservations != 'None' and get_FiltersObservationsDifference != 'None' and get_StarNames != 'None'):
            break
        else:
            looper = looper + 1
            continue