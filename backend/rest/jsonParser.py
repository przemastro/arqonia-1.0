import sys
import pyodbc
import ConfigParser
import pandas
import ast
import simplejson as json
from sjcl import SJCL
import os
import convertPlots
import reduceImages
import zipFiles
import time
from multiprocessing import Process, Queue


env = ConfigParser.RawConfigParser()
env.read('../resources/env.properties')
dbAddress = env.get('DatabaseConnection', 'database.address');
backendInputFits = env.get('FilesCatalogs', 'catalog.backendInputFits');
frontendInputFits = env.get('FilesCatalogs', 'catalog.frontendInputFits');
key = env.get('SecurityKey', 'public.key');
queries = ConfigParser.RawConfigParser()
queries.read('../resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()

reload(sys)
sys.setdefaultencoding('utf8')

#----------------------------------------------insert new observation---------------------------------------------------
def json_parser(name, startDate, endDate, uFileName, vFileName, bFileName, rFileName, iFileName, objectType, verified, email):
 try:
     cnx = pyodbc.connect(dbAddress)
     cursor = cnx.cursor()

     email = str(email)

     get_lastId = queries.get('DatabaseQueries', 'database.getLastIdFromStagingObservations')
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
     objectType = str(objectType)
     verified = str(verified)

     if verified == 'Yes':
        verified = '1'
     else:
        verified = '0'

  #--insert to data.fileNames
     #--uPhotometry
     uFileName = str(uFileName)
     if uFileName != 'None':
        cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (lastId, uFileName))
        cnx.commit()

     #--vPhotometry
     vFileName = str(vFileName)
     if vFileName != 'None':
        cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (lastId, vFileName))
        cnx.commit()

     #--bPhotometry
     bFileName = str(bFileName)
     if bFileName != 'None':
        cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (lastId, bFileName))
        cnx.commit()

     #--rPhotometry
     rFileName = str(rFileName)
     if rFileName != 'None':
         cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (lastId, rFileName))
         cnx.commit()

     #--iPhotometry
     iFileName = str(iFileName)
     if iFileName != 'None':
         cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (lastId, iFileName))
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

     #--read vfile
     rdataRange = 0
     if rFileName != 'None':
         rdata = pandas.read_csv('uploads/'+rFileName, header=None)
         rdataRange = len(rdata)
         rdata.columns = ["rTime", "rFlux"]

     #--read bfile
     idataRange = 0
     if iFileName != 'None':
         idata = pandas.read_csv('uploads/'+iFileName, header=None)
         idataRange = len(idata)
         idata.columns = ["iTime", "iFlux"]


     globalRange = udataRange
     if vdataRange>udataRange:
         globalRange = vdataRange
     if bdataRange>globalRange:
         globalRange = bdataRange
     if rdataRange>globalRange:
         globalRange = rdataRange
     if idataRange>globalRange:
         globalRange = idataRange


     insert_observation = ''

     if uFileName != 'None' or vFileName != 'None' or bFileName != 'None' or rFileName != 'None' or iFileName != 'None':
        for counter in range(0,globalRange):
           if counter < globalRange:
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
              try:
                  if rFileName != 'None':
                      rtime = str(rdata.rTime[i])
                      rflux = str(rdata.rFlux[i])
                  else:
                      rtime = 'NULL'
                      rflux = 'NULL'
              except:
                  rtime = 'NULL'
                  rflux = 'NULL'
              try:
                  if iFileName != 'None':
                      itime = str(idata.iTime[i])
                      iflux = str(idata.iFlux[i])
                  else:
                      itime = 'NULL'
                      iflux = 'NULL'
              except:
                  itime = 'NULL'
                  iflux = 'NULL'
              j = str(counter + 1)
              observation = "SELECT "+lastId+","+j+",'"+name+"','"+objectType+"',cast('"+startDate+"' as datetime),cast('"+endDate+"' as datetime),"+utime+","+uflux+","+vtime+","+vflux+","+btime+","+bflux+"," \
                                                                                                                                                                                                             ""+rtime+","+rflux+","+itime+","+iflux+", 'new',1, '"+verified+"',  (select id from data.users where email='"+email+"') UNION ALL "
              insert_observation = insert_observation + observation


        insert_observation = insert_observation[:-10]

        insert_observation = "SET NOCOUNT ON ;with cte (ID,RowId,ObjectName,ObjectType,StartDate,EndDate,uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime," \
                             "bPhotometry,rPhotometryTime,rPhotometry,iPhotometryTime,iPhotometry,Status,Active,Verified,OwnerId) as (" + insert_observation + ") INSERT INTO stg.stagingObservations (ID,RowId,ObjectName,ObjectType,StartDate,EndDate," \
                             "uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime,bPhotometry,rPhotometryTime,rPhotometry,iPhotometryTime,iPhotometry,Status,Active,Verified,OwnerId) select * from cte GO"
        print insert_observation

        cursor.execute(insert_observation)
        cnx.commit()

     cursor.close()

 except:
   print 'errors in json_parser function'
 else:
   cnx.close()


