import sys
import pyodbc
import os
import ConfigParser
import pandas


globalPath = 'C:/Users/Przemek/Desktop/arqonia/backend'
catalogsPath = 'C:/Users/Przemek/Downloads/catalogs/'

config = ConfigParser.RawConfigParser()
config.read(globalPath+'/resources/env.properties')
dbAddress = config.get('DatabaseConnection', 'database.address');
queries = ConfigParser.RawConfigParser()
queries.read(globalPath+'/resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()

def gc_catalog():
   try:
       cnx = pyodbc.connect(dbAddress)
       cursor = cnx.cursor()
       gc = pandas.read_csv(catalogsPath+'GC.csv', header=None, sep=';', low_memory=False)
       gcRange = len(gc)

       gc.columns = ["GlonJ2000","GlatJ2000","RAJ2000","DEJ2000","GC","Vmag","SpType",
                     "RA1950","EpRA","pmRA","DE1950","EpDE","pmDE","Remark","DM","GLON",
                     "GLAT","HD","m_HD","e_RA","e_pmRA","e_DE","e_pmDE","RA_icrs","DE_icrs"]


       insert_data = ''
       for counter in range(0,gcRange):
           i = counter
           GlonJ2000 = str(gc.GlonJ2000[i])
           GlatJ2000 = str(gc.GlatJ2000[i])
           RAJ2000 = str(gc.RAJ2000[i])
           DEJ2000 = str(gc.DEJ2000[i])
           GC = str(gc.GC[i])
           Vmag = str(gc.Vmag[i])
           SpType = str(gc.SpType[i])
           RA1950 = str(gc.RA1950[i])
           EpRA = str(gc.EpRA[i])
           pmRA = str(gc.pmRA[i])
           DE1950 = str(gc.DE1950[i])
           EpDE = str(gc.EpDE[i])
           pmDE = str(gc.pmDE[i])
           Remark = str(gc.Remark[i])
           DM = str(gc.DM[i])
           GLON = str(gc.GLON[i])
           GLAT = str(gc.GLAT[i])
           HD = str(gc.HD[i])
           m_HD = str(gc.m_HD[i])
           e_RA = str(gc.e_RA[i])
           e_pmRA = str(gc.e_pmRA[i])
           e_DE = str(gc.e_DE[i])
           e_pmDE = str(gc.e_pmDE[i])
           RA_icrs = str(gc.RA_icrs[i])
           DE_icrs = str(gc.DE_icrs[i])

           #single insert
           insert_data = "INSERT INTO data.gc " \
                         "values ('"+GlonJ2000+"','"+GlatJ2000+"','"+RAJ2000+"','"+DEJ2000+"','"+GC+"','"+Vmag+"','"+SpType+"','"+RA1950+"'," \
                             "'"+EpRA+"','"+pmRA+"','"+DE1950+"','"+EpDE+"','"+pmDE+"','"+Remark+"',ltrim(rtrim('"+DM+"')),'"+GLON+"'," \
                         "'"+GLAT+"',ltrim(rtrim('"+HD+"')),'"+m_HD+"','"+e_RA+"','"+e_pmRA+"','"+e_DE+"','"+e_pmDE+"','"+RA_icrs+"','"+DE_icrs+"')"

           print i
           cursor.execute(insert_data)
           cnx.commit()

       cursor.close()

   except:
       print 'errors in gc_catalog function'
   else:
       cnx.close()



def hd_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        hd = pandas.read_csv(catalogsPath+'HD.csv', header=None, sep=';', low_memory=False)
        hdRange = len(hd)

        hd.columns = ["GlonJ1900","GlatJ1900","RAJ2000","DEJ2000","HD","DM","RAB1900",
                      "DEB1900","q_Ptm","Ptm","n_Ptm","q_Ptg","Ptg","n_Ptg","SpT","Int",
                      "Rem","RA_icrs","DE_icrs","Tycho2"]


        insert_data = ''
        for counter in range(0,hdRange):
            i = counter
            GlonJ1900 = str(hd.GlonJ1900[i])
            GlatJ1900 = str(hd.GlatJ1900[i])
            RAJ2000 = str(hd.RAJ2000[i])
            DEJ2000 = str(hd.DEJ2000[i])
            HD = str(hd.HD[i])
            DM = str(hd.DM[i])
            RAB1900 = str(hd.RAB1900[i])
            DEB1900 = str(hd.DEB1900[i])
            q_Ptm = str(hd.q_Ptm[i])
            Ptm = str(hd.Ptm[i])
            n_Ptm = str(hd.n_Ptm[i])
            q_Ptg = str(hd.q_Ptg[i])
            Ptg = str(hd.Ptg[i])
            n_Ptg = str(hd.n_Ptg[i])
            SpT = str(hd.SpT[i])
            Int = str(hd.Int[i])
            Rem = str(hd.Rem[i])
            RA_icrs = str(hd.RA_icrs[i])
            DE_icrs = str(hd.DE_icrs[i])
            Tycho2 = str(hd.Tycho2[i])

            #single insert
            insert_data = "INSERT INTO data.hd (GlonJ1900,GlatJ1900,RAJ2000,DEJ2000,HD,DM,RAB1900," \
                          "DEB1900,q_Ptm,Ptm,n_Ptm,q_Ptg,Ptg,n_Ptg,SpT,Int," \
                          "Rem,RA_icrs,DE_icrs,Tycho2)" \
                          " values ('"+GlonJ1900+"','"+GlatJ1900+"','"+RAJ2000+"','"+DEJ2000+"',ltrim(rtrim('"+HD+"')),ltrim(rtrim('"+DM+"')),'"+RAB1900+"','"+DEB1900+"'," \
                                  "'"+q_Ptm+"','"+Ptm+"','"+n_Ptm+"','"+q_Ptg+"','"+Ptg+"','"+n_Ptg+"','"+SpT+"','"+Int+"'," \
                                  "'"+Rem+"','"+RA_icrs+"','"+DE_icrs+"','"+Tycho2+"')"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in hd_catalog function'
    else:
        cnx.close()


def hip_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        hip = pandas.read_csv(catalogsPath+'HIP.csv', header=None, sep=';', low_memory=False)
        hipRange = len(hip)

        hip.columns = ["GlonJ2000","GlatJ2000","RAJ2000","DEJ2000","HIP","n_HIP","Sn","So","Nc","RArad","e_RArad",
                       "DErad","e_DErad","Plx","e_Plx","pmRA","e_pmRA","pmDE","e_pmDE","Ntr","F2","F1",
                       "varr","Hpmag","e_Hpmag","sHp","VA","B_V","e_B_V","V_I","HIP1","Phot"]


        insert_data = ''
        for counter in range(0,hipRange):
            i = counter
            GlonJ2000 = str(hip.GlonJ2000[i])
            GlatJ2000 = str(hip.GlatJ2000[i])
            RAJ2000 = str(hip.RAJ2000[i])
            DEJ2000 = str(hip.DEJ2000[i])
            HIP = str(hip.HIP[i])
            n_HIP = str(hip.n_HIP[i])
            Sn = str(hip.Sn[i])
            So = str(hip.So[i])
            Nc = str(hip.Nc[i])
            RArad = str(hip.RArad[i])
            e_RArad = str(hip.e_RArad[i])
            DErad = str(hip.DErad[i])
            e_DErad = str(hip.e_DErad[i])
            Plx = str(hip.Plx[i])
            e_Plx = str(hip.e_Plx[i])
            pmRA = str(hip.pmRA[i])
            e_pmRA = str(hip.e_pmRA[i])
            pmDE = str(hip.pmDE[i])
            e_pmDE = str(hip.e_pmDE[i])
            Ntr = str(hip.Ntr[i])
            F2 = str(hip.F2[i])
            F1 = str(hip.F1[i])
            varr = str(hip.varr[i])
            Hpmag = str(hip.Hpmag[i])
            e_Hpmag = str(hip.e_Hpmag[i])
            sHp = str(hip.sHp[i])
            VA = str(hip.VA[i])
            B_V = str(hip.B_V[i])
            e_B_V = str(hip.e_B_V[i])
            V_I = str(hip.V_I[i])
            HIP1 = str(hip.HIP1[i])
            Phot = str(hip.Phot[i])

            #single insert
            insert_data = "INSERT INTO data.hip " \
                          " values ('"+GlonJ2000+"','"+GlatJ2000+"','"+RAJ2000+"','"+DEJ2000+"',ltrim(rtrim('"+HIP+"')),'"+n_HIP+"','"+Sn+"','"+So+"'," \
                                   "'"+Nc+"','"+RArad+"','"+e_RArad+"','"+DErad+"','"+e_DErad+"','"+Plx+"','"+e_Plx+"','"+pmRA+"'," \
                                   "'"+e_pmRA+"','"+pmDE+"','"+e_pmDE+"','"+Ntr+"','"+F2+"','"+F1+"','"+varr+"','"+Hpmag+"'," \
                                   "'"+e_Hpmag+"','"+sHp+"','"+VA+"','"+B_V+"','"+e_B_V+"','"+V_I+"','"+HIP1+"','"+Phot+"')"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in hip_catalog function'
    else:
        cnx.close()


def hr_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        hr = pandas.read_csv(catalogsPath+'HR.csv', header=None, sep=';', low_memory=False)
        hrRange = len(hr)

        hr.columns = ["GlonJ2000","GlatJ2000","RAJ2000","DEJ2000","HR","Name","DM","HD","SAO","FK5","IRflag","r_IRflag",
                      "Multiple","ADS","ADScomp","VarID","RAJ2000_original","DEJ2000_original","GLON","GLAT","Vmag",
                      "n_Vmag","u_Vmag","B_V","u_B_V","U_B","u_U_B","R_I","n_R_I","SpType","n_SpType","pmRA","pmDE",
                      "n_Parallax","Parallax","RadVel","n_RadVel","l_RotVel","RotVel","u_RotVel","Dmag","Sep","MultID","MultCnt","NoteFlag"]


        insert_data = ''
        for counter in range(0,hrRange):
            insert_data = ''
            i = counter
            GlonJ2000 = str(hr.GlonJ2000[i])
            GlatJ2000 = str(hr.GlatJ2000[i])
            RAJ2000 = str(hr.RAJ2000[i])
            DEJ2000 = str(hr.DEJ2000[i])
            HR = str(hr.HR[i])
            Name = str(hr.Name[i])
            DM = str(hr.DM[i])
            HD = str(hr.HD[i])
            SAO = str(hr.SAO[i])
            FK5 = str(hr.FK5[i])
            IRflag = str(hr.IRflag[i])
            r_IRflag = str(hr.r_IRflag[i])
            Multiple = str(hr.Multiple[i])
            ADS = str(hr.ADS[i])
            ADScomp = str(hr.ADScomp[i])
            VarID = str(hr.VarID[i])
            RAJ2000_original = str(hr.RAJ2000_original[i])
            DEJ2000_original = str(hr.DEJ2000_original[i])
            GLON = str(hr.GLON[i])
            GLAT = str(hr.GLAT[i])
            Vmag = str(hr.Vmag[i])
            n_Vmag = str(hr.n_Vmag[i])
            u_Vmag = str(hr.u_Vmag[i])
            u_B_V = str(hr.u_B_V[i])
            U_B = str(hr.U_B[i])
            B_V = str(hr.B_V[i])
            u_U_B = str(hr.u_U_B[i])
            R_I = str(hr.R_I[i])
            n_R_I = str(hr.n_R_I[i])
            SpType = str(hr.SpType[i])
            n_SpType = str(hr.n_SpType[i])
            pmRA = str(hr.pmRA[i])
            pmDE = str(hr.pmDE[i])
            n_Parallax = str(hr.n_Parallax[i])
            Parallax = str(hr.Parallax[i])
            RadVel = str(hr.RadVel[i])
            n_RadVel = str(hr.n_RadVel[i])
            l_RotVel = str(hr.l_RotVel[i])
            RotVel = str(hr.RotVel[i])
            u_RotVel = str(hr.u_RotVel[i])
            Dmag = str(hr.Dmag[i])
            Sep = str(hr.Sep[i])
            MultID = str(hr.MultID[i])
            MultCnt = str(hr.MultCnt[i])
            NoteFlag = str(hr.NoteFlag[i])

            #single insert
            insert_data = "INSERT INTO data.hr " \
                          " values ('"+GlonJ2000+"','"+GlatJ2000+"','"+RAJ2000+"','"+DEJ2000+"',cast(ltrim(rtrim('"+HR+"')) as int),ltrim(rtrim('"+Name+"')),ltrim(rtrim('"+DM+"')),cast(ltrim(rtrim('"+HD+"')) as int),cast(ltrim(rtrim('"+SAO+"')) as int),'"+FK5+"','"+IRflag+"','"+r_IRflag+"'," \
                                   "'"+Multiple+"','"+ADS+"','"+ADScomp+"','"+VarID+"','"+RAJ2000_original+"','"+DEJ2000_original+"','"+GLON+"','"+GLAT+"','"+Vmag+"'," \
                                   "'"+n_Vmag+"','"+u_Vmag+"','"+B_V+"','"+u_B_V+"','"+U_B+"','"+u_U_B+"','"+R_I+"','"+n_R_I+"','"+SpType+"','"+n_SpType+"','"+pmRA+"','"+pmDE+"'," \
                                   "'"+n_Parallax+"','"+Parallax+"','"+RadVel+"','"+n_RadVel+"','"+l_RotVel+"','"+RotVel+"','"+u_RotVel+"','"+Dmag+"','"+Sep+"','"+MultID+"','"+MultCnt+"','"+NoteFlag+"')"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in hr_catalog function'
    else:
        cnx.close()


def sao_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        sao = pandas.read_csv(catalogsPath+'SAO.csv', header=None, sep=';', low_memory=False)
        saoRange = len(sao)

        sao.columns = ["GlonJ1950","GlatJ1950","RAJ2000","DEJ2000","SAO","delFlag","RAB1950","pmRA","e_pmRA","RA2mf",
                       "RA2s","e_RA2s","EpRA2","DEB1950","pmDE","e_pmDE","DE2mf","DE2s","e_DE2s","EpDE2","e_Pos","Pmag",
                       "Vmag","SpType","r_Vmag","r_Num","r_Pmag","r_pmRA","r_SpType","Rem","a_Vmag","a_Pmag","r_Cat",
                       "CatNum","DM","HD","m_HD","GC","RA2000","pmRA2000","DE2000","pmDE2000","RA_icrs","DE_icrs"]

        insert_data = ''
        for counter in range(0,saoRange):
            insert_data = ''
            i = counter
            print i
            GlonJ1950 = str(sao.GlonJ1950[i])
            GlatJ1950 = str(sao.GlatJ1950[i])
            RAJ2000 = str(sao.RAJ2000[i])
            DEJ2000 = str(sao.DEJ2000[i])
            SAO = str(sao.SAO[i])
            delFlag = str(sao.delFlag[i])
            RAB1950 = str(sao.RAB1950[i])
            pmRA = str(sao.pmRA[i])
            e_pmRA = str(sao.e_pmRA[i])
            RA2mf = str(sao.RA2mf[i])
            RA2s = str(sao.RA2s[i])
            EpRA2 = str(sao.EpRA2[i])
            e_RA2s = str(sao.e_RA2s[i])
            DEB1950 = str(sao.DEB1950[i])
            pmDE = str(sao.pmDE[i])
            e_pmDE = str(sao.e_pmDE[i])
            DE2mf = str(sao.DE2mf[i])
            DE2s = str(sao.DE2s[i])
            e_DE2s = str(sao.e_DE2s[i])
            EpDE2 = str(sao.EpDE2[i])
            e_Pos = str(sao.e_Pos[i])
            Pmag = str(sao.Pmag[i])
            Vmag = str(sao.Vmag[i])
            SpType = str(sao.SpType[i])
            r_Vmag = str(sao.r_Vmag[i])
            r_Num = str(sao.r_Num[i])
            r_Pmag = str(sao.r_Pmag[i])
            r_pmRA = str(sao.r_pmRA[i])
            r_SpType = str(sao.r_SpType[i])
            Rem = str(sao.Rem[i])
            a_Vmag = str(sao.a_Vmag[i])
            a_Pmag = str(sao.a_Pmag[i])
            r_Cat = str(sao.r_Cat[i])
            CatNum = str(sao.CatNum[i])
            DM = str(sao.DM[i])
            HD = str(sao.HD[i])
            m_HD = str(sao.m_HD[i])
            GC = str(sao.GC[i])
            RA2000 = str(sao.RA2000[i])
            pmRA2000 = str(sao.pmRA2000[i])
            DE2000 = str(sao.DE2000[i])
            pmDE2000 = str(sao.pmDE2000[i])
            RA_icrs = str(sao.RA_icrs[i])
            DE_icrs = str(sao.DE_icrs[i])

            #single insert
            insert_data = "INSERT INTO data.sao " \
                          " values ('"+GlonJ1950+"','"+GlatJ1950+"','"+RAJ2000+"','"+DEJ2000+"','"+SAO+"','"+delFlag+"','"+RAB1950+"'," \
                                   "'"+pmRA+"','"+e_pmRA+"','"+RA2mf+"','"+RA2s+"','"+e_RA2s+"','"+EpRA2+"','"+DEB1950+"','"+pmDE+"'," \
                                   "'"+e_pmDE+"','"+DE2mf+"','"+DE2s+"','"+e_DE2s+"','"+EpDE2+"','"+e_Pos+"','"+Pmag+"','"+Vmag+"'," \
                                   "'"+SpType+"','"+r_Vmag+"','"+r_Num+"','"+r_Pmag+"','"+r_pmRA+"','"+r_SpType+"','"+Rem+"'," \
                                   "'"+a_Vmag+"','"+a_Pmag+"','"+r_Cat+"','"+CatNum+"','"+DM+"','"+HD+"','"+m_HD+"','"+GC+"','"+RA2000+"'," \
                                   "'"+pmRA2000+"','"+DE2000+"','"+pmDE2000+"','"+RA_icrs+"','"+DE_icrs+"')"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in sao_catalog function'
    else:
        cnx.close()


def tyc2_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        tyc2 = pandas.read_csv(catalogsPath+'TYC2.csv', header=None, sep=';', low_memory=False)
        tyc2Range = len(tyc2)

        tyc2.columns = ["GlonJ2000","GlatJ2000","RAJ2000","DEJ2000","TYC1","TYC2","TYC3","pflag","RAmdeg","DEmdeg","pmRA",
                        "pmDE","e_RAmdeg","e_DEmdeg","e_pmRA","e_pmDE","EpRAm","EpDEm","Num","q_RAmdeg","q_DEmdeg","q_pmRA",
                        "q_pmDE","BTmag","e_BTmag","VTmag","e_VTmag","prox","TYC","HIP","CCDM","RAdeg","DEdeg",
                        "EpRA1990","EpDE1990","e_RAdeg","e_DEdeg","posflg","corr2"]

        insert_data = ''
        for counter in range(0,tyc2Range):
            insert_data = ''
            i = counter
            GlonJ2000 = str(tyc2.GlonJ2000[i])
            GlatJ2000 = str(tyc2.GlatJ2000[i])
            RAJ2000 = str(tyc2.RAJ2000[i])
            DEJ2000 = str(tyc2.DEJ2000[i])
            TYC1 = str(tyc2.TYC1[i])
            TYC2 = str(tyc2.TYC2[i])
            TYC3 = str(tyc2.TYC3[i])
            pflag = str(tyc2.pflag[i])
            RAmdeg = str(tyc2.RAmdeg[i])
            DEmdeg = str(tyc2.DEmdeg[i])
            pmRA = str(tyc2.pmRA[i])
            pmDE = str(tyc2.pmDE[i])
            e_RAmdeg = str(tyc2.e_RAmdeg[i])
            e_DEmdeg = str(tyc2.e_DEmdeg[i])
            e_pmRA = str(tyc2.e_pmRA[i])
            e_pmDE = str(tyc2.e_pmDE[i])
            EpRAm = str(tyc2.EpRAm[i])
            EpDEm = str(tyc2.EpDEm[i])
            Num = str(tyc2.Num[i])
            q_RAmdeg = str(tyc2.q_RAmdeg[i])
            q_DEmdeg = str(tyc2.q_DEmdeg[i])
            q_pmRA = str(tyc2.q_pmRA[i])
            q_pmDE = str(tyc2.q_pmDE[i])
            BTmag = str(tyc2.BTmag[i])
            e_BTmag = str(tyc2.e_BTmag[i])
            VTmag = str(tyc2.VTmag[i])
            e_VTmag = str(tyc2.e_VTmag[i])
            prox = str(tyc2.prox[i])
            TYC = str(tyc2.TYC[i])
            HIP = str(tyc2.HIP[i])
            CCDM = str(tyc2.CCDM[i])
            RAdeg = str(tyc2.RAdeg[i])
            DEdeg = str(tyc2.DEdeg[i])
            EpRA1990 = str(tyc2.EpRA1990[i])
            EpDE1990 = str(tyc2.EpDE1990[i])
            e_RAdeg = str(tyc2.e_RAdeg[i])
            e_DEdeg = str(tyc2.e_DEdeg[i])
            posflg = str(tyc2.posflg[i])
            corr2 = str(tyc2.corr2[i])

            #single insert
            insert_data = "INSERT INTO data.tyc2 " \
                          " values ('"+GlonJ2000+"','"+GlatJ2000+"','"+RAJ2000+"','"+DEJ2000+"',ltrim(rtrim('"+TYC1+"')),ltrim(rtrim('"+TYC2+"')),ltrim(rtrim('"+TYC3+"')),'"+pflag+"'," \
                                    "'"+RAmdeg+"','"+DEmdeg+"','"+pmRA+"','"+pmDE+"','"+e_RAmdeg+"','"+e_DEmdeg+"','"+e_pmRA+"','"+e_pmDE+"'," \
                                    "'"+EpRAm+"','"+EpDEm+"','"+Num+"','"+q_RAmdeg+"','"+q_DEmdeg+"','"+q_pmRA+"','"+q_pmDE+"','"+BTmag+"'," \
                                    "'"+e_BTmag+"','"+VTmag+"','"+e_VTmag+"','"+prox+"','"+TYC+"',ltrim(rtrim('"+HIP+"')),'"+CCDM+"','"+RAdeg+"','"+DEdeg+"'," \
                                    "'"+EpRA1990+"','"+EpDE1990+"','"+e_RAdeg+"','"+e_DEdeg+"','"+posflg+"','"+corr2+"')"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in tyc2_catalog function'
    else:
        cnx.close()


def tyc2_sup1_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        tyc2_sup1 = pandas.read_csv(catalogsPath+'TYC2_sup1.csv', header=None, sep=';', low_memory=False)
        tyc2_sup1Range = len(tyc2_sup1)
        tyc2_sup1.columns = ["GlonJ2000","GlatJ2000","RAJ2000","DEJ2000","TYC1","TYC2","TYC3","pflag","RAmdeg","DEmdeg","pmRA",
                             "pmDE","e_RAmdeg","e_DEmdeg","e_pmRA","e_pmDE","BTmag","e_BTmag","VTmag","e_VTmag","prox","TYC","HIP","CCDM"]

        insert_data = ''
        for counter in range(0,tyc2_sup1Range):
            insert_data = ''
            i = counter
            GlonJ2000 = str(tyc2_sup1.GlonJ2000[i])
            GlatJ2000 = str(tyc2_sup1.GlatJ2000[i])
            RAJ2000 = str(tyc2_sup1.RAJ2000[i])
            DEJ2000 = str(tyc2_sup1.DEJ2000[i])
            TYC1 = str(tyc2_sup1.TYC1[i])
            TYC2 = str(tyc2_sup1.TYC2[i])
            TYC3 = str(tyc2_sup1.TYC3[i])
            pflag = str(tyc2_sup1.pflag[i])
            RAmdeg = str(tyc2_sup1.RAmdeg[i])
            DEmdeg = str(tyc2_sup1.DEmdeg[i])
            pmRA = str(tyc2_sup1.pmRA[i])
            pmDE = str(tyc2_sup1.pmDE[i])
            e_RAmdeg = str(tyc2_sup1.e_RAmdeg[i])
            e_DEmdeg = str(tyc2_sup1.e_DEmdeg[i])
            e_pmRA = str(tyc2_sup1.e_pmRA[i])
            e_pmDE = str(tyc2_sup1.e_pmDE[i])
            BTmag = str(tyc2_sup1.BTmag[i])
            e_BTmag = str(tyc2_sup1.e_BTmag[i])
            VTmag = str(tyc2_sup1.VTmag[i])
            e_VTmag = str(tyc2_sup1.e_VTmag[i])
            prox = str(tyc2_sup1.prox[i])
            TYC = str(tyc2_sup1.TYC[i])
            HIP = str(tyc2_sup1.HIP[i])
            CCDM = str(tyc2_sup1.CCDM[i])

            #single insert
            insert_data = "INSERT INTO data.TYC2 (GlonJ2000,GlatJ2000,RAJ2000,DEJ2000,TYC1,TYC2,TYC3,pflag,RAmdeg,DEmdeg,pmRA," \
                                                      "pmDE,e_RAmdeg,e_DEmdeg,e_pmRA,e_pmDE,BTmag,e_BTmag,VTmag,e_VTmag,prox,TYC,HIP,CCDM)" \
                          " values ('"+GlonJ2000+"','"+GlatJ2000+"','"+RAJ2000+"','"+DEJ2000+"',ltrim(rtrim('"+TYC1+"')),ltrim(rtrim('"+TYC2+"')),ltrim(rtrim('"+TYC3+"')),'"+pflag+"'," \
                                     "'"+RAmdeg+"','"+DEmdeg+"','"+pmRA+"','"+pmDE+"','"+e_RAmdeg+"','"+e_DEmdeg+"','"+e_pmRA+"','"+e_pmDE+"'," \
                                     "'"+BTmag+"','"+e_BTmag+"','"+VTmag+"','"+e_VTmag+"','"+prox+"','"+TYC+"',ltrim(rtrim('"+HIP+"')),'"+CCDM+"')"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in tyc2_sup1_catalog function'
    else:
        cnx.close()


def tyc2_sup2_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        tyc2_sup2 = pandas.read_csv(catalogsPath+'TYC2_sup2.csv', header=None, sep=';', low_memory=False)
        tyc2_sup2Range = len(tyc2_sup2)

        tyc2_sup2.columns = ["GlonJ2000","GlatJ2000","RAJ2000","DEJ2000","TYC1","TYC2","TYC3","pflag","RAmdeg","DEmdeg","pmRA",
                             "pmDE","e_RAmdeg","e_DEmdeg","e_pmRA","e_pmDE","BTmag","e_BTmag","VTmag","e_VTmag","prox","TYC","HIP","CCDM"]

        insert_data = ''
        for counter in range(0,tyc2_sup2Range):
            insert_data = ''
            i = counter
            GlonJ2000 = str(tyc2_sup2.GlonJ2000[i])
            GlatJ2000 = str(tyc2_sup2.GlatJ2000[i])
            RAJ2000 = str(tyc2_sup2.RAJ2000[i])
            DEJ2000 = str(tyc2_sup2.DEJ2000[i])
            TYC1 = str(tyc2_sup2.TYC1[i])
            TYC2 = str(tyc2_sup2.TYC2[i])
            TYC3 = str(tyc2_sup2.TYC3[i])
            pflag = str(tyc2_sup2.pflag[i])
            RAmdeg = str(tyc2_sup2.RAmdeg[i])
            DEmdeg = str(tyc2_sup2.DEmdeg[i])
            pmRA = str(tyc2_sup2.pmRA[i])
            pmDE = str(tyc2_sup2.pmDE[i])
            e_RAmdeg = str(tyc2_sup2.e_RAmdeg[i])
            e_DEmdeg = str(tyc2_sup2.e_DEmdeg[i])
            e_pmRA = str(tyc2_sup2.e_pmRA[i])
            e_pmDE = str(tyc2_sup2.e_pmDE[i])
            BTmag = str(tyc2_sup2.BTmag[i])
            e_BTmag = str(tyc2_sup2.e_BTmag[i])
            VTmag = str(tyc2_sup2.VTmag[i])
            e_VTmag = str(tyc2_sup2.e_VTmag[i])
            prox = str(tyc2_sup2.prox[i])
            TYC = str(tyc2_sup2.TYC[i])
            HIP = str(tyc2_sup2.HIP[i])
            CCDM = str(tyc2_sup2.CCDM[i])

            #single insert
            insert_data = "INSERT INTO data.TYC2 (GlonJ2000,GlatJ2000,RAJ2000,DEJ2000,TYC1,TYC2,TYC3,pflag,RAmdeg,DEmdeg,pmRA," \
                          "pmDE,e_RAmdeg,e_DEmdeg,e_pmRA,e_pmDE,BTmag,e_BTmag,VTmag,e_VTmag,prox,TYC,HIP,CCDM)" \
                          " values ('"+GlonJ2000+"','"+GlatJ2000+"','"+RAJ2000+"','"+DEJ2000+"',ltrim(rtrim('"+TYC1+"')),ltrim(rtrim('"+TYC2+"')),ltrim(rtrim('"+TYC3+"')),'"+pflag+"'," \
                                    "'"+RAmdeg+"','"+DEmdeg+"','"+pmRA+"','"+pmDE+"','"+e_RAmdeg+"','"+e_DEmdeg+"','"+e_pmRA+"','"+e_pmDE+"'," \
                                    "'"+BTmag+"','"+e_BTmag+"','"+VTmag+"','"+e_VTmag+"','"+prox+"','"+TYC+"',ltrim(rtrim('"+HIP+"')),'"+CCDM+"')"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in tyc2_sup2_catalog function'
    else:
        cnx.close()


def tyc2_hd_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        tyc2_hd = pandas.read_csv(catalogsPath+'TYC2_HD.csv', header=None, sep=';', low_memory=False)
        tyc2_hdRange = len(tyc2_hd)

        tyc2_hd.columns = ["TYC1","TYC2","TYC3","HD"]
        insert_data = ''
        for counter in range(0,tyc2_hdRange):
            insert_data = ''
            i = counter
            TYC1 = str(tyc2_hd.TYC1[i])
            TYC2 = str(tyc2_hd.TYC2[i])
            TYC3 = str(tyc2_hd.TYC3[i])
            HD = str(tyc2_hd.HD[i])

            #single insert
            insert_data = "INSERT INTO data.tyc2_hd " \
                          " values (ltrim(rtrim('"+TYC1+"')),ltrim(rtrim('"+TYC2+"')),ltrim(rtrim('"+TYC3+"')),ltrim(rtrim('"+HD+"')))"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in tyc2_hd_catalog function'
    else:
        cnx.close()


def hd_name_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        hd_name = pandas.read_csv(catalogsPath+'HD_NAME.csv', header=None, sep=';', low_memory=False)
        hd_nameRange = len(hd_name)
        print hd_nameRange
        hd_name.columns = ["HD","BFD","NAME"]
        insert_data = ''
        for counter in range(0,hd_nameRange):
            insert_data = ''
            i = counter
            HD = str(hd_name.HD[i])
            BFD = str(hd_name.BFD[i])
            NAME = str(hd_name.NAME[i])

            #single insert
            insert_data = "INSERT INTO data.hd_name " \
                          " values (ltrim(rtrim('"+HD+"')),ltrim(rtrim('"+BFD+"')),ltrim(rtrim('"+NAME+"')))"

            print i
            cursor.execute(insert_data)
            cnx.commit()

        cursor.close()

    except:
        print 'errors in hd_name_catalog function'
    else:
        cnx.close()


try:
    #gc_catalog()
    #hd_catalog()
    #hip_catalog()
    #hr_catalog()
    #sao_catalog()
    #tyc2_catalog()
    #tyc2_sup1_catalog()
    tyc2_sup2_catalog()
    #tyc2_hd_catalog()
    #hd_name_catalog()
except:
    print 'errors'
