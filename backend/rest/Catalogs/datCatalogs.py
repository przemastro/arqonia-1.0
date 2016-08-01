import sys
import pyodbc
import os
import ConfigParser

globalPath = 'C:/Users/Przemek/Desktop/arqonia/backend'
catalogsPath = 'C:/Users/Przemek/Downloads/catalogs/'

config = ConfigParser.RawConfigParser()
config.read(globalPath+'/resources/env.properties')
dbAddress = config.get('DatabaseConnection', 'database.address');
queries = ConfigParser.RawConfigParser()
queries.read(globalPath+'/resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()

def mpc_catalog():
   try:
       cnx = pyodbc.connect(dbAddress)
       cursor = cnx.cursor()
       fn = open(catalogsPath+'MPC.dat', 'r')
       position = 0
       for counter in range(1,716616):
           fn.seek(position);
           Number = fn.read(8);

           fn.seek(position+8);
           H = fn.read(5);

           fn.seek(position+14);
           G = fn.read(5);

           fn.seek(position+20);
           Epoch = fn.read(5);

           fn.seek(position+26);
           M = fn.read(9);

           fn.seek(position+37);
           Perihelion = fn.read(9);

           fn.seek(position+48);
           Node = fn.read(9);

           fn.seek(position+59);
           Inclination = fn.read(9);

           fn.seek(position+70);
           e = fn.read(9);

           fn.seek(position+80);
           n = fn.read(11);

           fn.seek(position+92);
           a = fn.read(11);

           fn.seek(position+105);
           U = fn.read(1);

           fn.seek(position+107);
           Reference = fn.read(9);

           fn.seek(position+117);
           Obs = fn.read(5);

           fn.seek(position+123);
           Opp = fn.read(3);

           fn.seek(position+127);
           Arc = fn.read(4);

           fn.seek(position+137);
           rms = fn.read(4);

           fn.seek(position+142);
           Perts = fn.read(3);

           fn.seek(position+166);
           Name = fn.read(25);


           position = position + 203
           insert_mpc = "insert into data.MPC values('"+Number+"','"+H+"','"+G+"','"+Epoch+"','"+M+"','"+Perihelion+"'," \
                                                          "'"+Node+"','"+Inclination+"','"+e+"','"+n+"','"+a+"','"+U+"'," \
                                                          "'"+Reference+"','"+Obs+"','"+Opp+"','"+Arc+"','"+rms+"','"+Perts+"','"+Name+"')"
           print counter

           cursor.execute(insert_mpc)
           cnx.commit()


       fn.close()
       cursor.close()
   except:
       print 'errors in mpc_catalog function'
   else:
       cnx.close()


def comets_catalog():
    try:
        cnx = pyodbc.connect(dbAddress)
        cursor = cnx.cursor()
        fn = open(catalogsPath+'comets.dat', 'r')
        position = 0

        #874
        for counter in range(0,874):
            fn.seek(position);
            Number = fn.read(4);

            fn.seek(position+4);
            OrbitType = fn.read(1);

            fn.seek(position+5);
            Designation = fn.read(7);

            fn.seek(position+14);
            P_Year = fn.read(4);

            fn.seek(position+19);
            P_Month = fn.read(2);

            fn.seek(position+22);
            P_Day = fn.read(7);

            fn.seek(position+30);
            P_Distance = fn.read(9);

            fn.seek(position+41);
            e = fn.read(8);

            fn.seek(position+51);
            Perihelion = fn.read(8);

            fn.seek(position+61);
            Longitude = fn.read(8);

            fn.seek(position+71);
            Inclination = fn.read(8);

            fn.seek(position+81);
            E_Year = fn.read(4);

            fn.seek(position+85);
            E_Month = fn.read(2);

            fn.seek(position+87);
            E_Day = fn.read(2);

            fn.seek(position+91);
            Abs_Mag = fn.read(4);

            fn.seek(position+102);
            Name = fn.read(50);


            position = position + 161
            insert_comets = "insert into data.comets values('"+Number+"','"+OrbitType+"','"+Designation+"','"+P_Year+"','"+P_Month+"','"+P_Day+"'," \
                                                        "'"+P_Distance+"','"+e+"','"+Perihelion+"','"+Longitude+"','"+Inclination+"'," \
                                                        "'"+E_Year+"','"+E_Month+"','"+E_Day+"', '"+Abs_Mag+"', '"+Name+"')"
            print counter

            cursor.execute(insert_comets)
            cnx.commit()


        fn.close()
        cursor.close()
    except:
        print 'errors in comets_catalog function'
    else:
        cnx.close()


try:
    mpc_catalog()
    #comets_catalog()
except:
    print 'errors'