#---------------------------------------------Update existing observation----------------------------------------------
def updateObservation(id, name, startDate, endDate, uFileName, vFileName, bFileName, rFileName, iFileName, objectType, verified, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)
        id = str(id)
        name = str(name)
        startDate = str(startDate)
        endDate = str(endDate)
        objectType = str(objectType)
        verified = str(verified)

        if verified == 'Yes':
           verified = '1'
        else:
           verified = '0'

    #--update in stg.stagingObservations and delete in data.fileNames

        cursor.execute(queries.get('DatabaseQueries', 'database.deleteStagingObservationsData'), (id))
        cnx.commit()

        #delete_observation= ("delete from bi.observations where id="+id)
        #cursor.execute(delete_observation)
        #cnx.commit()

        cursor.execute(queries.get('DatabaseQueries', 'database.deleteFilesFromFileNames'), (id))
        cnx.commit()

    #--insert to data.fileNames
        #--uPhotometry
        uFileName = str(uFileName)
        if uFileName != 'None':
           cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (id, uFileName))
           cnx.commit()

        #--vPhotometry
        vFileName = str(vFileName)
        if vFileName != 'None':
           cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (id, vFileName))
           cnx.commit()

        #--bPhotometry
        bFileName = str(bFileName)
        if bFileName != 'None':
           cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (id, bFileName))
           cnx.commit()

        #--rPhotometry
        rFileName = str(rFileName)
        if rFileName != 'None':
            cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (id, rFileName))
            cnx.commit()

        #--iPhotometry
        iFileName = str(iFileName)
        if iFileName != 'None':
            cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames'), (id, iFileName))
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

        #--read vfile
        rdataRange = 0
        if rFileName != 'None':
            rdata = pandas.read_csv('uploads/'+rFileName, header=None)
            rdataRange = len(rdata)
            rdata.columns = ["rTime", "rFlux"]

        #--read bfile
        idataRange = 0
        if iFileName != 'None':
            idata = pandas.read_csv('uploads/'+iFileName, header=None)
            idataRange = len(idata)
            idata.columns = ["iTime", "iFlux"]


        globalRange = udataRange
        if vdataRange>udataRange:
            globalRange = vdataRange
        if bdataRange>globalRange:
            globalRange = bdataRange
        if rdataRange>globalRange:
            globalRange = rdataRange
        if idataRange>globalRange:
            globalRange = idataRange

        insert_observation = ''

        for counter in range(0,globalRange):
            if counter < globalRange:
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
                try:
                    if rFileName != 'None':
                        rtime = str(rdata.rTime[i])
                        rflux = str(rdata.rFlux[i])
                    else:
                        rtime = 'NULL'
                        rflux = 'NULL'
                except:
                    rtime = 'NULL'
                    rflux = 'NULL'
                try:
                    if iFileName != 'None':
                        itime = str(idata.iTime[i])
                        iflux = str(idata.iFlux[i])
                    else:
                        itime = 'NULL'
                        iflux = 'NULL'
                except:
                    itime = 'NULL'
                    iflux = 'NULL'
                j = str(counter + 1)
                observation = "SELECT "+id+","+j+",'"+name+"','"+objectType+"',cast('"+startDate+"' as datetime),cast('"+endDate+"' as datetime),"+utime+","+uflux+","+vtime+","+vflux+"," \
                                                                   ""+btime+","+bflux+","+rtime+","+rflux+","+itime+","+iflux+",'new',1, '"+verified+"', (select id from data.users where email='"+email+"') UNION ALL "
                insert_observation = insert_observation + observation

        insert_observation = insert_observation[:-10]

        insert_observation = "SET NOCOUNT ON ;with cte (ID,RowId,ObjectName,ObjectType,StartDate,EndDate,uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime," \
                             "bPhotometry,rPhotometryTime,rPhotometry,iPhotometryTime,iPhotometry,Status,Active,Verified,OwnerId) as (" + insert_observation + ") INSERT INTO stg.stagingObservations (ID,RowId,ObjectName,ObjectType,StartDate,EndDate," \
                                                                                      "uPhotometryTime,uPhotometry,vPhotometryTime,vPhotometry,bPhotometryTime,bPhotometry,rPhotometryTime,rPhotometry,iPhotometryTime,iPhotometry,Status,Active,Verified,OwnerId) select * from cte GO"


        cursor.execute(insert_observation)
        cnx.commit()


        cursor.close()

    except:
        print 'errors in updateObservation function'
    else:
        cnx.close()


