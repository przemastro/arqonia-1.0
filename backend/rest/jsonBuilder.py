import simplejson as json
import pyodbc
import ast

try:

    #cnx = pyodbc.connect('Driver={SQL Server};Server=SAMSUNG-PC\SQLEXPRESS;Database=astro;Trusted_Connection=yes;uid=SAMSUNG-PC\SAMSUNG;pwd=')
    cnx = pyodbc.connect('Driver={SQL Server};Server=GPLPL0041\SQLEXPRESS;Database=Astro;Trusted_Connection=yes;uid=GFT\pwji;pwd=')
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
       get_objectName = ("select distinct(StarName) from bi.observationsSorted where id="+id)
       get_StartDate = ("select top 1 StartDate from bi.observationsSorted where id="+id)
       get_EndDate = ("select top 1 EndDate from bi.observationsSorted where id="+id)
       get_UPhotometry = ("select count(1) from bi.uPhotometrySorted where id="+id)
       get_VPhotometry = ("select count(1) from bi.vPhotometrySorted where id="+id)
       get_BPhotometry = ("select count(1) from bi.bPhotometrySorted where id="+id)

       cursor.execute(get_objectName)
       objectName = cursor.fetchone()
       objectName = objectName[0]

       cursor.execute(get_StartDate)
       StartDate = cursor.fetchone()
       StartDate = str(StartDate[0])

       cursor.execute(get_EndDate)
       EndDate = cursor.fetchone()
       EndDate = str(EndDate[0])

       cursor.execute(get_UPhotometry)
       UPhotometry = cursor.fetchone()
       UPhotometry = str(UPhotometry[0])
       if UPhotometry != 'null':
           UPhotometry = 'YES'
       else:
           UPhotometry = 'NO'

       cursor.execute(get_VPhotometry)
       VPhotometry = cursor.fetchone()
       VPhotometry = str(VPhotometry[0])
       if VPhotometry != 'null':
          VPhotometry = 'YES'
       else:
          VPhotometry = 'NO'

       cursor.execute(get_BPhotometry)
       BPhotometry = cursor.fetchone()
       BPhotometry = str(BPhotometry[0])
       if BPhotometry != 'null':
          BPhotometry = 'YES'
       else:
          BPhotometry = 'NO'

       object = {'name': objectName, 'startDate': StartDate,
                  'endDate': EndDate, 'uPhotometry': UPhotometry,
                  'vPhotometry': VPhotometry,
                  'bPhotometry': BPhotometry}

       controller = str(object) + ',' + controller

    controller = controller[:-1]
    controller = ast.literal_eval(controller)

    try:
       print json.dumps(controller, skipkeys=True)
    except (TypeError, ValueError) as err:
       print 'ERROR:', err
    controller = json.dumps(controller, skipkeys=True)

    json_string = json.dumps(controller, skipkeys=True, sort_keys=True, indent=2)
    json_string = json.loads(controller)


#------------------------------------------------get last Processed data------------------------------------------------

    get_LastLoadObservationId = ("select distinct(lg.ObservationId) from log.log lg join bi.observationsSorted os on lg.ObservationId=os.Id where lg.LastLoad=1")
    get_LastLoadStarName = ("select distinct(os.StarName) from log.log lg join bi.observationsSorted os on lg.ObservationId=os.Id where lg.LastLoad=1")
    get_LastLoadStartDate = ("select distinct(cast(os.StartDate as varchar)) from log.log lg join bi.observationsSorted os on lg.ObservationId=os.Id where lg.LastLoad=1")
    get_LastLoadEndDate = ("select distinct(cast(os.EndDate as varchar)) from log.log lg join bi.observationsSorted os on lg.ObservationId=os.Id where lg.LastLoad=1")

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


    lastLoad = [{'observationId': LastLoadObservationId, 'starName': LastLoadStarName, 'startDate': LastLoadStartDate, 'endDate': LastLoadEndDate}]

    cursor.close()

    print lastLoad
except:
        print 'errors'
else:
    cnx.close()

def json_data():
    json_data.jsonData = json_string

def json_load():
    json_load.jsonLastLoad = lastLoad