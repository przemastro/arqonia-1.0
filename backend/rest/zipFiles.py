
import sys
import pyodbc
import ConfigParser
import ast
import simplejson as json
from sjcl import SJCL
import os
import zipfile
from os.path import basename


env = ConfigParser.RawConfigParser()
env.read('../resources/env.properties')
dbAddress = env.get('DatabaseConnection', 'database.address');
backendInputFits = env.get('FilesCatalogs', 'catalog.backendInputFits');
backendOutputFits = env.get('FilesCatalogs', 'catalog.backendOutputFits');
frontendInputFits = env.get('FilesCatalogs', 'catalog.frontendInputFits');
frontendOutputFits = env.get('FilesCatalogs', 'catalog.frontendOutputFits');
key = env.get('SecurityKey', 'public.key');
queries = ConfigParser.RawConfigParser()
queries.read('../resources/queries.properties')
cnx = pyodbc.connect(dbAddress)
cursor = cnx.cursor()

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

modes = { zipfile.ZIP_DEFLATED: 'deflated',
          zipfile.ZIP_STORED:   'stored',
          }

def zipAll(getImages, sessionId):
   try:
      zf = zipfile.ZipFile(frontendOutputFits+sessionId+"_ProcessedImages.zip", mode='w')
      List = getImages
      for file in List:
         zf.write(backendOutputFits+"Processed_"+file, basename(backendOutputFits+"Processed_"+file), compress_type=compression)
      zf.close()
   except:
      print 'errors in zipAll function'

