import sys
import re
import pyodbc
import ConfigParser
import csv
import pandas


config = ConfigParser.RawConfigParser()
config.read('../resources/ConfigFile.properties')
dbAddress = config.get('DatabaseSection', 'database.address');

reload(sys)
sys.setdefaultencoding('utf8')

#----------------------------------------------insert new observation---------------------------------------------------
def json_parser(name, startDate, endDate, uName, uFileName, vName, vFileName, bName, bFileName):
 try:
     cnx = pyodbc.connect(dbAddress)
     cursor = cnx.cursor()


     get_lastId = ("select top 1 id from stg.StagingObservations order by id desc")
     cursor.execute(get_lastId)
     lastId = cursor.fetchone()

     if lastId is None:
         lastId = 1
     else:
         lastId = lastId[0] + 1

     lastId = str(lastId)
     name = str(name)
     startDate = str(startDate)
     endDate = str(endDate)


  #--insert to data.fileNames
     #--uPhotometry
     uName = str(uName)
     uFileName = str(uFileName)
     print uFileName
     insert_uFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+lastId+",'"+uFileName+"', ' ', ' ')")

     print insert_uFileName

     cursor.execute(insert_uFileName)
     cnx.commit()

     #--vPhotometry
     vName = str(vName)
     vFileName = str(vFileName)
     print vFileName
     insert_vFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+lastId+",'"+vFileName+"', ' ', ' ')")

     print insert_vFileName

     cursor.execute(insert_vFileName)
     cnx.commit()

     #--bPhotometry
     bName = str(bName)
     bFileName = str(bFileName)
     print bFileName
     insert_bFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+lastId+",'"+bFileName+"', ' ', ' ')")

     print insert_bFileName

     cursor.execute(insert_bFileName)
     cnx.commit()

  #---insert to stg.stagingObservations
     #--read ufile
     udata = pandas.read_csv('uploads/'+uFileName, header=None)
     print udata
     udataRange = len(udata)
     print udataRange
     udata.columns = ["uTime", "uFlux"]
     print(udata.columns)
     print udata.uTime[0]

     #--read vfile
     vdata = pandas.read_csv('uploads/'+vFileName, header=None)
     print vdata
     vdataRange = len(vdata)
     print vdataRange
     vdata.columns = ["vTime", "vFlux"]
     print(vdata.columns)
     print vdata.vTime[0]

     #--read bfile
     bdata = pandas.read_csv('uploads/'+bFileName, header=None)
     print bdata
     bdataRange = len(bdata)
     print bdataRange
     bdata.columns = ["bTime", "bFlux"]
     print(bdata.columns)
     print bdata.bTime[0]


     insert_observation = ''

     for counter in range(0,udataRange):
        if counter < udataRange-1:
           i = counter
           j = counter
           utime = str(udata.uTime[i])
           uflux = str(udata.uFlux[i])
           vtime = str(vdata.vTime[i])
           vflux = str(vdata.vFlux[i])
           btime = str(bdata.bTime[i])
           bflux = str(bdata.bFlux[i])
           j = str(counter + 1)
           observation = "SELECT "+lastId+","+j+",'"+name+"','"+startDate+"','"+endDate+"','"+utime+"','"+uflux+"','"+vtime+"','"+vflux+"','"+btime+"','"+bflux+"','new',1 UNION ALL "
           insert_observation = insert_observation + observation
        else:
           i = counter
           j = counter
           utime = str(udata.uTime[i])
           uflux = str(udata.uFlux[i])
           vtime = str(vdata.vTime[i])
           vflux = str(vdata.vFlux[i])
           btime = str(bdata.bTime[i])
           bflux = str(bdata.bFlux[i])
           j = str(counter + 1)
           observation = "SELECT "+lastId+","+j+",'"+name+"','"+startDate+"','"+endDate+"','"+utime+"','"+uflux+"','"+vtime+"','"+vflux+"','"+btime+"','"+bflux+"','new',1"
           insert_observation = insert_observation + observation



     insert_observation = "SET NOCOUNT ON ;with cte (ID,RowId,StarName,StartDate,EndDate,uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime," \
                          "bPhotometry,Status,Active) as (" + insert_observation + ") INSERT INTO stg.stagingObservations (ID,RowId,StarName,StartDate,EndDate," \
                          "uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime,bPhotometry,Status,Active) select * from cte GO"

     print insert_observation

     cursor.execute(insert_observation)
     cnx.commit()

     cursor.close()

 except:
   print 'errors'
 else:
   cnx.close()


#---------------------------------------------Update existing observation----------------------------------------------
def updateObservation(id, name, startDate, endDate, uPhotometry, vPhotometry, bPhotometry):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        id = str(id)
        name = str(name)
        startDate = str(startDate)
        endDate = str(endDate)
        uPhotometry = str(uPhotometry)
        vPhotometry = str(vPhotometry)
        bPhotometry = str(bPhotometry)

        update_observation = ("Update stg.stagingObservations set starName='"+name+"', startDate='"+startDate+"', endDate='"+endDate+"', uPhotometry='0.259254028383', uPhotometryTime='2721.7367',"
                              "vPhotometry='0.259254028383', vPhotometryTime='2721.7367', bPhotometry='0.259254028383', bPhotometryTime='2721.7367', Status='new', active=1 where id="+id+"")

        print update_observation

        cursor.execute(update_observation)
        cnx.commit()

        cursor.close()

    except:
        print 'errors'
    else:
        cnx.close()