#!/usr/bin/env python

import numpy as np
import pyfits
import numpy
import astropy
import ConfigParser
import math
from photutils import CircularAperture
from photutils import aperture_photometry
from photutils import CircularAnnulus


env = ConfigParser.RawConfigParser()
env.read('../resources/env.properties')
backendInputFits = env.get('FilesCatalogs', 'catalog.backendInputFits');
backendOutputFits = env.get('FilesCatalogs', 'catalog.backendOutputFits');
frontendInputFits = env.get('FilesCatalogs', 'catalog.frontendInputFits');


def photometry(positionX, positionY, radius, radiusInner, radiusOuter, imageForPhotometry, sessionId):
    try:

       positionX = int(positionX)
       positionY = int(positionY)
       radius = int(radius)
       radiusInner = int(radiusInner)
       radiusOuter = int(radiusOuter)
       positions = [(positionX, positionY)]
       apertures = CircularAperture(positions, r=radius)
       annulus_apertures = CircularAnnulus(positions, r_in=radiusInner, r_out=radiusOuter)

       #Open data
       dataList = []
       dataList = openFile(backendInputFits+sessionId+"_Processed_"+imageForPhotometry)

       #object aperture
       try:
          rawflux_table = aperture_photometry(dataList, apertures)
       except(RuntimeError, TypeError, NameError):
          print 'I cannot'

       #backround apertures
       bkgflux_table = aperture_photometry(dataList, annulus_apertures)
       try:
          phot_table = astropy.table.hstack([rawflux_table, bkgflux_table], table_names=['raw', 'bkg'])
       except(RuntimeError, TypeError, NameError):
          print 'error'

       bkg_mean = phot_table['aperture_sum_bkg'] / annulus_apertures.area()
       bkg_sum = bkg_mean * apertures.area()
       final_sum = phot_table['aperture_sum_raw'] - bkg_sum
       phot_table['residual_aperture_sum'] = final_sum

       #instrumental magnitude
       instrumentalMag = -2.5*math.log10((rawflux_table[0][3]-phot_table['residual_aperture_sum'][0]))
       return instrumentalMag
    except(RuntimeError, TypeError, NameError):
       print 'error in photometry function'


def openFile(fileName):
    hdulist = pyfits.open(fileName)
    img_data_raw = hdulist[0].data
    hdulist.close()
    img_data_raw = numpy.array(img_data_raw, dtype=float)
    return img_data_raw
