import sys
import pyodbc
import ConfigParser
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
     if uFileName != 'None':
        insert_uFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+lastId+",'"+uFileName+"', ' ', ' ')")

        cursor.execute(insert_uFileName)
        cnx.commit()

     #--vPhotometry
     vName = str(vName)
     vFileName = str(vFileName)
     if vFileName != 'None':
        insert_vFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+lastId+",'"+vFileName+"', ' ', ' ')")


        cursor.execute(insert_vFileName)
        cnx.commit()

     #--bPhotometry
     bName = str(bName)
     bFileName = str(bFileName)
     if bFileName != 'None':
        insert_bFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+lastId+",'"+bFileName+"', ' ', ' ')")

        cursor.execute(insert_bFileName)
        cnx.commit()


  #---insert to stg.stagingObservations
     #--read ufile
     udataRange = 0
     if uFileName != 'None':
        udata = pandas.read_csv('uploads/'+uFileName, header=None)
        udataRange = len(udata)
        udata.columns = ["uTime", "uFlux"]

     #--read vfile
     vdataRange = 0
     if vFileName != 'None':
        vdata = pandas.read_csv('uploads/'+vFileName, header=None)
        vdataRange = len(vdata)
        vdata.columns = ["vTime", "vFlux"]

     #--read bfile
     bdataRange = 0
     if bFileName != 'None':
        bdata = pandas.read_csv('uploads/'+bFileName, header=None)
        bdataRange = len(bdata)
        bdata.columns = ["bTime", "bFlux"]

     globalRange = udataRange
     if vdataRange>udataRange:
         globalRange = vdataRange
     if bdataRange>vdataRange:
         globalRange = bdataRange

     insert_observation = ''

     if uFileName != 'None' or vFileName != 'None' or bFileName != 'None':
        for counter in range(0,globalRange):
           if counter < globalRange-1:
              i = counter
              j = counter
              try:
                  if uFileName != 'None':
                      utime = str(udata.uTime[i])
                      uflux = str(udata.uFlux[i])
                  else:
                      utime = 'NULL'
                      uflux = 'NULL'
              except:
                  utime = 'NULL'
                  uflux = 'NULL'
              try:
                  if vFileName != 'None':
                      vtime = str(vdata.vTime[i])
                      vflux = str(vdata.vFlux[i])
                  else:
                      vtime = 'NULL'
                      vflux = 'NULL'
              except:
                  vtime = 'NULL'
                  vflux = 'NULL'
              try:
                  if bFileName != 'None':
                      btime = str(bdata.bTime[i])
                      bflux = str(bdata.bFlux[i])
                  else:
                      btime = 'NULL'
                      bflux = 'NULL'
              except:
                  btime = 'NULL'
                  bflux = 'NULL'
              j = str(counter + 1)
              observation = "SELECT "+lastId+","+j+",'"+name+"',cast('"+startDate+"' as datetime),cast('"+endDate+"' as datetime),"+utime+","+uflux+","+vtime+","+vflux+","+btime+","+bflux+",'new',1 UNION ALL "
              insert_observation = insert_observation + observation
           else:
              i = counter
              j = counter

              try:
                  if uFileName != 'None':
                      utime = str(udata.uTime[i])
                      uflux = str(udata.uFlux[i])
                  else:
                      utime = 'NULL'
                      uflux = 'NULL'
              except:
                  utime = 'NULL'
                  uflux = 'NULL'
              try:
                  if vFileName != 'None':
                      vtime = str(vdata.vTime[i])
                      vflux = str(vdata.vFlux[i])
                  else:
                      vtime = 'NULL'
                      vflux = 'NULL'
              except:
                  vtime = 'NULL'
                  vflux = 'NULL'
              try:
                  if bFileName != 'None':
                      btime = str(bdata.bTime[i])
                      bflux = str(bdata.bFlux[i])
                  else:
                      btime = 'NULL'
                      bflux = 'NULL'
              except:
                  btime = 'NULL'
                  bflux = 'NULL'
              j = str(counter + 1)
              observation = "SELECT "+lastId+","+j+",'"+name+"',cast('"+startDate+"' as datetime),cast('"+endDate+"' as datetime),"+utime+","+uflux+","+vtime+","+vflux+","+btime+","+bflux+",'new',1"
              insert_observation = insert_observation + observation



        insert_observation = "SET NOCOUNT ON ;with cte (ID,RowId,StarName,StartDate,EndDate,uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime," \
                             "bPhotometry,Status,Active) as (" + insert_observation + ") INSERT INTO stg.stagingObservations (ID,RowId,StarName,StartDate,EndDate," \
                             "uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime,bPhotometry,Status,Active) select * from cte GO"

        cursor.execute(insert_observation)
        cnx.commit()

     cursor.close()

 except:
   print 'errors'
 else:
   cnx.close()