#----------------------------------------------------add new user-------------------------------------------------------
def addUser(name, email, activeNumber):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        name = str(name)
        email = str(email)
        activeNumber = str(activeNumber)

        if email != 'None' and name != 'None':
            cursor.execute(queries.get('DatabaseQueries', 'database.verifyUserExists'), (email))
            Value = cursor.fetchone()[0]

            if Value>0:
                msg = "User exists"
            else:
                cursor.execute(queries.get('DatabaseQueries', 'database.insertNewUser'), (name, email, activeNumber, activeNumber))
                cnx.commit()
                msg = "Correct"

        return msg
        cursor.close()

    except:
        print 'errors in addUser function'
    else:
        cnx.close()


#----------------------------------------------------update existing user-----------------------------------------------
def updateUser(name, email, password, oldEmail):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        name = str(name)
        email = str(email)
        password = str(password)
        oldEmail = str(oldEmail)

        if email != 'None' and password != 'None' and name != 'None' and oldEmail != 'None':
                cursor.execute(queries.get('DatabaseQueries', 'database.updateExistingUser'), (name, email, password, oldEmail))
                cnx.commit()
                msg = "Correct"

        return msg
        cursor.close()

    except:
        print 'errors in updateUser function'
    else:
        cnx.close()

#----------------------------------------------------remove existing user-----------------------------------------------
def removeUser(email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)

        if email != 'None':
            cursor.execute(queries.get('DatabaseQueries', 'database.softDeleteUser'), (email))
            cnx.commit()
            cursor.execute(queries.get('DatabaseQueries', 'database.removeObservationsOfDeletedUser'), (email))
            cnx.commit()
            msg = "Correct"

        return msg
        cursor.close()

    except:
        print 'errors in removeUser function'
    else:
        cnx.close()

#----------------------------------------------------Get Password-------------------------------------------------------
def getPassword(email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)

        cursor.execute(queries.get('DatabaseQueries', 'database.getPassword'), (email))
        Value = cursor.fetchone()
        msg = Value[0]

        return msg
        cursor.close()

    except:
        print 'errors in getPassword function'
    else:
        cnx.close()


#------------------------------------------------------Authentication---------------------------------------------------
def authentication(email, sessionId):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)
        sessionId = int(sessionId)

        cursor.execute(queries.get('DatabaseQueries', 'database.getSessionId'), (email))
        DBSessionId = cursor.fetchone()
        if(DBSessionId[0] != None):
           DBSessionId = int(DBSessionId[0])
        else:
           DBSessionId = int(0)
        if(DBSessionId==sessionId):
            cursor.execute(queries.get('DatabaseQueries', 'database.updateSysDate'), (email))
            cnx.commit()
            auth = 'true'
        else:
            auth = "Unauthorized User"

        return auth
        cursor.close()

    except:
        print 'errors in authentication function'
    else:
        cnx.close()


#------------------------------------------------------Logout User------------------------------------------------------
def logoutUser(email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)

        cursor.execute(queries.get('DatabaseQueries', 'database.logoutUser'), (email))
        cnx.commit()
        cursor.close()

    except:
        print 'errors in logoutUser function'
    else:
        cnx.close()

