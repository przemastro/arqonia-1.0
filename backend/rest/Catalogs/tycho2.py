import sys
import pyodbc
import os
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('C:/Users/Przemek/Desktop/astroApp/backend/resources/env.properties')
dbAddress = config.get('DatabaseConnection', 'database.address');
queries = ConfigParser.RawConfigParser()
queries.read('C:/Users/Przemek/Desktop/astroApp/backend/resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()


try:

    cnx = pyodbc.connect(dbAddress)
    cursor = cnx.cursor()
    fn = open('C:/Users/Przemek/Downloads/tyc2/tyc2-00.dat', 'r')
    position = 0
    for counter in range(1,127001):
       fn.seek(position);
       TYC1 = fn.read(4);

       fn.seek(position+5);
       TYC2 = fn.read(5);

       fn.seek(position+11);
       TYC3 = fn.read(1);

       fn.seek(position+13);
       pflag = fn.read(1);

       fn.seek(position+15);
       RAmdeg = fn.read(12);

       fn.seek(position+28);
       DEmdeg = fn.read(12);

       fn.seek(position+41);
       pmRA = fn.read(7);

       fn.seek(position+49);
       pmDE = fn.read(7);

       fn.seek(position+57);
       e_RAmdeg = fn.read(3);

       fn.seek(position+61);
       e_DEmdeg = fn.read(3);

       fn.seek(position+65);
       e_pmRA = fn.read(4);

       fn.seek(position+70);
       e_pmDE = fn.read(4);

       fn.seek(position+75);
       EpRAm = fn.read(7);

       fn.seek(position+83);
       EpDEm = fn.read(7);

       fn.seek(position+91);
       Num = fn.read(2);

       fn.seek(position+94);
       q_RAmdeg = fn.read(3);

       fn.seek(position+98);
       q_DEmdeg = fn.read(3);

       fn.seek(position+102);
       q_pmRA = fn.read(3);

       fn.seek(position+106);
       q_pmDE = fn.read(3);

       fn.seek(position+110);
       BTmag = fn.read(6);

       fn.seek(position+117);
       e_BTmag = fn.read(5);

       fn.seek(position+123);
       VTmag = fn.read(6);

       fn.seek(position+130);
       e_VTmag = fn.read(5);

       fn.seek(position+136);
       prox = fn.read(3);

       fn.seek(position+140);
       TYC = fn.read(1);

       fn.seek(position+142);
       HIP = fn.read(5);

       fn.seek(position+148);
       CCDM = fn.read(3);

       fn.seek(position+152);
       RAdeg = fn.read(12);

       fn.seek(position+165);
       DEdeg = fn.read(12);

       fn.seek(position+178);
       EpRA = fn.read(4);

       fn.seek(position+183);
       EpDE = fn.read(4);

       fn.seek(position+188);
       e_RAdeg = fn.read(5);

       fn.seek(position+194);
       e_DEdeg = fn.read(5);

       fn.seek(position+200);
       posflg = fn.read(1);

       fn.seek(position+202);
       corr = fn.read(4);



       position = position + 207
       print TYC1, TYC2, TYC3, pflag
       insert_tycho2 = "insert into data.Tycho2 values('"+TYC1+"','"+TYC2+"','"+TYC3+"','"+pflag+"','"+RAmdeg+"','"+DEmdeg+"','"+pmRA+"','"+pmDE+"'," \
                                                           "'"+e_RAmdeg+"','"+e_DEmdeg+"','"+e_pmRA+"','"+e_pmDE+"','"+EpRAm+"','"+EpDEm+"','"+Num+"','"+q_RAmdeg+"'," \
                                                           "'"+q_DEmdeg+"','"+q_pmRA+"','"+q_pmDE+"','"+BTmag+"','"+e_BTmag+"','"+VTmag+"','"+e_VTmag+"','"+prox+"'," \
                                                           "'"+TYC+"','"+HIP+"','"+CCDM+"','"+RAdeg+"','"+DEdeg+"','"+EpRA+"','"+EpDE+"','"+e_RAdeg+"'," \
                                                           "'"+e_DEdeg+"','"+posflg+"','"+corr+"')"
       print insert_tycho2

       cursor.execute(insert_tycho2)
       cnx.commit()


    fn.close()
    cursor.close()
except:
    print 'errors in loadTycho2 function'
else:
    cnx.close()


