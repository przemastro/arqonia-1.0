import simplejson as json
import pyodbc
import ast
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('../resources/ConfigFile.properties')
dbAddress = config.get('DatabaseConnection', 'database.address');
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()


def json_data():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_IdFromObservationsSorted = config.get('DatabaseQueries', 'database.getIdFromObservationsSorted');
        getIds = fetch_all(get_IdFromObservationsSorted)

        controller = ''

        for counter in getIds:
            id = str(counter)
            get_objectName = (config.get('DatabaseQueries', 'database.getStarNameFromObservationsSorted') + id)
            get_StartDate = (config.get('DatabaseQueries', 'database.getStartDateFromObservationsSorted') + id)
            get_EndDate = (config.get('DatabaseQueries', 'database.getEndDateFromObservationsSorted') + id)
            get_UPhotometryFlag = (
            config.get('DatabaseQueries', 'database.getUPhotometryFlagFromUPhotometrySorted') + id)
            get_UPhotometryFlux = (
            config.get('DatabaseQueries', 'database.getUPhotometryFluxFromUPhotometrySorted') + id)
            get_UPhotometryTime = (
            config.get('DatabaseQueries', 'database.getUPhotometryTimeFromUPhotometrySorted') + id)
            get_VPhotometryFlag = (
            config.get('DatabaseQueries', 'database.getVPhotometryFlagFromVPhotometrySorted') + id)
            get_VPhotometryFlux = (
            config.get('DatabaseQueries', 'database.getVPhotometryFluxFromVPhotometrySorted') + id)
            get_VPhotometryTime = (
            config.get('DatabaseQueries', 'database.getVPhotometryTimeFromVPhotometrySorted') + id)
            get_BPhotometryFlag = (
            config.get('DatabaseQueries', 'database.getBPhotometryFlagFromBPhotometrySorted') + id)
            get_BPhotometryFlux = (
            config.get('DatabaseQueries', 'database.getBPhotometryFluxFromBPhotometrySorted') + id)
            get_BPhotometryTime = (
            config.get('DatabaseQueries', 'database.getBPhotometryTimeFromBPhotometrySorted') + id)

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

            object = {'id': id, 'name': objectName, 'startDate': StartDate, 'endDate': EndDate,
                      'uPhotometry': UPhotometry, 'uPhotometryFlux': UPhotometryFlux,
                      'uPhotometryTime': UPhotometryTime,
                      'vPhotometry': VPhotometry, 'vPhotometryFlux': VPhotometryFlux,
                      'vPhotometryTime': VPhotometryTime,
                      'bPhotometry': BPhotometry, 'bPhotometryFlux': BPhotometryFlux,
                      'bPhotometryTime': BPhotometryTime}

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
        config.get('DatabaseQueries', 'database.getLastLoadObservationIdFromStagingObservations'))
        get_LastLoadStarName = (config.get('DatabaseQueries', 'database.getLastLoadStarNameFromStagingObservations'))
        get_LastLoadStartDate = (config.get('DatabaseQueries', 'database.getLastLoadStartDateFromStagingObservations'))
        get_LastLoadEndDate = (config.get('DatabaseQueries', 'database.getLastLoadEndDateFromStagingObservations'))

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

        get_ObservationsDates = (config.get('DatabaseQueries', 'database.getObservationsDatesFromObservationsSorted'))
        get_ObservationsCounts = (config.get('DatabaseQueries', 'database.getObservationsCountsFromObservationsSorted'))

        ObservationsCounts = fetch_all(get_ObservationsCounts)
        ObservationsDates = fetch_all(get_ObservationsDates)

        observationsDiagram = [{'data': ObservationsCounts, 'dates': ObservationsDates}]

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

        get_VObservations = (config.get('DatabaseQueries', 'database.getVObservationsFromVPhotometrySorted'))
        get_BVObservationsDifference = (
        config.get('DatabaseQueries', 'database.getBVObservationsDifferenceFromHrDiagramAvg'))
        get_StarNames = (config.get('DatabaseQueries', 'database.getStarNamesFromHrDiagramAvg'))

        get_XMax = (config.get('DatabaseQueries', 'database.getXMaxFromHrDiagramAvg'))
        get_XMin = (config.get('DatabaseQueries', 'database.getXMinFromHrDiagramAvg'))
        get_YMax = (config.get('DatabaseQueries', 'database.getYMaxFromVPhotometrySorted'))
        get_YMin = (config.get('DatabaseQueries', 'database.getYMinFromVPhotometrySorted'))

        VObservations = fetch_all(get_VObservations)
        BVObservationsDifference = fetch_all(get_BVObservationsDifference)
        StarNames = fetch_all(get_StarNames)

        XMax = fetch_one(get_XMax)
        XMin = fetch_one(get_XMin)
        YMax = fetch_one(get_YMax)
        YMin = fetch_one(get_YMin)

        observationsHRDiagram = [{'bvObservationsDifference': BVObservationsDifference, 'vObservations': VObservations,
                                  'starNames': StarNames,
                                  'XMax': XMax, 'XMin': XMin, 'YMax': YMax, 'YMin': YMin}]

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
