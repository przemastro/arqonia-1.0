import simplejson as json
import pyodbc
import ast

try:

    cnx = pyodbc.connect('Driver={SQL Server};Server=SAMSUNG-PC\SQLEXPRESS;Database=astro;Trusted_Connection=yes;uid=SAMSUNG-PC\SAMSUNG;pwd=')
    cursor = cnx.cursor()

    get_observationsCount = ("select count(1) from dbo.Observations;")

    cursor.execute(get_observationsCount)
    observationsCount = cursor.fetchone()
    observationsCount = observationsCount[0]

    controller = ''
    count = ''

    for counter in range(1, observationsCount+1):
       id=str(counter)
       get_objectName = ("select StarName from dbo.Observations where id="+id)
       get_StartDate = ("select StartDate from dbo.Observations where id="+id)
       get_EndDate = ("select EndDate from dbo.Observations where id="+id)
       get_UPhotometry = ("select UPhotometry from dbo.Observations where id="+id)
       get_VPhotometry = ("select VPhotometry from dbo.Observations where id="+id)
       get_Bhotometry = ("select BPhotometry from dbo.Observations where id="+id)

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

       cursor.execute(get_VPhotometry)
       VPhotometry = cursor.fetchone()
       VPhotometry = str(VPhotometry[0])

       cursor.execute(get_Bhotometry)
       Bhotometry = cursor.fetchone()
       Bhotometry = str(Bhotometry[0])

       object = {'name': objectName, 'startDate': StartDate,
                  'endDate': EndDate, 'uPhotometry': UPhotometry,
                  'vPhotometry': VPhotometry,
                  'bPhotometry': Bhotometry}

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


    cursor.close()

except:
        print 'errors'
else:
    cnx.close()

def json_data():
    json_data.jsonData = json_string