#-----------------------------------------------------verify Credentials------------------------------------------------
def verifyCredentials(email, password, sessionId):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)
        password = str(password)
        sessionId = str(sessionId)

        #Verify user exists
        if email != 'None' and password != 'None':
            cursor.execute(queries.get('DatabaseQueries', 'database.verifyUser'), (email))

        Value = cursor.fetchone()[0]

        if Value==1:
            #Firstly check if user is logged in
            cursor.execute(queries.get('DatabaseQueries', 'database.getSessionId'), (email))
            sessionIdValue = cursor.fetchone()
            if(str(sessionIdValue[0]) != 'None'):
               msg = "User is already logged In"
            else:
               #Now verify credentials
               cursor.execute(queries.get('DatabaseQueries', 'database.getPassword'), (email))
               DBPassword = cursor.fetchone()[0]
               if(decrypt_password(DBPassword)==password):
                  #Activation for first login - in fact I will update everytime this flag
                  cursor.execute(queries.get('DatabaseQueries', 'database.updateActiveFlag'), (email))
                  cnx.commit()
                  #Update SessionId
                  cursor.execute(queries.get('DatabaseQueries', 'database.updateSessionId'), (sessionId, email))
                  cnx.commit()
                  #and the rest
                  cursor.execute(queries.get('DatabaseQueries', 'database.getUserName'), (email))
                  msg = cursor.fetchone()[0]
               else:
                  msg = "Wrong credentials"
        else:
            msg = "Wrong credentials"

        return msg
        cursor.close()

    except:
        print 'errors in verifyCredentials function'
    else:
        cnx.close()


#----------------------------------------------------add subscriber-----------------------------------------------------
def addSubscriber(email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)

        cursor.execute(queries.get('DatabaseQueries', 'database.addSubscriberIfNotExists'), (email, email))
        cnx.commit()

        cursor.close()

    except:
        print 'errors in addUser function'
    else:
        cnx.close()