#---------------------------------------------Update existing observation----------------------------------------------
def updateObservation(id, name, startDate, endDate, uName, uFileName, vName, vFileName, bName, bFileName):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()



        id = str(id)
        name = str(name)
        startDate = str(startDate)
        endDate = str(endDate)

    #--update in stg.stagingObservations and delete in data.fileNames

        delete_stagingObservation= ("delete from stg.stagingObservations where id="+id)

        cursor.execute(delete_stagingObservation)
        cnx.commit()

        delete_observation= ("delete from bi.observations where id="+id)

        cursor.execute(delete_observation)
        cnx.commit()

        delete_files= ("delete from data.fileNames where observationId="+id)

        cursor.execute(delete_files)
        cnx.commit()

    #--insert to data.fileNames
        #--uPhotometry
        uName = str(uName)
        uFileName = str(uFileName)
        if uFileName != 'None':
           insert_uFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+id+",'"+uFileName+"', ' ', ' ')")

           cursor.execute(insert_uFileName)
           cnx.commit()

        #--vPhotometry
        vName = str(vName)
        vFileName = str(vFileName)
        if vFileName != 'None':
           insert_vFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+id+",'"+vFileName+"', ' ', ' ')")


           cursor.execute(insert_vFileName)
           cnx.commit()

        #--bPhotometry
        bName = str(bName)
        bFileName = str(bFileName)
        if bFileName != 'None':
           insert_bFileName = ("insert into data.fileNames(ObservationId, FileName, FileType, FileSize) values("+id+",'"+bFileName+"', ' ', ' ')")

           cursor.execute(insert_bFileName)
           cnx.commit()


    #---insert to stg.stagingObservations
        #--read ufile
        udataRange = 0
        if uFileName != 'None':
           udata = pandas.read_csv('uploads/'+uFileName, header=None)
           udataRange = len(udata)
           udata.columns = ["uTime", "uFlux"]

        #--read vfile
        vdataRange = 0
        if vFileName != 'None':
           vdata = pandas.read_csv('uploads/'+vFileName, header=None)
           vdataRange = len(vdata)
           vdata.columns = ["vTime", "vFlux"]

        #--read bfile
        bdataRange = 0
        if bFileName != 'None':
           bdata = pandas.read_csv('uploads/'+bFileName, header=None)
           bdataRange = len(bdata)
           bdata.columns = ["bTime", "bFlux"]


        globalRange = udataRange
        if vdataRange>udataRange:
           globalRange = vdataRange
        if bdataRange>vdataRange:
           globalRange = bdataRange

        insert_observation = ''

        for counter in range(0,globalRange):
            if counter < globalRange-1:
                i = counter
                j = counter
                try:
                    if uFileName != 'None':
                        utime = str(udata.uTime[i])
                        uflux = str(udata.uFlux[i])
                    else:
                        utime = 'NULL'
                        uflux = 'NULL'
                except:
                    utime = 'NULL'
                    uflux = 'NULL'
                try:
                    if vFileName != 'None':
                        vtime = str(vdata.vTime[i])
                        vflux = str(vdata.vFlux[i])
                    else:
                        vtime = 'NULL'
                        vflux = 'NULL'
                except:
                    vtime = 'NULL'
                    vflux = 'NULL'
                try:
                    if bFileName != 'None':
                        btime = str(bdata.bTime[i])
                        bflux = str(bdata.bFlux[i])
                    else:
                        btime = 'NULL'
                        bflux = 'NULL'
                except:
                    btime = 'NULL'
                    bflux = 'NULL'
                j = str(counter + 1)
                observation = "SELECT "+id+","+j+",'"+name+"',cast('"+startDate+"' as datetime),cast('"+endDate+"' as datetime),"+utime+","+uflux+","+vtime+","+vflux+","+btime+","+bflux+",'new',1 UNION ALL "
                insert_observation = insert_observation + observation
            else:
                i = counter
                j = counter
                try:
                    if uFileName != 'None':
                        utime = str(udata.uTime[i])
                        uflux = str(udata.uFlux[i])
                    else:
                        utime = 'NULL'
                        uflux = 'NULL'
                except:
                    utime = 'NULL'
                    uflux = 'NULL'
                try:
                    if vFileName != 'None':
                        vtime = str(vdata.vTime[i])
                        vflux = str(vdata.vFlux[i])
                    else:
                        vtime = 'NULL'
                        vflux = 'NULL'
                except:
                    vtime = 'NULL'
                    vflux = 'NULL'
                try:
                    if bFileName != 'None':
                        btime = str(bdata.bTime[i])
                        bflux = str(bdata.bFlux[i])
                    else:
                        btime = 'NULL'
                        bflux = 'NULL'
                except:
                    btime = 'NULL'
                    bflux = 'NULL'
                j = str(counter + 1)
                observation = "SELECT "+id+","+j+",'"+name+"',cast('"+startDate+"' as datetime),cast('"+endDate+"' as datetime),"+utime+","+uflux+","+vtime+","+vflux+","+btime+","+bflux+",'new',1"
                insert_observation = insert_observation + observation



        insert_observation = "SET NOCOUNT ON ;with cte (ID,RowId,StarName,StartDate,EndDate,uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime," \
                             "bPhotometry,Status,Active) as (" + insert_observation + ") INSERT INTO stg.stagingObservations (ID,RowId,StarName,StartDate,EndDate," \
                                                                                      "uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime,bPhotometry,Status,Active) select * from cte GO"


        cursor.execute(insert_observation)
        cnx.commit()


        cursor.close()

    except:
        print 'errors'
    else:
        cnx.close()