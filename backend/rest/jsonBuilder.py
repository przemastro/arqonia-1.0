import simplejson as json
import pyodbc
import ast
import ConfigParser
import time

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

        controller = ''
        for counter in getIds:
            id = str(counter)
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
            get_IPhotometryFlux = ( queries.get('DatabaseQueries', 'database.getIPhotometryFluxFromIPhotometrySorted') + id)
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
        controller = json.dumps(controller, skipkeys=True)

        cursor.close()
        json_string = json.loads(controller)
        json_data.jsonData = json_string

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

        get_IdFromObservationsSorted = (queries.get('DatabaseQueries', 'database.getUserIdFromObservationsSorted') + "'" + email + "' order by os.id desc");
        getIds = fetch_all(get_IdFromObservationsSorted)

        controller = ''
        for counter in getIds:
            id = str(counter)
            get_observationsOwners = (queries.get('DatabaseQueries', 'database.getUserObservationsOwners') + id + " and us.Email='" + email + "'")
            get_objectName = (queries.get('DatabaseQueries', 'database.getUserStarNameFromObservationsSorted') + id + " and us.Email='" + email + "'")
            get_StartDate = (queries.get('DatabaseQueries', 'database.getUserStartDateFromObservationsSorted') + id + " and us.Email='" + email + "'")
            get_EndDate = (queries.get('DatabaseQueries', 'database.getUserEndDateFromObservationsSorted') + id + " and us.Email='" + email + "'")
            get_UPhotometryFlag = (queries.get('DatabaseQueries', 'database.getUserUPhotometryFlagFromUPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_UPhotometryFlux = (queries.get('DatabaseQueries', 'database.getUserUPhotometryFluxFromUPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_UPhotometryTime = (queries.get('DatabaseQueries', 'database.getUserUPhotometryTimeFromUPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_VPhotometryFlag = (queries.get('DatabaseQueries', 'database.getUserVPhotometryFlagFromVPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_VPhotometryFlux = (queries.get('DatabaseQueries', 'database.getUserVPhotometryFluxFromVPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_VPhotometryTime = (queries.get('DatabaseQueries', 'database.getUserVPhotometryTimeFromVPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_BPhotometryFlag = (queries.get('DatabaseQueries', 'database.getUserBPhotometryFlagFromBPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_BPhotometryFlux = (queries.get('DatabaseQueries', 'database.getUserBPhotometryFluxFromBPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_BPhotometryTime = (queries.get('DatabaseQueries', 'database.getUserBPhotometryTimeFromBPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_RPhotometryFlag = (queries.get('DatabaseQueries', 'database.getUserRPhotometryFlagFromRPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_RPhotometryFlux = (queries.get('DatabaseQueries', 'database.getUserRPhotometryFluxFromRPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_RPhotometryTime = (queries.get('DatabaseQueries', 'database.getUserRPhotometryTimeFromRPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_IPhotometryFlag = (queries.get('DatabaseQueries', 'database.getUserIPhotometryFlagFromIPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_IPhotometryFlux = (queries.get('DatabaseQueries', 'database.getUserIPhotometryFluxFromIPhotometrySorted') + id + " and us.Email='" + email + "'")
            get_IPhotometryTime = (queries.get('DatabaseQueries', 'database.getUserIPhotometryTimeFromIPhotometrySorted') + id + " and us.Email='" + email + "'")

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
            print controller

        controller = ast.literal_eval(controller[:-1])
        controller = json.dumps(controller, skipkeys=True)

        cursor.close()
        observations = json.loads(controller)
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

        lastLoad = [{'observationId': fetch_one(get_LastLoadObservationId), 'starName': fetch_one(get_LastLoadStarName),
                     'startDate': fetch_one(get_LastLoadStartDate), 'endDate': fetch_one(get_LastLoadEndDate)}]

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


#------------------------------------------------HR User Diagram Range--------------------------------------------------
def personalizedObservationsHRDiagramRange(hrDiagramType, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        hrDiagramType = str(hrDiagramType)
        email = str(email)
        #B-V
        if(hrDiagramType == 'B-V'):
           get_XMax = (queries.get('DatabaseQueries', 'database.getUserXMaxFromBVDiagramAvg') + "'" + email + "'")
           get_XMin = (queries.get('DatabaseQueries', 'database.getUserXMinFromBVDiagramAvg') + "'" + email + "'")
           get_YMax = (queries.get('DatabaseQueries', 'database.getUserYMaxFromVPhotometrySorted') + "'" + email + "'")
           get_YMin = (queries.get('DatabaseQueries', 'database.getUserYMinFromVPhotometrySorted') + "'" + email + "'")
           time.sleep(1)
           data = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]
        #U-B
        elif(hrDiagramType == 'U-B'):
           get_XMax = (queries.get('DatabaseQueries', 'database.getUserXMaxFromUBDiagramAvg') + "'" + email + "'")
           get_XMin = (queries.get('DatabaseQueries', 'database.getUserXMinFromUBDiagramAvg') + "'" + email + "'")
           get_YMax = (queries.get('DatabaseQueries', 'database.getUserYMaxFromBPhotometrySorted') + "'" + email + "'")
           get_YMin = (queries.get('DatabaseQueries', 'database.getUserYMinFromBPhotometrySorted') + "'" + email + "'")
           time.sleep(1)
           data = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]
        #R-I
        elif(hrDiagramType == 'R-I'):
           get_XMax = (queries.get('DatabaseQueries', 'database.getUserXMaxFromRIDiagramAvg') + "'" + email + "'")
           get_XMin = (queries.get('DatabaseQueries', 'database.getUserXMinFromRIDiagramAvg') + "'" + email + "'")
           get_YMax = (queries.get('DatabaseQueries', 'database.getUserYMaxFromIPhotometrySorted') + "'" + email + "'")
           get_YMin = (queries.get('DatabaseQueries', 'database.getUserYMinFromIPhotometrySorted') + "'" + email + "'")
           time.sleep(1)
           data = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]
        #V-I
        elif(hrDiagramType == 'V-I'):
           get_XMax = (queries.get('DatabaseQueries', 'database.getUserXMaxFromVIDiagramAvg') + "'" + email + "'")
           get_XMin = (queries.get('DatabaseQueries', 'database.getUserXMinFromVIDiagramAvg') + "'" + email + "'")
           get_YMax = (queries.get('DatabaseQueries', 'database.getUserYMaxFromIPhotometrySorted') + "'" + email + "'")
           get_YMin = (queries.get('DatabaseQueries', 'database.getUserYMinFromIPhotometrySorted') + "'" + email + "'")
           time.sleep(1)
           data = [{'XMax': fetch_one(get_XMax), 'XMin': fetch_one(get_XMin), 'YMax': fetch_one(get_YMax), 'YMin': fetch_one(get_YMin)}]

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
        print hrDiagramType

        #B-V
        if(hrDiagramType == 'B-V'):
           get_VObservations = (queries.get('DatabaseQueries', 'database.getJoinedUserVObservationsFromVPhotometrySorted') + "'" + email + "' group by so.ObjectName")
           get_BVObservationsDifference = (queries.get('DatabaseQueries', 'database.getUserBVObservationsDifferenceFromBVDiagramAvg') + "'" + email + "'")
           get_StarNames = (queries.get('DatabaseQueries', 'database.getUserStarNamesFromBVDiagramAvg') + "'" + email + "'")
           #time.sleep(1)
           data = [{'abvObservationsDifference': fetch_all(get_BVObservationsDifference), 'cvObservations': fetch_all(get_VObservations), 'bstarNames': fetch_all(get_StarNames)}]
        #U-B
        elif(hrDiagramType == 'U-B'):
           get_BObservations = (queries.get('DatabaseQueries', 'database.getJoinedUserBObservationsFromBPhotometrySorted') + "'" + email + "' group by so.ObjectName")
           get_UBObservationsDifference = (queries.get('DatabaseQueries', 'database.getUserUBObservationsDifferenceFromUBDiagramAvg') + "'" + email + "'")
           get_StarNames = (queries.get('DatabaseQueries', 'database.getUserStarNamesFromUBDiagramAvg') + "'" + email + "'")
           data = [{'aubObservationsDifference': fetch_all(get_UBObservationsDifference), 'cbObservations': fetch_all(get_BObservations), 'bstarNames': fetch_all(get_StarNames)}]
        #R-I
        elif(hrDiagramType == 'R-I'):
           get_IObservations = (queries.get('DatabaseQueries', 'database.getJoinedUserIForRIObservationsFromIPhotometrySorted') + "'" + email + "' group by so.ObjectName")
           get_RIObservationsDifference = (queries.get('DatabaseQueries', 'database.getUserRIObservationsDifferenceFromRIDiagramAvg') + "'" + email + "'")
           get_StarNames = (queries.get('DatabaseQueries', 'database.getUserStarNamesFromRIDiagramAvg') + "'" + email + "'")
           data = [{'ariObservationsDifference': fetch_all(get_RIObservationsDifference), 'ciObservations': fetch_all(get_IObservations), 'bstarNames': fetch_all(get_StarNames)}]
        #V-I
        elif(hrDiagramType == 'V-I'):
           get_IObservations = (queries.get('DatabaseQueries', 'database.getJoinedUserIForVIObservationsFromIPhotometrySorted') + "'" + email + "' group by so.ObjectName")
           get_VIObservationsDifference = (queries.get('DatabaseQueries', 'database.getUserVIObservationsDifferenceFromVIDiagramAvg') + "'" + email + "'")
           get_StarNames = (queries.get('DatabaseQueries', 'database.getUserStarNamesFromVIDiagramAvg') + "'" + email + "'")
           data = [{'aviObservationsDifference': fetch_all(get_VIObservationsDifference), 'ciObservations': fetch_all(get_IObservations), 'bstarNames': fetch_all(get_StarNames)}]

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
            get_XMax = (queries.get('DatabaseQueries', 'database.getUserLCXMaxFromUPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            print get_XMax
            get_XMin = (queries.get('DatabaseQueries', 'database.getUserLCXMinFromUPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMax = (queries.get('DatabaseQueries', 'database.getUserLCYMaxFromUPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMin = (queries.get('DatabaseQueries', 'database.getUserLCYMinFromUPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromUPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            time.sleep(1)
            data = [{'eStarNames': fetch_all(get_StarNames), 'aXMax': fetch_all(get_XMax), 'bXMin': fetch_all(get_XMin), 'cYMax': fetch_all(get_YMax), 'dYMin': fetch_all(get_YMin)}]
            print data
        #V
        elif(filter == 'V'):
            get_XMax = (queries.get('DatabaseQueries', 'database.getUserLCXMaxFromVPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_XMin = (queries.get('DatabaseQueries', 'database.getUserLCXMinFromVPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMax = (queries.get('DatabaseQueries', 'database.getUserLCYMaxFromVPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMin = (queries.get('DatabaseQueries', 'database.getUserLCYMinFromVPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromVPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            time.sleep(1)
            data = [{'eStarNames': fetch_all(get_StarNames), 'aXMax': fetch_all(get_XMax), 'bXMin': fetch_all(get_XMin), 'cYMax': fetch_all(get_YMax), 'dYMin': fetch_all(get_YMin)}]
            print data
        #B
        elif(filter == 'B'):
            get_XMax = (queries.get('DatabaseQueries', 'database.getUserLCXMaxFromBPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_XMin = (queries.get('DatabaseQueries', 'database.getUserLCXMinFromBPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMax = (queries.get('DatabaseQueries', 'database.getUserLCYMaxFromBPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMin = (queries.get('DatabaseQueries', 'database.getUserLCYMinFromBPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromBPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            time.sleep(1)
            data = [{'eStarNames': fetch_all(get_StarNames), 'aXMax': fetch_all(get_XMax), 'bXMin': fetch_all(get_XMin), 'cYMax': fetch_all(get_YMax), 'dYMin': fetch_all(get_YMin)}]
        #R
        elif(filter == 'R'):
            get_XMax = (queries.get('DatabaseQueries', 'database.getUserLCXMaxFromRPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_XMin = (queries.get('DatabaseQueries', 'database.getUserLCXMinFromRPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMax = (queries.get('DatabaseQueries', 'database.getUserLCYMaxFromRPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMin = (queries.get('DatabaseQueries', 'database.getUserLCYMinFromRPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromRPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            time.sleep(1)
            data = [{'eStarNames': fetch_all(get_StarNames), 'aXMax': fetch_all(get_XMax), 'bXMin': fetch_all(get_XMin), 'cYMax': fetch_all(get_YMax), 'dYMin': fetch_all(get_YMin)}]
        #I
        elif(filter == 'I'):
            get_XMax = (queries.get('DatabaseQueries', 'database.getUserLCXMaxFromIPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_XMin = (queries.get('DatabaseQueries', 'database.getUserLCXMinFromIPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMax = (queries.get('DatabaseQueries', 'database.getUserLCYMaxFromIPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_YMin = (queries.get('DatabaseQueries', 'database.getUserLCYMinFromIPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserLCStarNamesFromIPhotometrySorted') + "'" + email + "' group by ObjectName order by ObjectName asc")
            time.sleep(1)
            data = [{'eStarNames': fetch_all(get_StarNames), 'aXMax': fetch_all(get_XMax), 'bXMin': fetch_all(get_XMin), 'cYMax': fetch_all(get_YMax), 'dYMin': fetch_all(get_YMin)}]

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

        #U
        if(filter == 'U'):
            get_UObservations = (queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromUPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_UTimes = (queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromUPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromUPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            data = [{'cstarNames': fetch_all(get_StarNames), 'auObservations': fetch_all(get_UObservations), 'buTimes': fetch_all(get_UTimes)}]
        #V
        elif(filter == 'V'):
            get_VObservations = (queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromVPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_VTimes = (queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromVPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromVPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            data = [{'cstarNames': fetch_all(get_StarNames), 'avObservations': fetch_all(get_VObservations), 'bvTimes': fetch_all(get_VTimes)}]
        #B
        elif(filter == 'B'):
            get_BObservations = (queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromBPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_BTimes = (queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromBPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromBPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            data = [{'cstarNames': fetch_all(get_StarNames), 'abObservations': fetch_all(get_BObservations), 'bbTimes': fetch_all(get_BTimes)}]
        #R
        elif(filter == 'R'):
            get_RObservations = (queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromRPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_RTimes = (queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromRPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromRPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            data = [{'cstarNames': fetch_all(get_StarNames), 'arObservations': fetch_all(get_RObservations), 'brTimes': fetch_all(get_RTimes)}]
        #I
        elif(filter == 'I'):
            get_IObservations = (queries.get('DatabaseQueries', 'database.getUserAllLCObservationsFromIPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_ITimes = (queries.get('DatabaseQueries', 'database.getUserAllLCTimesFromIPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            get_StarNames = (queries.get('DatabaseQueries', 'database.getUserAllLCStarNamesFromIPhotometrySorted') + "'" + email + "' order by ObjectName asc")
            data = [{'cstarNames': fetch_all(get_StarNames), 'aiObservations': fetch_all(get_IObservations), 'biTimes': fetch_all(get_ITimes)}]

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