#--------------------------------------------------Return object details------------------------------------------------
def objectDetails(name):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        objectName = str(name)

        if(objectName[:3]=='TYC'):
            tycObjectName = objectName[3:]
            length = len(tycObjectName)
            tyc3ObjectName = tycObjectName[length-1:]
            specialCharacterPosition = tycObjectName.index('-')
            tyc1ObjectName = tycObjectName[:specialCharacterPosition]
            tyc2ObjectName = tycObjectName[:length-2]
            tyc2ObjectName = tyc2ObjectName[specialCharacterPosition+1:]

        controller = ''
        #Proper Name
        if((cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromHDName'), (objectName)).fetchone())[0]>0):

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingObjectName'), (objectName)).fetchone()
            if(HD): #if record exists
               if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                   calc = str(float(HD[4].strip())-float(HD[3].strip()))
               else:
                   calc = " "
               details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
               controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingObjectName'), (objectName)).fetchone()
            if(HR):
               if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                   calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                   calcU = str(float(HR[6].strip())+float(HR[3].strip()))
               else:
                   calcB = " "
                   calcU = " "
               details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
               controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingObjectName'), (objectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingObjectName'), (objectName)).fetchone()
            if(SAO):
               if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                   calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
               else:
                   calc = " "
               details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
               controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingObjectName'), (objectName)).fetchone()
            if(TYC2):
               if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                   calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
               else:
                   calc = " "
               details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
               controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingObjectName'), (objectName)).fetchone()
            if(HIP):
               if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                   calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
               else:
                   calc = " "
               details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
               controller = str(details) + ',' + controller
            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)

        #HD
        elif (objectName[:2]=='HD' and (cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromHD'), (objectName[2:])).fetchone())[0]>0):
            hdObjectName = objectName[2:]

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingHDObjectName'), (hdObjectName)).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingHDObjectName'), (hdObjectName)).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingHDObjectName'), (hdObjectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingHDObjectName'), (hdObjectName)).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingHDObjectName'), (hdObjectName)).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingHDObjectName'), (hdObjectName)).fetchone()
            if(HIP):
                if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                    calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)

        #HR
        elif (objectName[:2]=='HR' and (cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromHR'), (objectName[2:])).fetchone())[0]>0):
            hrObjectName = objectName[2:]

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingHRObjectName'), (hrObjectName)).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingHRObjectName'), (hrObjectName)).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingHRObjectName'), (hrObjectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingHRObjectName'), (hrObjectName)).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingHRObjectName'), (hrObjectName)).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingHRObjectName'), (hrObjectName)).fetchone()
            if(HIP):
                if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                    calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)


        #HR by name
        elif ((cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromHRByName'), (objectName)).fetchone())[0]>0):

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingObjectNameInHR'), (objectName)).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingObjectNameInHR'), (objectName)).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingObjectNameInHR'), (objectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingObjectNameInHR'), (objectName)).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingObjectNameInHR'), (objectName)).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingObjectNameInHR'), (objectName)).fetchone()
            if(HIP):
                if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                    calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)

        #GC
        elif (objectName[:2]=='GC' and (cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromGC'), (objectName[2:])).fetchone())[0]>0):
            gcObjectName = objectName[2:]

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingGCObjectName'), (gcObjectName)).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingGCObjectName'), (gcObjectName)).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingGCObjectName'), (gcObjectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingGCObjectName'), (gcObjectName)).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingGCObjectName'), (gcObjectName)).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingGCObjectName'), (gcObjectName)).fetchone()
            if(HIP):
                if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                    calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)

        #SAO
        elif (objectName[:3]=='SAO' and (cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromSAO'), (objectName[3:])).fetchone())[0]>0):
            saoObjectName = objectName[3:]

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingSAOObjectName'), (saoObjectName)).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingSAOObjectName'), (saoObjectName)).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingSAOObjectName'), (saoObjectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingSAOObjectName'), (saoObjectName)).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingSAOObjectName'), (saoObjectName)).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingSAOObjectName'), (saoObjectName)).fetchone()
            if(HIP):
                if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                    calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)


        #HIP
        elif (objectName[:3]=='HIP' and (cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromHIP'), (objectName[3:])).fetchone())[0]>0):
            hipObjectName = objectName[3:]

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingHIPObjectName'), (hipObjectName)).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingHIPObjectName'), (hipObjectName)).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingHIPObjectName'), (hipObjectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingHIPObjectName'), (hipObjectName)).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingHIPObjectName'), (hipObjectName)).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingHIPObjectName'), (hipObjectName)).fetchone()
            if(HIP):
                if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                    calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)


        #TYC2
        elif (objectName[:3]=='TYC' and (cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromTYC'), (tyc1ObjectName, tyc2ObjectName, tyc3ObjectName)).fetchone())[0]>0):

            HD = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHDHavingTYCObjectName'), (tyc1ObjectName, tyc2ObjectName, tyc3ObjectName)).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            HR = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHRHavingTYCObjectName'), (tyc1ObjectName, tyc2ObjectName, tyc3ObjectName)).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            GC = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromGCHavingTYCObjectName'), (tyc1ObjectName, tyc2ObjectName, tyc3ObjectName)).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            SAO = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromSAOHavingTYCObjectName'), (tyc1ObjectName, tyc2ObjectName, tyc3ObjectName)).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            TYC2 = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromTYCHavingTYCObjectName'), (tyc1ObjectName, tyc2ObjectName, tyc3ObjectName)).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            HIP = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromHIPHavingTYCObjectName'), (tyc1ObjectName, tyc2ObjectName, tyc3ObjectName)).fetchone()
            if(HIP):
                if(HIP[3].strip() != "" and HIP[4].strip() != ""):
                    calc = str(float(HIP[4].strip())+float(HIP[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HIP[0].strip(), HIP[1].strip(), "HIP", str(HIP[2]), " ", HIP[3].strip(), calc, HIP[4].strip(), " ", " ", HIP[5].strip(), " ")
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = json.loads(controller)


        #Comets
        elif ((cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromComets'), (objectName)).fetchone())[0]>0):

            COMET = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromComets'), (objectName)).fetchone()
            if(COMET): #if record exists
                details = calculate_cometsParameters(COMET[0].strip(), COMET[1].strip(), COMET[2].strip()+" "+COMET[3].strip()+" "+COMET[4].strip(),
                                                     COMET[5].strip(), COMET[6].strip(), COMET[7].strip(), COMET[8].strip(), COMET[9].strip(),
                                                     COMET[10].strip()+COMET[11].strip()+COMET[12].strip(), COMET[13].strip())
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = [json.loads(controller)]

        #Planetoids
        elif ((cursor.execute(queries.get('DatabaseQueries', 'database.getCountFromMpc'), (objectName)).fetchone())[0]>0):

            PL = cursor.execute(queries.get('DatabaseQueries', 'database.getDataFromMpc'), (objectName)).fetchone()
            if(PL): #if record exists
                details = calculate_planetoidsParameters(PL[0].strip(), PL[1].strip(), PL[2].strip(), PL[3].strip(), PL[4].strip(),
                                                         PL[5].strip(), PL[6].strip(), PL[7].strip(), PL[8].strip(), PL[9].strip(),
                                                         PL[10].strip())

                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = [json.loads(controller)]

        return json_string
        cursor.close()
    except:
        print 'errors in objectDetails function'
    else:
        cnx.close()


#--------------------------------------------------Return personal catalog----------------------------------------------
def catalogData(objectType, abbreviation, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        objectType = str(objectType)
        abbreviation = str(abbreviation)
        email = str(email)

        if(abbreviation=='None'):
            abbreviation=''

        controller = ''
        if(objectType == 'Star'):
           #B-V
           BVObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getBVObservationsDifferenceFromBVDiagramAvgForStar')), (objectType, email)).fetchall()]
           #U-B
           UBObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUBObservationsDifferenceFromUBDiagramAvgForStar')), (objectType, email)).fetchall()]
           #R-I
           RIObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getRIObservationsDifferenceFromRIDiagramAvgForStar')), (objectType, email)).fetchall()]
           #V-I
           VIObservationsDifference = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getVIObservationsDifferenceFromVIDiagramAvgForStar')), (objectType, email)).fetchall()]


        #U
        UObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getUObservationsFromUPhotometrySortedForObjectType')), (objectType, email)).fetchall()]
        #V
        VObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getVObservationsFromVPhotometrySortedForObjectType')), (objectType, email)).fetchall()]
        #B
        BObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getBObservationsFromBPhotometrySortedForObjectType')), (objectType, email)).fetchall()]
        #R
        RObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getRObservationsFromRPhotometrySortedForObjectType')), (objectType, email)).fetchall()]
        #I
        IObservations = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getIObservationsFromIPhotometrySortedForObjectType')), (objectType, email)).fetchall()]
        #ObjectNames
        ObjectNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getObjectNamesForCatalog')), (objectType, email)).fetchall()]
        jsonRange = len(UObservations)


        if(objectType == 'Star'):
            controller = ''
            #to create array of objects if we have only one observation
            if (jsonRange == 1):
                controller = str({'01id': "", '02objectNames': "",
                                  '03uObservations': "", '04vObservations': "", '05bObservations': "",
                                  '06rObservations': "", '07iObservations': "",
                                  '08bvObservationsDifference': "", '09ubObservationsDifference': "",
                                  '10riObservationsDifference': "",'11viObservationsDifference': ""}) + ',' + controller
            for counter in range(0,jsonRange):
                i = counter + 1
                catalogData = {'01id': abbreviation+str(i), '02objectNames': ObjectNames[counter],
                               '03uObservations': UObservations[counter], '04vObservations': VObservations[counter], '05bObservations': BObservations[counter],
                              '06rObservations': RObservations[counter], '07iObservations': IObservations[counter],
                              '08bvObservationsDifference': BVObservationsDifference[counter], '09ubObservationsDifference': UBObservationsDifference[counter],
                              '10riObservationsDifference': RIObservationsDifference[counter],'11viObservationsDifference': VIObservationsDifference[counter]}
                controller = str(catalogData) + ',' + controller
        else:
            controller = ''
            #to create array of objectc if we have only one observation
            if (jsonRange == 1):
                controller = str({'1id': "", '2objectNames': "",
                                  '3uObservations': "", '4vObservations': "", '5bObservations': "",
                                  '6rObservations': "", '7iObservations': ""}) + ',' + controller
            for counter in range(0,jsonRange):
                i = counter + 1
                catalogData = {'1id': abbreviation+str(i), '2objectNames': ObjectNames[counter],
                               '3uObservations': UObservations[counter], '4vObservations': VObservations[counter], '5bObservations': BObservations[counter],
                               '6rObservations': RObservations[counter], '7iObservations': IObservations[counter]}
                controller = str(catalogData) + ',' + controller

        controller = ast.literal_eval(controller[:-1])
        controller = json.dumps(controller, skipkeys=True)


        catalogData = json.loads(controller)

        return catalogData
        cursor.close()
    except:
        print 'errors in catalogData function'
    else:
        cnx.close()



#----------------------------------------------insert new reduction images----------------------------------------------
def addReductionImages(sessionId, files, email, conversionType, imageType):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        sessionId = str(sessionId)
        email = str(email)
        conversionType = str(conversionType)
        imageType = str(imageType)
        fileExtension = 'fits'

        cursor.execute(queries.get('DatabaseQueries', 'database.getLastIdFromDataImages'))
        lastId = cursor.fetchone()
        if lastId is None:
            lastId = 1
        else:
            lastId = lastId[0] + 1

        counter = lastId

        cursor.execute(queries.get('DatabaseQueries', 'database.updateActiveFlagFalse'), (sessionId, imageType))
        cnx.commit()

        #--Insert to data.images
        for file in files:
            objectName = file
            lastId = str(counter)

            existsFlag = cursor.execute(queries.get('DatabaseQueries', 'database.getNumberOfImagesInDataImages'), (objectName, sessionId, conversionType, imageType)).fetchone()

            if (existsFlag[0] == 0):
               print 'fits does not exist in DB'
               cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataReductionImagesFITS'), (lastId, email, fileExtension, sessionId, conversionType, imageType, objectName))
               cnx.commit()
               looper=1
               while(looper<100):
                  time.sleep(1)
                  if os.path.isfile(backendInputFits+objectName):
                      break
                  else:
                      looper = looper + 1
                      continue


               file_list = os.listdir(backendInputFits)
               for fileName in file_list:
                  specialCharacterPosition = objectName.index('.')
                  sourceString = str(objectName[:specialCharacterPosition])
                  replaceString = sessionId+"_"+imageType+"_"+str(objectName[:specialCharacterPosition])
                  if (fileName == objectName):
                      try:
                         os.rename(backendInputFits+fileName, backendInputFits+fileName.replace(sourceString,replaceString))
                      except:
                         print 'errors in renaming function'

               #start conversion
               specialCharacterPosition = objectName.index('.')
               replaceString = sessionId+"_"+imageType+"_"+str(objectName[:specialCharacterPosition])
               convertPlots.plot(replaceString, conversionType)
               #end conversion

               #Add converted file to DB
               convertedObjectName = conversionType+"_"+replaceString+".png"
               counter = counter + 1
               lastId = str(counter)
               print 'png does not exist in DB'
               cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataReductionImagesPNG'), (lastId, email, sessionId, conversionType, imageType, convertedObjectName))
               cnx.commit()

            else:
                print 'fits exists in DB'
                objectName = file
                specialCharacterPosition = objectName.index('.')
                replaceString = sessionId+"_"+imageType+"_"+str(objectName[:specialCharacterPosition])
                convertedObjectName = conversionType+"_"+replaceString+".png"
                #update .png file active flag
                cursor.execute(queries.get('DatabaseQueries', 'database.updateActiveFlagTrue'), (sessionId, convertedObjectName, imageType))
                cnx.commit()
                #update .fits file active flag
                cursor.execute(queries.get('DatabaseQueries', 'database.updateActiveFlagTrue'), (sessionId, file, imageType))
                cnx.commit()
                looper=1
                while(looper<100):
                    time.sleep(1)
                    if os.path.isfile(backendInputFits+objectName):
                        break
                    else:
                        print 'continue fits exists in DB'
                        looper = looper + 1
                        continue

            counter = counter + 1


        #return json value
        get_ImageIds = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getImageIds')), (sessionId, conversionType, imageType)).fetchall()]
        get_FileNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getFileNames')), (sessionId, conversionType, imageType)).fetchall()]
        data = {'imageIds': get_ImageIds, 'fileNames': get_FileNames}
        i = 1
        if(i==1):
           data = data
        elif(i>1):
           data = [data]
        return data
        cursor.close()

    except:
        print 'errors in addReductionImages function'
    else:
        cnx.close()


#--------------------------------------------------------reduce data----------------------------------------------------
def processImages(sessionId, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        sessionId = str(sessionId)
        email = str(email)

        get_lastId = queries.get('DatabaseQueries', 'database.getLastIdFromDataImages')
        cursor.execute(get_lastId)
        lastId = cursor.fetchone()
        if lastId is None:
            lastId = 1
        else:
            lastId = lastId[0] + 1

        #Get Images
        getDarkFrames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getDarkFrames')), (sessionId)).fetchall()]
        getBiasFrames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getBiasFrames')), (sessionId)).fetchall()]
        getFlatFields = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getFlatFields')), (sessionId)).fetchall()]
        getRawFrames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getRawFrames')), (sessionId)).fetchall()]


        reduceImages.reduce(getDarkFrames, getBiasFrames, getFlatFields, getRawFrames, sessionId)

        cursor.execute(queries.get('DatabaseQueries', 'database.updateActiveFlagFalseProcessed'), (sessionId))
        cnx.commit()
        rawImages = getRawFrames
        counter = lastId
        for file in rawImages:
           lastId = str(counter)
           counter = counter + 1
           cursor.execute(queries.get('DatabaseQueries', 'database.insertOutputFitsImages'), (lastId, email, sessionId, file))
           cnx.commit()
           lastId = str(counter)
           counter = counter + 1
           specialCharacterPosition = file.index('.')
           objectName = str(file[:specialCharacterPosition])
           objectName = "Linear_"+sessionId+"_Processed_"+objectName+".png"
           cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataReductionImagesReduction'), (lastId, email, sessionId, objectName))
           cnx.commit()

        #return json value
        get_ImageIds = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getImageIdsReduced')), (sessionId)).fetchall()]
        get_FileNames = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getFileNamesReduced')), (sessionId)).fetchall()]
        data = {'imageIds': get_ImageIds, 'fileNames': get_FileNames}
        i = 1
        if(i==1):
            data = data
        elif(i>1):
            data = [data]
        return data
        cursor.close()

    except:
        print 'errors in processImages function'
    else:
        cnx.close()


#----------------------------------------------------------ZIP Files----------------------------------------------------
def returnZippedImages(sessionId, email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        sessionId = str(sessionId)

        #Get Images
        getImages = [oc[0] for oc in cursor.execute((queries.get('DatabaseQueries', 'database.getImages')), (sessionId)).fetchall()]


        data = zipFiles.zipAll(getImages, sessionId)

        cursor.close()

    except:
        print 'errors in processImages function'
    else:
        cnx.close()


def calculate_starsParameters(ra, de, code, name, Umag, Vmag, Bmag, BV, UB, RI, VI, SpType):
    details = {"type": "Star", "ra": ra, "de": de, "code": code, "name": name, "Umag": Umag, "Vmag": Vmag, "Bmag": Bmag, "BV": BV, "UB": UB, "RI": RI, "VI": VI, "SpType": SpType}
    return details

def calculate_cometsParameters(name, orbitType, pDate, pDistance, e, perihelion, longitude, inclination, eDate, absMag):
    details = {"type": "Comet", "name": name, "orbitType": orbitType, "pDate": pDate, "pDistance": pDistance, "e": e, "perihelion": perihelion,
               "longitude": longitude, "inclination": inclination, "eDate": eDate, "absMag": absMag}
    return details

def calculate_planetoidsParameters(name, number, h, epoch, m, perihelion, longitude, inclination, e, n, a):
    details = {"type": "Planetoid", "name": name, "number": number, "h": h, "epoch": epoch, "m": m, "perihelion": perihelion,
               "longitude": longitude, "inclination": inclination, "e": e, "n": n, "a": a}
    return details

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

def decrypt_password(password):
    d = json.loads(password)
    sj = SJCL().decrypt(d, key)
    return sj