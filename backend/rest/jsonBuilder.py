import simplejson as json
import pyodbc
import ast
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read('../resources/ConfigFile.properties')
dbAddress = config.get('DatabaseSection', 'database.address');

try:

    cnx = pyodbc.connect(dbAddress)
    cursor = cnx.cursor()


    get_Ids = ("select distinct(Id) from bi.observationsSorted order by id desc")
    cursor.execute(get_Ids)
    getIds = cursor.fetchall()
    getIds = [g[0] for g in getIds]
    print getIds

    controller = ''
    count = ''

    for counter in getIds:
       id=str(counter)
       print id
       get_objectName = ("select distinct(StarName) from bi.observationsSorted where id="+id)
       get_StartDate = ("select top 1 StartDate from bi.observationsSorted where id="+id)
       get_EndDate = ("select top 1 EndDate from bi.observationsSorted where id="+id)
       get_UPhotometryFlag = ("select count(1) from bi.uPhotometrySorted where id="+id)
       get_UPhotometryFlux = ("select uPhotometry from bi.uPhotometrySorted where id="+id)
       get_UPhotometryTime = ("select uPhotometryTime from bi.uPhotometrySorted where id="+id)
       get_VPhotometryFlag = ("select count(1) from bi.vPhotometrySorted where id="+id)
       get_VPhotometryFlux = ("select vPhotometry from bi.vPhotometrySorted where id="+id)
       get_VPhotometryTime = ("select vPhotometryTime from bi.vPhotometrySorted where id="+id)
       get_BPhotometryFlag = ("select count(1) from bi.bPhotometrySorted where id="+id)
       get_BPhotometryFlux = ("select bPhotometry from bi.bPhotometrySorted where id="+id)
       get_BPhotometryTime = ("select bPhotometryTime from bi.bPhotometrySorted where id="+id)

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
       if UPhotometry != 'null':
           UPhotometry = 'YES'
       else:
           UPhotometry = 'NO'

       cursor.execute(get_UPhotometryFlux)
       UPhotometryFlux = cursor.fetchall()
       UPhotometryFlux = [u[0] for u in UPhotometryFlux]
       UPhotometryFlux = ans = ' '.join(UPhotometryFlux).replace(' ', '\n')

       cursor.execute(get_UPhotometryTime)
       UPhotometryTime = cursor.fetchall()
       UPhotometryTime = [u[0] for u in UPhotometryTime]
       UPhotometryTime = ans = ' '.join(UPhotometryTime).replace(' ', '\n')

       cursor.execute(get_VPhotometryFlag)
       VPhotometry = cursor.fetchone()
       VPhotometry = str(VPhotometry[0])
       if VPhotometry != 'null':
          VPhotometry = 'YES'
       else:
          VPhotometry = 'NO'

       cursor.execute(get_VPhotometryFlux)
       VPhotometryFlux = cursor.fetchall()
       VPhotometryFlux = [v[0] for v in VPhotometryFlux]
       VPhotometryFlux = ans = ' '.join(VPhotometryFlux).replace(' ', '\n')

       cursor.execute(get_VPhotometryTime)
       VPhotometryTime = cursor.fetchall()
       VPhotometryTime = [v[0] for v in VPhotometryTime]
       VPhotometryTime = ans = ' '.join(VPhotometryTime).replace(' ', '\n')

       cursor.execute(get_BPhotometryFlag)
       BPhotometry = cursor.fetchone()
       BPhotometry = str(BPhotometry[0])
       if BPhotometry != 'null':
          BPhotometry = 'YES'
       else:
          BPhotometry = 'NO'

       cursor.execute(get_BPhotometryFlux)
       BPhotometryFlux = cursor.fetchall()
       BPhotometryFlux = [b[0] for b in BPhotometryFlux]
       BPhotometryFlux = ans = ' '.join(BPhotometryFlux).replace(' ', '\n')

       cursor.execute(get_BPhotometryTime)
       BPhotometryTime = cursor.fetchall()
       BPhotometryTime = [b[0] for b in BPhotometryTime]
       BPhotometryTime = ans = ' '.join(BPhotometryTime).replace(' ', '\n')

       object = {'id': id, 'name': objectName, 'startDate': StartDate,
                  'endDate': EndDate,
                  'uPhotometry': UPhotometry, 'uPhotometryFlux': UPhotometryFlux, 'uPhotometryTime': UPhotometryTime,
                  'vPhotometry': VPhotometry, 'vPhotometryFlux': VPhotometryFlux, 'vPhotometryTime': VPhotometryTime,
                  'bPhotometry': BPhotometry, 'bPhotometryFlux': BPhotometryFlux, 'bPhotometryTime': BPhotometryTime}

       controller = str(object) + ',' + controller

    controller = controller[:-1]
    controller = ast.literal_eval(controller)

    try:
       print 'Processing ...'
       #print json.dumps(controller, skipkeys=True)
    except (TypeError, ValueError) as err:
       print 'ERROR:', err
    controller = json.dumps(controller, skipkeys=True)

    json_string = json.dumps(controller, skipkeys=True, sort_keys=True, indent=2)
    json_string = json.loads(controller)


