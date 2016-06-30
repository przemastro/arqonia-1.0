import simplejson as json
import pyodbc
import ast
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read('../resources/ConfigFile.properties')
dbAddress = config.get('DatabaseSection', 'database.address');
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()


def json_data():
    try:
        config = ConfigParser.RawConfigParser()
        config.read('../resources/ConfigFile.properties')
        dbAddress = config.get('DatabaseSection', 'database.address');
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()


        getIdFromObservationsSorted = config.get('DatabaseSection', 'database.getIdFromObservationsSorted');
        get_Ids = (getIdFromObservationsSorted)
        cursor.execute(get_Ids)
        getIds = cursor.fetchall()
        getIds = [g[0] for g in getIds]

        controller = ''

        for counter in getIds:
            id=str(counter)
            get_objectName = (config.get('DatabaseSection', 'database.getStarNameFromObservationsSorted')+id)
            get_StartDate = (config.get('DatabaseSection', 'database.getStartDateFromObservationsSorted')+id)
            get_EndDate = (config.get('DatabaseSection', 'database.getEndDateFromObservationsSorted')+id)
            get_UPhotometryFlag = (config.get('DatabaseSection', 'database.getUPhotometryFlagFromUPhotometrySorted')+id)
            get_UPhotometryFlux = (config.get('DatabaseSection', 'database.getUPhotometryFluxFromUPhotometrySorted')+id)
            get_UPhotometryTime = (config.get('DatabaseSection', 'database.getUPhotometryTimeFromUPhotometrySorted')+id)
            get_VPhotometryFlag = (config.get('DatabaseSection', 'database.getVPhotometryFlagFromVPhotometrySorted')+id)
            get_VPhotometryFlux = (config.get('DatabaseSection', 'database.getVPhotometryFluxFromVPhotometrySorted')+id)
            get_VPhotometryTime = (config.get('DatabaseSection', 'database.getVPhotometryTimeFromVPhotometrySorted')+id)
            get_BPhotometryFlag = (config.get('DatabaseSection', 'database.getBPhotometryFlagFromBPhotometrySorted')+id)
            get_BPhotometryFlux = (config.get('DatabaseSection', 'database.getBPhotometryFluxFromBPhotometrySorted')+id)
            get_BPhotometryTime = (config.get('DatabaseSection', 'database.getBPhotometryTimeFromBPhotometrySorted')+id)

            cursor.execute(get_objectName)
            objectName = cursor.fetchone()
            objectName = objectName[0]

            cursor.execute(get_StartDate)
            StartDate = cursor.fetchone()
            StartDate = str(StartDate[0])

            cursor.execute(get_EndDate)
            EndDate = cursor.fetchone()
            EndDate = str(EndDate[0])

            cursor.execute(get_UPhotometryFlag)
            UPhotometry = cursor.fetchone()
            UPhotometry = str(UPhotometry[0])
            if UPhotometry != 'null' and UPhotometry != '0':
                UPhotometry = 'YES'
            else:
                UPhotometry = 'NO'

            if UPhotometry == 'YES':
                cursor.execute(get_UPhotometryFlux)
                UPhotometryFlux = cursor.fetchall()
                UPhotometryFlux = [u[0] for u in UPhotometryFlux]
                UPhotometryFlux = ans = ' '.join(UPhotometryFlux).replace(' ', '\n')

                cursor.execute(get_UPhotometryTime)
                UPhotometryTime = cursor.fetchall()
                UPhotometryTime = [u[0] for u in UPhotometryTime]
                UPhotometryTime = ans = ' '.join(UPhotometryTime).replace(' ', '\n')
            else:
                UPhotometryFlux = 'No data available'
                UPhotometryTime = 'No data available'


            cursor.execute(get_VPhotometryFlag)
            VPhotometry = cursor.fetchone()
            VPhotometry = str(VPhotometry[0])
            if VPhotometry != 'null' and VPhotometry != '0':
                VPhotometry = 'YES'
            else:
                VPhotometry = 'NO'

            if VPhotometry == 'YES':
                cursor.execute(get_VPhotometryFlux)
                VPhotometryFlux = cursor.fetchall()
                VPhotometryFlux = [v[0] for v in VPhotometryFlux]
                VPhotometryFlux = ans = ' '.join(VPhotometryFlux).replace(' ', '\n')

                cursor.execute(get_VPhotometryTime)
                VPhotometryTime = cursor.fetchall()
                VPhotometryTime = [v[0] for v in VPhotometryTime]
                VPhotometryTime = ans = ' '.join(VPhotometryTime).replace(' ', '\n')
            else:
                VPhotometryFlux = 'No data available'
                VPhotometryTime = 'No data available'


            cursor.execute(get_BPhotometryFlag)
            BPhotometry = cursor.fetchone()
            BPhotometry = str(BPhotometry[0])
            if BPhotometry != 'null' and BPhotometry != '0':
                BPhotometry = 'YES'
            else:
                BPhotometry = 'NO'

            if BPhotometry == 'YES':
                cursor.execute(get_BPhotometryFlux)
                BPhotometryFlux = cursor.fetchall()
                BPhotometryFlux = [b[0] for b in BPhotometryFlux]
                BPhotometryFlux = ans = ' '.join(BPhotometryFlux).replace(' ', '\n')

                cursor.execute(get_BPhotometryTime)
                BPhotometryTime = cursor.fetchall()
                BPhotometryTime = [b[0] for b in BPhotometryTime]
                BPhotometryTime = ans = ' '.join(BPhotometryTime).replace(' ', '\n')
            else:
                BPhotometryFlux = 'No data available'
                BPhotometryTime = 'No data available'

            object = {'id': id, 'name': objectName, 'startDate': StartDate,
                      'endDate': EndDate,
                      'uPhotometry': UPhotometry, 'uPhotometryFlux': UPhotometryFlux, 'uPhotometryTime': UPhotometryTime,
                      'vPhotometry': VPhotometry, 'vPhotometryFlux': VPhotometryFlux, 'vPhotometryTime': VPhotometryTime,
                      'bPhotometry': BPhotometry, 'bPhotometryFlux': BPhotometryFlux, 'bPhotometryTime': BPhotometryTime}

            controller = str(object) + ',' + controller

        controller = controller[:-1]
        controller = ast.literal_eval(controller)
        controller = json.dumps(controller, skipkeys=True)

        json_string = json.loads(controller)
        json_data.jsonData = json_string

    except:
        print 'errors json_data function'
    else:
        cnx.close()


