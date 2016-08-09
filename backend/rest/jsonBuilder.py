import simplejson as json
import pyodbc
import ast
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('../resources/env.properties')
dbAddress = config.get('DatabaseConnection', 'database.address');
queries = ConfigParser.RawConfigParser()
queries.read('../resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()


def json_data():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_IdFromObservationsSorted = queries.get('DatabaseQueries', 'database.getIdFromObservationsSorted');
        getIds = fetch_all(get_IdFromObservationsSorted)

        controller = ''

        for counter in getIds:
            id = str(counter)
            get_objectName = (queries.get('DatabaseQueries', 'database.getStarNameFromObservationsSorted') + id)
            get_StartDate = (queries.get('DatabaseQueries', 'database.getStartDateFromObservationsSorted') + id)
            get_EndDate = (queries.get('DatabaseQueries', 'database.getEndDateFromObservationsSorted') + id)
            get_UPhotometryFlag = (
            queries.get('DatabaseQueries', 'database.getUPhotometryFlagFromUPhotometrySorted') + id)
            get_UPhotometryFlux = (
            queries.get('DatabaseQueries', 'database.getUPhotometryFluxFromUPhotometrySorted') + id)
            get_UPhotometryTime = (
            queries.get('DatabaseQueries', 'database.getUPhotometryTimeFromUPhotometrySorted') + id)
            get_VPhotometryFlag = (
            queries.get('DatabaseQueries', 'database.getVPhotometryFlagFromVPhotometrySorted') + id)
            get_VPhotometryFlux = (
            queries.get('DatabaseQueries', 'database.getVPhotometryFluxFromVPhotometrySorted') + id)
            get_VPhotometryTime = (
            queries.get('DatabaseQueries', 'database.getVPhotometryTimeFromVPhotometrySorted') + id)
            get_BPhotometryFlag = (
            queries.get('DatabaseQueries', 'database.getBPhotometryFlagFromBPhotometrySorted') + id)
            get_BPhotometryFlux = (
            queries.get('DatabaseQueries', 'database.getBPhotometryFluxFromBPhotometrySorted') + id)
            get_BPhotometryTime = (
            queries.get('DatabaseQueries', 'database.getBPhotometryTimeFromBPhotometrySorted') + id)
            get_RPhotometryFlag = (
            queries.get('DatabaseQueries', 'database.getRPhotometryFlagFromRPhotometrySorted') + id)
            get_RPhotometryFlux = (
            queries.get('DatabaseQueries', 'database.getRPhotometryFluxFromRPhotometrySorted') + id)
            get_RPhotometryTime = (
            queries.get('DatabaseQueries', 'database.getRPhotometryTimeFromRPhotometrySorted') + id)
            get_IPhotometryFlag = (
            queries.get('DatabaseQueries', 'database.getIPhotometryFlagFromIPhotometrySorted') + id)
            get_IPhotometryFlux = (
            queries.get('DatabaseQueries', 'database.getIPhotometryFluxFromIPhotometrySorted') + id)
            get_IPhotometryTime = (
            queries.get('DatabaseQueries', 'database.getIPhotometryTimeFromIPhotometrySorted') + id)

            objectName = str(fetch_one(get_objectName))
            StartDate = str(fetch_one(get_StartDate))
            EndDate = str(fetch_one(get_EndDate))

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

            object = {'id': id, 'name': objectName, 'startDate': StartDate, 'endDate': EndDate,
                      'uPhotometry': UPhotometry, 'uPhotometryFlux': UPhotometryFlux,
                      'uPhotometryTime': UPhotometryTime,
                      'vPhotometry': VPhotometry, 'vPhotometryFlux': VPhotometryFlux,
                      'vPhotometryTime': VPhotometryTime,
                      'bPhotometry': BPhotometry, 'bPhotometryFlux': BPhotometryFlux,
                      'bPhotometryTime': BPhotometryTime,
                      'rPhotometry': RPhotometry, 'rPhotometryFlux': RPhotometryFlux,
                      'rPhotometryTime': RPhotometryTime,
                      'iPhotometry': IPhotometry, 'iPhotometryFlux': IPhotometryFlux,
                      'iPhotometryTime': IPhotometryTime}

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


def json_load():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_LastLoadObservationId = (
        queries.get('DatabaseQueries', 'database.getLastLoadObservationIdFromStagingObservations'))
        get_LastLoadStarName = (queries.get('DatabaseQueries', 'database.getLastLoadStarNameFromStagingObservations'))
        get_LastLoadStartDate = (queries.get('DatabaseQueries', 'database.getLastLoadStartDateFromStagingObservations'))
        get_LastLoadEndDate = (queries.get('DatabaseQueries', 'database.getLastLoadEndDateFromStagingObservations'))

        LastLoadObservationId = fetch_one(get_LastLoadObservationId)
        LastLoadStarName = fetch_one(get_LastLoadStarName)
        LastLoadStartDate = fetch_one(get_LastLoadStartDate)
        LastLoadEndDate = fetch_one(get_LastLoadEndDate)

        lastLoad = [
            {'observationId': LastLoadObservationId, 'starName': LastLoadStarName, 'startDate': LastLoadStartDate,
             'endDate': LastLoadEndDate}]

        cursor.close()
        json_load.jsonLastLoad = lastLoad

    except:
        print 'errors json_load function'
    else:
        cnx.close()


def json_diagram():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_XMax = (queries.get('DatabaseQueries', 'database.getXMaxFromHrDiagramAvg'))
        get_XMin = (queries.get('DatabaseQueries', 'database.getXMinFromHrDiagramAvg'))
        get_YMax = (queries.get('DatabaseQueries', 'database.getYMaxFromVPhotometrySorted'))
        get_YMin = (queries.get('DatabaseQueries', 'database.getYMinFromVPhotometrySorted'))

        XMax = fetch_one(get_XMax)
        XMin = fetch_one(get_XMin)
        YMax = fetch_one(get_YMax)
        YMin = fetch_one(get_YMin)

        observationsDiagram = [{'XMax': XMax, 'XMin': XMin, 'YMax': YMax, 'YMin': YMin}]

        cursor.close()
        json_diagram.jsonDiagram = observationsDiagram

    except:
        print 'errors json_diagram function'
    else:
        cnx.close()


def json_hrdiagram():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_VObservations = (queries.get('DatabaseQueries', 'database.getVObservationsFromVPhotometrySorted'))
        get_BVObservationsDifference = (queries.get('DatabaseQueries', 'database.getBVObservationsDifferenceFromHrDiagramAvg'))
        get_StarNames = (queries.get('DatabaseQueries', 'database.getStarNamesFromHrDiagramAvg'))


        VObservations = fetch_all(get_VObservations)
        BVObservationsDifference = fetch_all(get_BVObservationsDifference)
        StarNames = fetch_all(get_StarNames)


        observationsHRDiagram = [{'bvObservationsDifference': BVObservationsDifference, 'vObservations': VObservations,
                                  'starNames': StarNames}]

        cursor.close()
        json_hrdiagram.jsonHRDiagram = observationsHRDiagram

    except:
        print 'errors in json_hrdiagram function'
    else:
        cnx.close()


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