#------------------------------------------------get last Processed data------------------------------------------------

    get_LastLoadObservationId = ("select distinct(lg.ObservationId) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")
    get_LastLoadStarName = ("select distinct(os.StarName) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")
    get_LastLoadStartDate = ("select distinct(cast(os.StartDate as varchar)) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")
    get_LastLoadEndDate = ("select distinct(cast(os.EndDate as varchar)) from log.log lg join stg.stagingObservations os on lg.ObservationId=os.Id where lg.LastLoad=1")

    cursor.execute(get_LastLoadObservationId)
    LastLoadObservationId = cursor.fetchone()
    LastLoadObservationId = LastLoadObservationId[0]

    cursor.execute(get_LastLoadStarName)
    LastLoadStarName = cursor.fetchone()
    LastLoadStarName = LastLoadStarName[0]

    cursor.execute(get_LastLoadStartDate)
    LastLoadStartDate = cursor.fetchone()
    LastLoadStartDate = LastLoadStartDate[0]

    cursor.execute(get_LastLoadEndDate)
    LastLoadEndDate = cursor.fetchone()
    LastLoadEndDate = LastLoadEndDate[0]
    print LastLoadEndDate


    lastLoad = [{'observationId': LastLoadObservationId, 'starName': LastLoadStarName, 'startDate': LastLoadStartDate, 'endDate': LastLoadEndDate}]

    print lastLoad

#------------------------------------------------get Observations counts------------------------------------------------

    get_ObservationsDates = ("select cast(StartDate as varchar) from bi.observationsSorted group by StartDate order by CONVERT(DateTime, StartDate ,101) asc")
    get_ObservationsCounts = ("select count(distinct cast(id as varchar)) as data from bi.observationsSorted group by StartDate order by CONVERT(DateTime, StartDate ,101) asc")


    cursor.execute(get_ObservationsCounts)
    ObservationsCounts = cursor.fetchall()
    ObservationsCounts = [oc[0] for oc in ObservationsCounts]
    #ObservationsCounts = ', '.join(str(e) for e in ObservationsCounts)



    cursor.execute(get_ObservationsDates)
    ObservationsDates = cursor.fetchall()
    ObservationsDates = [od[0] for od in ObservationsDates]
    #ObservationsDates = ans = ', '.join(ObservationsDates)

    observationsDiagram = [{'data': ObservationsCounts, 'dates': ObservationsDates}]

    print observationsDiagram


#------------------------------------------------get Observations for HR------------------------------------------------

    get_BObservations = ("select cast(avg(cast(cast(rtrim(ltrim(bPhotometry)) as varchar(10)) as decimal(18,10))) as varchar) as bAverage from bi.bPhotometrySorted group by StarName")
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

    cursor.execute(get_XMax)
    XMax = cursor.fetchone()
    XMax = XMax[0]

    cursor.execute(get_XMin)
    XMin = cursor.fetchone()
    XMin = XMin[0]

    cursor.execute(get_YMax)
    YMax = cursor.fetchone()
    YMax = YMax[0]

    cursor.execute(get_YMin)
    YMin = cursor.fetchone()
    YMin = YMin[0]

    print StarNames


    observationsHRDiagram = [{'bvObservationsDifference': BVObservationsDifference, 'vObservations': VObservations, 'starNames': StarNames,
                              'XMax': XMax, 'XMin': XMin, 'YMax': YMax, 'YMin': YMin}]

    print observationsHRDiagram


    cursor.close()


except:
        print 'errors'
else:
    cnx.close()

def json_data():
    json_data.jsonData = json_string

def json_load():
    json_load.jsonLastLoad = lastLoad

def json_diagram():
    json_diagram.jsonDiagram = observationsDiagram

def json_hrdiagram():
    json_hrdiagram.jsonHRDiagram = observationsHRDiagram