#------------------------------------------------get last Processed data------------------------------------------------
def json_load():
    try:
        config = ConfigParser.RawConfigParser()
        config.read('../resources/ConfigFile.properties')
        dbAddress = config.get('DatabaseSection', 'database.address');
        cnx = pyodbc.connect(dbAddress)

        get_LastLoadObservationId = ("select distinct(lg.ObservationId) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")
        get_LastLoadStarName = ("select distinct(os.StarName) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")
        get_LastLoadStartDate = ("select distinct(cast(os.StartDate as varchar)) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")
        get_LastLoadEndDate = ("select distinct(cast(os.EndDate as varchar)) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")

        LastLoadObservationId = fetch_one(get_LastLoadObservationId)
        LastLoadStarName = fetch_one(get_LastLoadStarName)
        LastLoadStartDate = fetch_one(get_LastLoadStartDate)
        LastLoadEndDate = fetch_one(get_LastLoadEndDate)

        lastLoad = [{'observationId': LastLoadObservationId, 'starName': LastLoadStarName, 'startDate': LastLoadStartDate, 'endDate': LastLoadEndDate}]

        json_load.jsonLastLoad = lastLoad

    except:
        print 'errors json_load function'
    else:
        cnx.close()

#--------------------------------------------get Observations counts for Diagram----------------------------------------
def json_diagram():
    try:
        config = ConfigParser.RawConfigParser()
        config.read('../resources/ConfigFile.properties')
        dbAddress = config.get('DatabaseSection', 'database.address');
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_ObservationsDates = ("select cast(StartDate as varchar) from bi.observationsSorted group by StartDate order by CONVERT(DateTime, StartDate ,101) asc")
        get_ObservationsCounts = ("select count(distinct cast(id as varchar)) as data from bi.observationsSorted group by StartDate order by CONVERT(DateTime, StartDate ,101) asc")


        cursor.execute(get_ObservationsCounts)
        ObservationsCounts = cursor.fetchall()
        ObservationsCounts = [oc[0] for oc in ObservationsCounts]

        cursor.execute(get_ObservationsDates)
        ObservationsDates = cursor.fetchall()
        ObservationsDates = [od[0] for od in ObservationsDates]

        observationsDiagram = [{'data': ObservationsCounts, 'dates': ObservationsDates}]
        json_diagram.jsonDiagram = observationsDiagram

    except:
        print 'errors json_diagram function'
    else:
        cnx.close()

#------------------------------------------------get Observations for HR------------------------------------------------
def json_hrdiagram():
    try:
        config = ConfigParser.RawConfigParser()
        config.read('../resources/ConfigFile.properties')
        dbAddress = config.get('DatabaseSection', 'database.address');
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        get_VObservations = ("select cast(avg(cast(cast(rtrim(ltrim(vPhotometry)) as varchar(10)) as decimal(18,10))) as varchar) as vAverage from bi.vPhotometrySorted group by StarName")
        get_BVObservationsDifference = ("select BVDifference from bi.hrDiagramAvg")
        get_StarNames = ("select StarName from bi.hrDiagramAvg")

        get_XMax = ("select cast((max(cast(cast(rtrim(ltrim(BVDifference)) as varchar(10)) as decimal(18,10)))) as varchar) as bvDifferenceMax from bi.hrDiagramAvg")
        get_XMin = ("select cast((min(cast(cast(rtrim(ltrim(BVDifference)) as varchar(10)) as decimal(18,10)))) as varchar) as bvDifferenceMin from bi.hrDiagramAvg")
        get_YMax = ("select cast((max(cast(cast(rtrim(ltrim(vPhotometry)) as varchar(10)) as decimal(18,10)))) as varchar) as vPhotometryMax from bi.vPhotometrySorted")
        get_YMin = ("select cast((min(cast(cast(rtrim(ltrim(vPhotometry)) as varchar(10)) as decimal(18,10)))) as varchar) as vPhotometryMin from bi.vPhotometrySorted")


        cursor.execute(get_VObservations)
        VObservations = cursor.fetchall()
        VObservations = [oc[0] for oc in VObservations]

        cursor.execute(get_BVObservationsDifference)
        BVObservationsDifference = cursor.fetchall()
        BVObservationsDifference = [od[0] for od in BVObservationsDifference]

        cursor.execute(get_StarNames)
        StarNames = cursor.fetchall()
        StarNames = [od[0] for od in StarNames]

        XMax = fetch_one(get_XMax)
        XMin = fetch_one(get_XMin)
        YMax = fetch_one(get_YMax)
        YMin = fetch_one(get_YMin)

        observationsHRDiagram = [{'bvObservationsDifference': BVObservationsDifference, 'vObservations': VObservations, 'starNames': StarNames,
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
