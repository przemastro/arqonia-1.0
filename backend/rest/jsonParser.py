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
        cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+lastId+",'"+uFileName+"', ' ', ' ')")
        cnx.commit()

     #--vPhotometry
     vFileName = str(vFileName)
     if vFileName != 'None':
        cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+lastId+",'"+vFileName+"', ' ', ' ')")
        cnx.commit()

     #--bPhotometry
     bFileName = str(bFileName)
     if bFileName != 'None':
        cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+lastId+",'"+bFileName+"', ' ', ' ')")
        cnx.commit()

     #--rPhotometry
     rFileName = str(rFileName)
     if rFileName != 'None':
         cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+lastId+",'"+rFileName+"', ' ', ' ')")
         cnx.commit()

     #--iPhotometry
     iFileName = str(iFileName)
     if iFileName != 'None':
         cursor.execute(queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+lastId+",'"+iFileName+"', ' ', ' ')")
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

        delete_stagingObservation= ("delete from stg.stagingObservations where id="+id)

        cursor.execute(delete_stagingObservation)
        cnx.commit()

        #delete_observation= ("delete from bi.observations where id="+id)

        #cursor.execute(delete_observation)
        #cnx.commit()

        delete_files= ("delete from data.fileNames where observationId="+id)

        cursor.execute(delete_files)
        cnx.commit()

    #--insert to data.fileNames
        #--uPhotometry
        uFileName = str(uFileName)
        if uFileName != 'None':
           insert_uFileName = (queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+id+",'"+uFileName+"', ' ', ' ')")
           cursor.execute(insert_uFileName)
           cnx.commit()

        #--vPhotometry
        vFileName = str(vFileName)
        if vFileName != 'None':
           insert_vFileName = (queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+id+",'"+vFileName+"', ' ', ' ')")
           cursor.execute(insert_vFileName)
           cnx.commit()

        #--bPhotometry
        bFileName = str(bFileName)
        if bFileName != 'None':
           insert_bFileName = (queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+id+",'"+bFileName+"', ' ', ' ')")
           cursor.execute(insert_bFileName)
           cnx.commit()

        #--rPhotometry
        rFileName = str(rFileName)
        if rFileName != 'None':
            insert_rFileName = (queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+id+",'"+rFileName+"', ' ', ' ')")
            cursor.execute(insert_rFileName)
            cnx.commit()

        #--iPhotometry
        iFileName = str(iFileName)
        if iFileName != 'None':
            insert_iFileName = (queries.get('DatabaseQueries', 'database.insertIntoDataFileNames')+"values("+id+",'"+iFileName+"', ' ', ' ')")
            cursor.execute(insert_iFileName)
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
            verify_User = ("select count(1) from data.users where Email='"+email+"'")
            cursor.execute(verify_User)

            Value = cursor.fetchone()
            Value = Value[0]

            if Value>0:
                msg = "User exists"
            else:
                insert_NewUser = (queries.get('DatabaseQueries', 'database.insertNewUser')+"values('"+name+"', '"+email+"','"+activeNumber+"','false','"+activeNumber+"')")
                cursor.execute(insert_NewUser)
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
                update_ExistingUser = ("update data.users set Name='"+name+"', Email='"+email+"', Password='"+password+"' where email='"+oldEmail+"'")
                cursor.execute(update_ExistingUser)
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
            update_ExistingUser = ("update data.users set activeFlag='false' where email='"+email+"'")
            cursor.execute(update_ExistingUser)
            cnx.commit()
            removeObservation = ("update so set active=1, status='deleted' from stg.stagingObservations so "
                                 "join data.users us on so.OwnerId=us.ID where email='"+email+"'")
            cursor.execute(removeObservation)
            cnx.commit()
            msg = "Correct"

        return msg
        cursor.close()

    except:
        print 'errors in updateUser function'
    else:
        cnx.close()

#----------------------------------------------------Get Password-------------------------------------------------------
def getPassword(email):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)

        get_Password = ("select password from data.users where Email='"+email+"'")
        cursor.execute(get_Password)
        Value = cursor.fetchone()
        msg = Value[0]

        return msg
        cursor.close()

    except:
        print 'errors in addUser function'
    else:
        cnx.close()


#------------------------------------------------------Authentication---------------------------------------------------
def authentication(email, sessionId):
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()

        email = str(email)
        sessionId = int(sessionId)

        verify_sessionId = ("select sessionId from data.users where Email='"+email+"'")
        print verify_sessionId
        cursor.execute(verify_sessionId)
        DBSessionId = cursor.fetchone()
        DBSessionId = int(DBSessionId[0])
        if(DBSessionId==sessionId):
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

        logoutDataUsers = ("update data.users set SessionId=NULL where Email='"+email+"'")
        print logoutDataUsers
        cursor.execute(logoutDataUsers)
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
            verify_User = ("select count(1) from data.users where Email='"+email+"' and (ActiveFlag='true' or (ActiveFlag='false' and ActiveCode is not NULL))")
            cursor.execute(verify_User)

        Value = cursor.fetchone()
        Value = Value[0]

        if Value==1:
            #Firstly check if user is logged in
            verify_userIsLoggedIn = ("select sessionId from data.users where Email='"+email+"'")
            cursor.execute(verify_userIsLoggedIn)
            sessionIdValue = cursor.fetchone()
            print sessionIdValue[0]
            if(str(sessionIdValue[0]) != 'None'):
               msg = "User is already logged In"
               print msg
            else:
               #Now verify credentials
               verify_password = ("select password from data.users where Email='"+email+"'")
               cursor.execute(verify_password)
               DBPassword = cursor.fetchone()
               DBPassword = DBPassword[0]
               if(decrypt_password(DBPassword)==password):
                  #Activation for first login - in fact I will update everytime this flag
                  update_ActiveFlag = ("update data.users set activeFlag='true', activeCode=NULL where Email='"+email+"'")
                  cursor.execute(update_ActiveFlag)
                  cnx.commit()
                  #Update SessionId
                  update_SessionId = ("update data.users set sessionID='"+sessionId+"' where Email='"+email+"'")
                  cursor.execute(update_SessionId)
                  cnx.commit()
                  #and the rest
                  select_userName = ("select name from data.users where Email='"+email+"'")
                  cursor.execute(select_userName)
                  Name = cursor.fetchone()
                  msg = Name[0]
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

        insert_NewSubscriber = ("BEGIN IF NOT EXISTS (SELECT * FROM [data].[subscribeList] WHERE email = '"+email+"') "
                                "BEGIN INSERT INTO [data].[subscribeList] (Email) VALUES ('"+email+"') "
                                "END END")
        cursor.execute(insert_NewSubscriber)
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
        if((cursor.execute("select count(1) from data.HD_name where name = '"+objectName+"'").fetchone())[0]>0):

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.HD_name hdn join data.HD hd on hdn.hd=hd.hd where hdn.name = '"+objectName+"'")
            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
               if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                   calc = str(float(HD[4].strip())-float(HD[3].strip()))
               else:
                   calc = " "
               details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
               controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.HD_name hdn join data.HR hr on hdn.hd=hr.hd where hdn.name = '"+objectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
               if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                   calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                   calcU = str(float(HR[6].strip())+float(HR[3].strip()))
               else:
                   calcB = " "
                   calcU = " "
               details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
               controller = str(details) + ',' + controller

            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.HD_name hdn join data.HR hr on hdn.hd=hr.hd join data.GC gc on hr.hd=gc.hd where hdn.name = '"+objectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.HD_name hdn join data.HR hr on hdn.hd=hr.hd join data.SAO sao on hr.hd=sao.hd where hdn.name = '"+objectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
               if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                   calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
               else:
                   calc = " "
               details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
               controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.HD_name hdn join data.tyc2_HD tychd on tychd.hd=hdn.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                          " and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 where hdn.name = '"+objectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
               if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                   calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
               else:
                   calc = " "
               details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
               controller = str(details) + ',' + controller

            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.HD_name hdn join data.tyc2_HD tychd on tychd.hd=hdn.hd join data.TYC2 tyc on "
                          " tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 join data.hip hip on hip.HIP=tyc.HIP where hdn.name = '"+objectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif (objectName[:2]=='HD' and (cursor.execute("select count(1) from data.HD where hd = '"+objectName[2:]+"'").fetchone())[0]>0):
            hdObjectName = objectName[2:]

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.HD_name hdn join data.HD hd on hdn.hd=hd.hd where hd.hd = '"+hdObjectName+"'")
            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.HD hd join data.HR hr on hd.hd=hr.hd where hd.hd = '"+hdObjectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.HD hd join data.GC gc on hd.hd=gc.hd where hd.hd = '"+hdObjectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.HD hd join data.SAO sao on hd.hd=sao.hd where hd.hd = '"+hdObjectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.HD hd join data.tyc2_HD tychd on tychd.hd=hd.hd "
                           "join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 where hd.hd = '"+hdObjectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.HD hd join data.tyc2_HD tychd on tychd.hd=hd.hd "
                          "join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                          "join data.hip hip on hip.HIP=tyc.HIP where hd.hd = '"+hdObjectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif (objectName[:2]=='HR' and (cursor.execute("select count(1) from data.HR where hr = '"+objectName[2:]+"'").fetchone())[0]>0):
            hrObjectName = objectName[2:]

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.HR hr join data.HD hd on hd.hd=hr.hd where hr.hr = '"+hrObjectName+"'")
            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.HR hr where hr.hr = '"+hrObjectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.HR hr join data.HD hd on hd.hd=hr.hd join data.GC gc on hd.hd=gc.hd where hr.hr = '"+hrObjectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.HR hr join data.HD hd on hd.hd=hr.hd join data.SAO sao on hd.hd=sao.hd where hr.hr = '"+hrObjectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.HR hr join data.HD hd on hd.hd=hr.hd "
                           "join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 "
                           "and tychd.TYC3=tyc.TYC3 where hr.hr = '"+hrObjectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller


            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.HR hr join data.HD hd on hd.hd=hr.hd join data.tyc2_HD tychd on tychd.hd=hd.hd "
                          "join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                          "join data.hip hip on hip.HIP=tyc.HIP where hr.hr = '"+hrObjectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif ((cursor.execute("select count(1) from data.HR where name = '"+objectName+"'").fetchone())[0]>0):

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.HR hr join data.HD hd on hd.hd=hr.hd where hr.name = '"+objectName+"'")
            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.HR hr where hr.name = '"+objectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.HR hr join data.HD hd on hd.hd=hr.hd join data.GC gc on hd.hd=gc.hd where hr.name = '"+objectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.HR hr join data.HD hd on hd.hd=hr.hd join data.SAO sao on hd.hd=sao.hd where hr.name = '"+objectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.HR hr join data.HD hd on hd.hd=hr.hd "
                           "join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 "
                           "and tychd.TYC3=tyc.TYC3 where hr.name = '"+objectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller


            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.HR hr join data.HD hd on hd.hd=hr.hd join data.tyc2_HD tychd on tychd.hd=hd.hd "
                          "join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                          "join data.hip hip on hip.HIP=tyc.HIP where hr.name = '"+objectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif (objectName[:2]=='GC' and (cursor.execute("select count(1) from data.GC where gc = '"+objectName[2:]+"'").fetchone())[0]>0):
            gcObjectName = objectName[2:]

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.GC gc join data.HD hd on hd.hd=gc.hd where gc.gc = '"+gcObjectName+"'")
            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.GC gc "
                         "join data.HD hd on hd.hd=gc.hd join data.HR hr on hr.hd=hd.hd where gc.gc = '"+gcObjectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller


            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.GC gc where gc.gc = '"+gcObjectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.GC gc join data.HD hd on hd.hd=gc.hd "
                          "join data.SAO sao on hd.hd=sao.hd where gc.gc = '"+gcObjectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.GC gc "
                           "join data.HD hd on hd.hd=gc.hd join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                           "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 where gc.gc = '"+gcObjectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller


            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.GC gc "
                          "join data.HD hd on hd.hd=gc.hd join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                          "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 join data.hip hip on hip.HIP=tyc.HIP "
                          "where gc.gc = '"+gcObjectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif (objectName[:3]=='SAO' and (cursor.execute("select count(1) from data.SAO where sao = '"+objectName[3:]+"'").fetchone())[0]>0):
            saoObjectName = objectName[3:]

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.SAO sao "
                         "join data.HD hd on hd.hd=sao.hd where sao.sao = '"+saoObjectName+"'")
            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.SAO sao "
                         "join data.HD hd on hd.hd=sao.hd join data.HR hr on hr.hd=hd.hd where sao.sao = '"+saoObjectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.SAO sao join data.HD hd on hd.hd=sao.hd "
                         "join data.GC gc on gc.hd=hd.hd where sao.sao = '"+saoObjectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.SAO sao "
                          "where sao.sao = '"+saoObjectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.SAO sao "
                           "join data.HD hd on hd.hd=sao.hd join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                           "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 where sao.sao = '"+saoObjectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller


            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.SAO sao "
                          "join data.HD hd on hd.hd=sao.hd join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                          "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 join data.hip hip on hip.HIP=tyc.HIP where sao.sao = '"+saoObjectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif (objectName[:3]=='HIP' and (cursor.execute("select count(1) from data.HIP where hip = '"+objectName[3:]+"'").fetchone())[0]>0):
            hipObjectName = objectName[3:]

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.HD hd join data.tyc2_HD tychd on tychd.hd=hd.hd "
                         "join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                         "join data.hip hip on hip.HIP=tyc.HIP where hip.hip = '"+hipObjectName+"'")
            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.HR hr "
                         "join data.HD hd on hd.hd=hr.hd join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                         "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 join data.hip hip on hip.HIP=tyc.HIP where hip.hip = '"+hipObjectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.GC gc join data.HD hd on hd.hd=gc.hd "
                         "join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 "
                         "and tychd.TYC3=tyc.TYC3 join data.hip hip on hip.HIP=tyc.HIP where hip.hip = '"+hipObjectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.SAO sao "
                          "join data.HD hd on hd.hd=sao.hd join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                          "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 join data.hip hip on hip.HIP=tyc.HIP where hip.hip = '"+hipObjectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.tyc2_HD tychd "
                           "join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                           "join data.hip hip on hip.HIP=tyc.HIP where hip.hip = '"+hipObjectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller


            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.hip hip "
                          "where hip.hip = '"+hipObjectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif (objectName[:3]=='TYC' and (cursor.execute("select count(1) from data.TYC2 "
            "where TYC1 = '"+tyc1ObjectName+"' and TYC2 = '"+tyc2ObjectName+"' and TYC3 = '"+tyc3ObjectName+"'").fetchone())[0]>0):

            select_hd = ("select distinct hd.RAJ2000, hd.DEJ2000, hd.HD, hd.Ptm, hd.Ptg, hd.SpT from data.HD hd "
                         "join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                         "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                         "where tyc.TYC1 = '"+tyc1ObjectName+"' and tyc.TYC2 = '"+tyc2ObjectName+"' and tyc.TYC3 = '"+tyc3ObjectName+"'")

            HD = cursor.execute(select_hd).fetchone()
            if(HD): #if record exists
                if(HD[4].strip() != "" and HD[3].strip() != ""): #if columns are not null
                    calc = str(float(HD[4].strip())-float(HD[3].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(HD[0].strip(), HD[1].strip(), "HD", str(HD[2]), " ", HD[3].strip(), HD[4].strip(), calc, " ", " ", " ", HD[5].strip())
                controller = str(details) + ',' + controller

            select_hr = ("select distinct hr.RAJ2000, hr.DEJ2000, hr.HR, hr.Vmag, hr.SpType, hr.B_V, hr.U_B, hr.R_I from data.HR hr "
                         "join data.HD hd on hd.hd=hr.hd join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 "
                         "and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                         "where tyc.TYC1 = '"+tyc1ObjectName+"' and tyc.TYC2 = '"+tyc2ObjectName+"' and tyc.TYC3 = '"+tyc3ObjectName+"'")
            HR = cursor.execute(select_hr).fetchone()
            if(HR):
                if(HR[5].strip() != "" and HR[3].strip() != "" and HR[6].strip() != ""):
                    calcB = str(float(HR[5].strip())+float(HR[3].strip()))
                    calcU = str(float(HR[6].strip())+float(HR[3].strip()))
                else:
                    calcB = " "
                    calcU = " "
                details = calculate_starsParameters(HR[0].strip(), HR[1].strip(), "HR", str(HR[2]), calcU, HR[3].strip(), calcB, HR[5].strip(), HR[6].strip(), HR[7].strip(), " ", HR[4].strip())
                controller = str(details) + ',' + controller

            select_gc = ("select distinct gc.RAJ2000, gc.DEJ2000, gc.GC, gc.Vmag, gc.SpType from data.GC gc join data.HD hd on hd.hd=gc.hd "
                         "join data.tyc2_HD tychd on tychd.hd=hd.hd join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                         "where tyc.TYC1 = '"+tyc1ObjectName+"' and tyc.TYC2 = '"+tyc2ObjectName+"' and tyc.TYC3 = '"+tyc3ObjectName+"'")
            GC = cursor.execute(select_gc).fetchone()
            details = calculate_starsParameters(GC[0].strip(), GC[1].strip(), "GC", str(GC[2]), " ", GC[3].strip(), " ", " ", " ", " ", " ", GC[4].strip())
            controller = str(details) + ',' + controller

            select_sao = ("select distinct sao.RAJ2000, sao.DEJ2000, sao.SAO, sao.Pmag, sao.Vmag, sao.SpType from data.SAO sao "
                          "join data.HD hd on hd.hd=sao.hd join data.tyc2_HD tychd on tychd.hd=hd.hd "
                          "join data.TYC2 tyc on tychd.TYC1=tyc.TYC1 and tychd.TYC2=tyc.TYC2 and tychd.TYC3=tyc.TYC3 "
                          "where tyc.TYC1 = '"+tyc1ObjectName+"' and tyc.TYC2 = '"+tyc2ObjectName+"' and tyc.TYC3 = '"+tyc3ObjectName+"'")
            SAO = cursor.execute(select_sao).fetchone()
            if(SAO):
                if(SAO[3].strip() != "" and SAO[4].strip() != ""):
                    calc = str(float(SAO[3].strip())-float(SAO[4].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(SAO[0].strip(), SAO[1].strip(), "SAO", str(SAO[2]), " ", SAO[4].strip(), SAO[3].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller

            select_tyc2 = ("select distinct tyc.RAJ2000, tyc.DEJ2000, tyc.TYC1, tyc.TYC2, tyc.TYC3, tyc.BTmag, tyc.VTmag from data.TYC2 tyc "
                           "where tyc.TYC1 = '"+tyc1ObjectName+"' and tyc.TYC2 = '"+tyc2ObjectName+"' and tyc.TYC3 = '"+tyc3ObjectName+"'")
            TYC2 = cursor.execute(select_tyc2).fetchone()
            if(TYC2):
                if(TYC2[5].strip() != "" and TYC2[6].strip() != ""):
                    calc = str(float(TYC2[5].strip())-float(TYC2[6].strip()))
                else:
                    calc = " "
                details = calculate_starsParameters(TYC2[0].strip(), TYC2[1].strip(), "TYC", str(TYC2[2])+"-"+str(TYC2[3])+"-"+str(TYC2[4]), " ", TYC2[6].strip(), TYC2[5].strip(), calc, " ", " ", " ", " ")
                controller = str(details) + ',' + controller


            select_hip = ("select distinct hip.RAJ2000, hip.DEJ2000, hip.HIP, hip.Hpmag, hip.B_V, hip.V_I from data.TYC2 tyc "
                          "join data.hip hip on hip.HIP=tyc.HIP "
                          "where tyc.TYC1 = '"+tyc1ObjectName+"' and tyc.TYC2 = '"+tyc2ObjectName+"' and tyc.TYC3 = '"+tyc3ObjectName+"'")
            HIP = cursor.execute(select_hip).fetchone()
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
        elif ((cursor.execute("select count(1) from data.comets where ltrim(rtrim(name)) = '"+objectName+"'").fetchone())[0]>0):
            select_comet = ("select Name, OrbitType, P_Year, P_Month, P_Day, P_Distance, e, Perihelion, Longitude, Inclination, "
                         "E_Year, E_Month, E_Day, Abs_Mag from data.comets where ltrim(rtrim(name)) = '"+objectName+"'")

            COMET = cursor.execute(select_comet).fetchone()
            if(COMET): #if record exists
                details = calculate_cometsParameters(COMET[0].strip(), COMET[1].strip(), COMET[2].strip()+" "+COMET[3].strip()+" "+COMET[4].strip(),
                                                     COMET[5].strip(), COMET[6].strip(), COMET[7].strip(), COMET[8].strip(), COMET[9].strip(),
                                                     COMET[10].strip()+COMET[11].strip()+COMET[12].strip(), COMET[13].strip())
                controller = str(details) + ',' + controller

            controller = ast.literal_eval(controller[:-1])
            controller = json.dumps(controller, skipkeys=True)
            json_string = [json.loads(controller)]

        #Planetoids
        elif ((cursor.execute("select count(1) from data.mpc where ltrim(rtrim(name)) = '"+objectName+"'").fetchone())[0]>0):

            select_planetoid = ("select Name, Number, H, Epoch, M, Perihelion, Node, Inclination, e, n, a from data.mpc"
                                " where ltrim(rtrim(name)) = '"+objectName+"'")

            PL = cursor.execute(select_planetoid).fetchone()
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
           get_BVObservationsDifference = (queries.get('DatabaseQueries', 'database.getBVObservationsDifferenceFromBVDiagramAvgForStar') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
           BVObservationsDifference = fetch_all(get_BVObservationsDifference)
           #U-B
           get_UBObservationsDifference = (queries.get('DatabaseQueries', 'database.getUBObservationsDifferenceFromUBDiagramAvgForStar') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
           UBObservationsDifference = fetch_all(get_UBObservationsDifference)
           #R-I
           get_RIObservationsDifference = (queries.get('DatabaseQueries', 'database.getRIObservationsDifferenceFromRIDiagramAvgForStar') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
           RIObservationsDifference = fetch_all(get_RIObservationsDifference)
           #V-I
           get_VIObservationsDifference = (queries.get('DatabaseQueries', 'database.getVIObservationsDifferenceFromVIDiagramAvgForStar') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
           VIObservationsDifference = fetch_all(get_VIObservationsDifference)


        #U
        get_UObservations = (queries.get('DatabaseQueries', 'database.getUObservationsFromUPhotometrySortedForObjectType') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
        UObservations = fetch_all(get_UObservations)
        #V
        get_VObservations = (queries.get('DatabaseQueries', 'database.getVObservationsFromVPhotometrySortedForObjectType') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
        VObservations = fetch_all(get_VObservations)
        #B
        get_BObservations = (queries.get('DatabaseQueries', 'database.getBObservationsFromBPhotometrySortedForObjectType') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
        BObservations = fetch_all(get_BObservations)
        #R
        get_RObservations = (queries.get('DatabaseQueries', 'database.getRObservationsFromRPhotometrySortedForObjectType') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
        RObservations = fetch_all(get_RObservations)
        #I
        get_IObservations = (queries.get('DatabaseQueries', 'database.getIObservationsFromIPhotometrySortedForObjectType') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
        IObservations = fetch_all(get_IObservations)
        #ObjectNames
        get_ObjectNames = (queries.get('DatabaseQueries', 'database.getObjectNamesForCatalog') + " where ob.ObjectType='" + objectType + "' and email='" + email + "' group by ob.ObjectName")
        ObjectNames = fetch_all(get_ObjectNames)
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

        #specialCharacterPosition = files.index('.') + 1
        #fileExtension = str(files[specialCharacterPosition:])
        fileExtension = 'fits'

        get_lastId = queries.get('DatabaseQueries', 'database.getLastIdFromDataImages')
        cursor.execute(get_lastId)
        lastId = cursor.fetchone()
        if lastId is None:
            lastId = 1
        else:
            lastId = lastId[0] + 1

        counter = lastId


        #--Insert to data.images
        for file in files:
            objectName = file
            lastId = str(counter)

            verifyFileExists = (queries.get('DatabaseQueries', 'database.getNumberOfImagesInDataImages') + "'"+objectName+"' "
                                            "and im.sessionId = "+sessionId+" and co.conversionType = '"+conversionType+"' and it.ImageType = '"+imageType+"'")

            cursor.execute(verifyFileExists)
            existsFlag = cursor.fetchone()

            if (existsFlag[0] == 0):
               print 'fits does not exist in DB'
               insertImage = (queries.get('DatabaseQueries', 'database.insertIntoDataReductionImages')+
                              " values("+lastId+", 1, (select id from data.users where email='"+email+"'),"
                              "(select fileExtensionId from dic.FileExtensions where FileExtension = '"+fileExtension+"'), "
                              "'"+sessionId+"', (select ConversionTypeId from dic.ConversionTypes where ConversionType='"+conversionType+"'),"
                              "(select ImageTypeId from dic.ImageTypes where ImageType='"+imageType+"'),'"+objectName+"', 'inputFits', "
                              "'Reduction', getdate())")

               cursor.execute(insertImage)
               cnx.commit()
               looper=1
               while(looper<100):
                  time.sleep(1)
                  if os.path.isfile(backendInputFits+objectName):
                      break
                  else:
                      print 'continue fits does not exist in DB'
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
            else:
                print 'fits exists in DB'
                looper=1
                while(looper<100):
                    time.sleep(1)
                    if os.path.isfile(backendInputFits+objectName):
                        break
                    else:
                        print 'continue fits exists in DB'
                        looper = looper + 1
                        continue
            #start conversion
            print 'Start Conversion'
            specialCharacterPosition = objectName.index('.')
            replaceString = sessionId+"_"+imageType+"_"+str(objectName[:specialCharacterPosition])
            convertPlots.plot(replaceString, conversionType)
            #end conversion

            #Add converted file to DB
            convertedObjectName = conversionType+"_"+replaceString+".png"
            verifyConvertedFileExists = (queries.get('DatabaseQueries', 'database.getNumberOfImagesInDataImages') + "'"+convertedObjectName+"' "
                                            "and sessionId = "+sessionId+"")
            cursor.execute(verifyConvertedFileExists)
            existsConvertedFlag = cursor.fetchone()

            if (existsConvertedFlag[0] == 0):
               counter = counter + 1
               lastId = str(counter)
               #print 'png does not exist in DB'
               insertImage = (queries.get('DatabaseQueries', 'database.insertIntoDataReductionImages')+
                           "values("+lastId+", 1, (select id from data.users where email='"+email+"'),"
                           "(select fileExtensionId from dic.FileExtensions where FileExtension = 'png'), "
                           "'"+sessionId+"', (select ConversionTypeId from dic.ConversionTypes where ConversionType='"+conversionType+"'),"
                           "(select ImageTypeId from dic.ImageTypes where ImageType='"+imageType+"'),'"+convertedObjectName+"', 'inputFits', "
                           "'Reduction', getdate())")
               cursor.execute(insertImage)
               cnx.commit()
            counter = counter + 1
        else:
           print 'png already exists in DB'



        #return json value
        get_ImageIds = (queries.get('DatabaseQueries', 'database.getImageIds') + sessionId + " and im.FileExtensionId=2 and co.conversionType='"+conversionType+"' and it.ImageType = '"+imageType+"'")
        #print get_ImageIds
        get_FileNames = (queries.get('DatabaseQueries', 'database.getFileNames') + sessionId + " and FileExtensionId=2 and co.conversionType='"+conversionType+"' and it.ImageType = '"+imageType+"'")
        #print get_FileNames
        data = {'imageIds': fetch_all(get_ImageIds), 'fileNames': fetch_all(get_FileNames)}
        #print data
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
        getDarkFrames = (queries.get('DatabaseQueries', 'database.getDarkFrames') + sessionId)
        getBiasFrames = (queries.get('DatabaseQueries', 'database.getBiasFrames') + sessionId)
        getFlatFields = (queries.get('DatabaseQueries', 'database.getFlatFields') + sessionId)
        getRawFrames = (queries.get('DatabaseQueries', 'database.getRawFrames') + sessionId)


        reduceImages.reduce(fetch_all(getDarkFrames), fetch_all(getBiasFrames), fetch_all(getFlatFields), fetch_all(getRawFrames), sessionId)

        rawImages = fetch_all(getRawFrames)
        print rawImages
        counter = lastId
        for file in rawImages:
           print 'tutaj'
           print file
           lastId = str(counter)
           counter = counter + 1
           insertFitsImage = "insert into data.images(ID, ImageId, OwnerID, FileExtensionId, SessionId, ConversionTypeId, ImageTypeId, ObjectName, FolderName, ProcessingType, UploadTime) " \
                             "values('"+lastId+"', 1, (select id from data.users where email='"+email+"'), 3, '"+sessionId+"', 1, 5, '"+file+"', 'outputFits', 'Reduction', getdate())"

           print insertFitsImage
           cursor.execute(insertFitsImage)
           cnx.commit()
           print 'helow'
           lastId = str(counter)
           counter = counter + 1
           specialCharacterPosition = file.index('.')
           objectName = str(file[:specialCharacterPosition])
           objectName = "Linear_"+sessionId+"_Processed_"+objectName+".png"
           insertPngImage = (queries.get('DatabaseQueries', 'database.insertIntoDataReductionImages')+
                              " values('"+lastId+"', 1, (select id from data.users where email='"+email+"'),"
                              "2, '"+sessionId+"', 1, 5, '"+objectName+"', 'outputFits', 'Reduction', getdate())")
           cursor.execute(insertPngImage)
           cnx.commit()

        #return json value
        get_ImageIds = (queries.get('DatabaseQueries', 'database.getImageIds') + sessionId + " and im.FileExtensionId=2 and co.conversionType='Linear' and it.ImageType = 'Processed'")
        #print get_ImageIds
        get_FileNames = (queries.get('DatabaseQueries', 'database.getFileNames') + sessionId + " and FileExtensionId=2 and co.conversionType='Linear' and it.ImageType = 'Processed'")
        #print get_FileNames
        data = {'imageIds': fetch_all(get_ImageIds), 'fileNames': fetch_all(get_FileNames)}
        #print data
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
        getImages = (queries.get('DatabaseQueries', 'database.getImages') + sessionId)


        data = zipFiles.zipAll(fetch_all(getImages), sessionId)

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