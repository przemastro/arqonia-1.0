#!/usr/bin/env python

import numpy as np
import pyfits
from scipy import ndimage
import pylab
import numpy
import math
import os
import time
import ConfigParser
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


env = ConfigParser.RawConfigParser()
env.read('../resources/env.properties')
backendInputFits = env.get('FilesCatalogs', 'catalog.backendInputFits');
backendOutputFits = env.get('FilesCatalogs', 'catalog.backendOutputFits');
frontendInputFits = env.get('FilesCatalogs', 'catalog.frontendInputFits');




def reduce(getDarkFrames, getBiasFrames, getFlatFields, getRawFrames, sessionId):
    try:
        sig_fract = 5.0
        percent_fract = 0.01
        min_val = 0.0

        #Open Dark Frames data
        List = getDarkFrames
        reference_dark_image = 'None'
        dataList = []
        if List != []:
           for file in List:
               dataList.append(openFile(backendInputFits+sessionId+"_Dark_"+file))
           reference_dark_image = medianImage(dataList)

        #Open Bias Frames data
        List = getBiasFrames
        reference_bias_image = 'None'
        if List != []:
           dataList = []
           for file in List:
               dataList.append(openFile(backendInputFits+sessionId+"_Bias_"+file))
           reference_bias_image = medianImage(dataList)

        #Open Flat Fields data
        List = getFlatFields
        reference_flat_image = 'None'
        if List != []:
           dataList = []
           for file in List:
               dataList.append(openFileAndNormalize(backendInputFits+sessionId+"_Flat_"+file))
           reference_flat_image = medianImage(dataList)


        #Open Raw Images Data and Reduce
        List = getRawFrames
        if List != []:
           for file in List:
              dataImage = openFile(backendInputFits+sessionId+"_Raw_"+file)
              #reference dark frame exists
              dark_corrected_image = 'None'
              if reference_dark_image != 'None':
                 print 'Dark Frame Correction'
                 dark_corrected_image = dataImage - reference_dark_image
                 print dark_corrected_image
              #reference dark frame does not exist but reference bias frame exists
              bias_corrected_image = 'None'
              if reference_dark_image == 'None' and reference_bias_image != 'None':
                 bias_corrected_image = dataImage - reference_bias_image
                 print bias_corrected_image
              #reference dark frame exists and reference bias frame exists
              if reference_dark_image != 'None' and reference_bias_image != 'None':
                 bias_corrected_image = dark_corrected_image - reference_bias_image
                 print bias_corrected_image

              #dark corrected image exists and flat exists
              if dark_corrected_image != 'None' and reference_flat_image != 'None' and bias_corrected_image == 'None':
                 print 'dark corrected with flat'
                 final_image = dark_corrected_image / reference_flat_image
              #bias corrected image exists and flat exists
              if bias_corrected_image != 'None' and reference_flat_image != 'None':
                 print 'bias corrected with flat'
                 final_image = bias_corrected_image / reference_flat_image
              #reference flat field does not exist but bias corrected image exists
              if bias_corrected_image != 'None' and reference_flat_image == 'None':
                  print 'bias corrected without flat'
                  final_image = bias_corrected_image
              #reference flat field does not exist and only dark corrected image exists
              if dark_corrected_image != 'None' and reference_flat_image == 'None' and bias_corrected_image == 'None':
                  print 'dark corrected without flat'
                  final_image = dark_corrected_image
              #reference flat field exists and raw image exists
              if bias_corrected_image == 'None' and reference_flat_image != 'None' and dark_corrected_image == 'None':
                  print 'only flat'
                  final_image = dataImage / reference_flat_image
              #reference flat field does not exist and only raw image exists
              if bias_corrected_image == 'None' and reference_flat_image == 'None' and dark_corrected_image == 'None':
                  print 'only raw'
                  final_image = dataImage

              width = float(final_image.shape[1])/100
              height = float(final_image.shape[0])/100
              try:
                 os.remove(backendOutputFits+"Processed_"+file)
                 pyfits.append(backendOutputFits+"Processed_"+file, final_image)
              except(RuntimeError, TypeError, NameError):
                 print 'error appending or removing'
              sky, num_iter = sky_mean_sig_clip(final_image, sig_fract, percent_fract, max_iter=1)
              img_data = final_image - sky
              new_img = linear(img_data, scale_min = min_val)
              Rotated_Plot = ndimage.rotate(new_img, 180)
              Flipped_Plot = np.fliplr(Rotated_Plot)
              fig = Figure(figsize=(width, height))
              fig.figimage(Flipped_Plot, cmap='gray')
              canvas = FigureCanvas(fig)
              specialCharacterPosition = file.index('.')
              fileWithoutExtension = str(file[:specialCharacterPosition])
              canvas.print_figure(frontendInputFits+"Linear_"+sessionId+"_Processed_"+fileWithoutExtension+".png")

    except:
        print 'error in reduce function'

def medianImage(images):
    stack = numpy.array(images)
    median = numpy.median(stack, axis=0)
    return median

def openFile(fileName):
    hdulist = pyfits.open(fileName)
    img_data_raw = hdulist[0].data
    hdulist.close()
    img_data_raw = numpy.array(img_data_raw, dtype=float)
    return img_data_raw

def openFileAndNormalize(fileName):
    hdulist = pyfits.open(fileName)
    img_data_raw = hdulist[0].data
    hdulist.close()
    img_data_raw = numpy.array(img_data_raw, dtype=float)
    image_mean = numpy.mean(img_data_raw)
    normalized = img_data_raw / image_mean
    return normalized

def sky_mean_sig_clip(input_arr, sig_fract, percent_fract, max_iter=100, low_cut=True, high_cut=True):
    work_arr = numpy.ravel(input_arr)
    old_sky = numpy.mean(work_arr)
    sig = work_arr.std()
    upper_limit = old_sky + sig_fract * sig
    lower_limit = old_sky - sig_fract * sig
    if low_cut and high_cut:
        indices = numpy.where((work_arr < upper_limit) & (work_arr > lower_limit))
    else:
        if low_cut:
            indices = numpy.where((work_arr > lower_limit))
        else:
            indices = numpy.where((work_arr < upper_limit))
    work_arr = work_arr[indices]
    new_sky = numpy.mean(work_arr)
    iteration = 0
    while ((math.fabs(old_sky - new_sky)/new_sky) > percent_fract) and (iteration < max_iter) :
        iteration += 1
        old_sky = new_sky
        sig = work_arr.std()
        upper_limit = old_sky + sig_fract * sig
        lower_limit = old_sky - sig_fract * sig
        if low_cut and high_cut:
            indices = numpy.where((work_arr < upper_limit) & (work_arr > lower_limit))
        else:
            if low_cut:
                indices = numpy.where((work_arr > lower_limit))
            else:
                indices = numpy.where((work_arr < upper_limit))
        work_arr = work_arr[indices]
        new_sky = numpy.mean(work_arr)
    return (new_sky, iteration)


def linear(inputArray, scale_min=None, scale_max=None):
    #print "img_scale : linear"
    imageData=numpy.array(inputArray, copy=True)

    if scale_min == None:
        scale_min = imageData.min()
    if scale_max == None:
        scale_max = imageData.max()

    imageData.clip(min=scale_min, max=scale_max)
    imageData = (imageData -scale_min) / (scale_max - scale_min)
    indices = numpy.where(imageData < 0)
    imageData[indices] = 0.0

    return imageData


def power(inputArray, power_index=3.0, scale_min=None, scale_max=None):
    #print "img_scale : power"
    imageData=numpy.array(inputArray, copy=True)

    if scale_min == None:
        scale_min = imageData.min()
    if scale_max == None:
        scale_max = imageData.max()
    factor = 1.0 / math.pow((scale_max - scale_min), power_index)
    indices0 = numpy.where(imageData < scale_min)
    indices1 = numpy.where((imageData >= scale_min) & (imageData <= scale_max))
    indices2 = numpy.where(imageData > scale_max)
    imageData[indices0] = 0.0
    imageData[indices2] = 1.0
    imageData[indices1] = numpy.power((imageData[indices1] - scale_min), power_index)*factor

    return imageData

def sky_mean_sig_clip(input_arr, sig_fract, percent_fract, max_iter=100, low_cut=True, high_cut=True):
    work_arr = numpy.ravel(input_arr)
    old_sky = numpy.mean(work_arr)
    sig = work_arr.std()
    upper_limit = old_sky + sig_fract * sig
    lower_limit = old_sky - sig_fract * sig
    if low_cut and high_cut:
        indices = numpy.where((work_arr < upper_limit) & (work_arr > lower_limit))
    else:
        if low_cut:
            indices = numpy.where((work_arr > lower_limit))
        else:
            indices = numpy.where((work_arr < upper_limit))
    work_arr = work_arr[indices]
    new_sky = numpy.mean(work_arr)
    iteration = 0
    while ((math.fabs(old_sky - new_sky)/new_sky) > percent_fract) and (iteration < max_iter) :
        iteration += 1
        old_sky = new_sky
        sig = work_arr.std()
        upper_limit = old_sky + sig_fract * sig
        lower_limit = old_sky - sig_fract * sig
        if low_cut and high_cut:
            indices = numpy.where((work_arr < upper_limit) & (work_arr > lower_limit))
        else:
            if low_cut:
                indices = numpy.where((work_arr > lower_limit))
            else:
                indices = numpy.where((work_arr < upper_limit))
        work_arr = work_arr[indices]
        new_sky = numpy.mean(work_arr)
    return (new_sky, iteration)


def linear(inputArray, scale_min=None, scale_max=None):
    #print "img_scale : linear"
    imageData=numpy.array(inputArray, copy=True)

    if scale_min == None:
        scale_min = imageData.min()
    if scale_max == None:
        scale_max = imageData.max()

    imageData.clip(min=scale_min, max=scale_max)
    imageData = (imageData -scale_min) / (scale_max - scale_min)
    indices = numpy.where(imageData < 0)
    imageData[indices] = 0.0

    return imageData


def histeq(inputArray, num_bins=1024):

    imageData=numpy.array(inputArray, copy=True)

    # histogram equalisation: we want an equal number of pixels in each intensity range
    sortedDataIntensities=numpy.sort(numpy.ravel(imageData))
    median=numpy.median(sortedDataIntensities)

    # Make cumulative histogram of data values, simple min-max used to set bin sizes and range
    dataCumHist=numpy.zeros(num_bins)
    minIntensity=sortedDataIntensities.min()
    maxIntensity=sortedDataIntensities.max()
    histRange=maxIntensity-minIntensity
    binWidth=histRange/float(num_bins-1)
    for i in range(len(sortedDataIntensities)):
        binNumber=int(math.ceil((sortedDataIntensities[i]-minIntensity)/binWidth))
        addArray=numpy.zeros(num_bins)
        onesArray=numpy.ones(num_bins-binNumber)
        onesRange=range(binNumber, num_bins)
        numpy.put(addArray, onesRange, onesArray)
        dataCumHist=dataCumHist+addArray

    # Make ideal cumulative histogram
    idealValue=dataCumHist.max()/float(num_bins)
    idealCumHist=numpy.arange(idealValue, dataCumHist.max()+idealValue, idealValue)

    # Map the data to the ideal
    for y in range(imageData.shape[0]):
        for x in range(imageData.shape[1]):
            # Get index corresponding to dataIntensity
            intensityBin=int(math.ceil((imageData[y][x]-minIntensity)/binWidth))

    # Guard against rounding errors (happens rarely I think)
    if intensityBin<0:
        intensityBin=0
    if intensityBin>len(dataCumHist)-1:
        intensityBin=len(dataCumHist)-1

    # Get the cumulative frequency corresponding intensity level in the data
    dataCumFreq=dataCumHist[intensityBin]

    # Get the index of the corresponding ideal cumulative frequency
    idealBin=numpy.searchsorted(idealCumHist, dataCumFreq)
    idealIntensity=(idealBin*binWidth)+minIntensity
    imageData[y][x]=idealIntensity

    scale_min = imageData.min()
    scale_max = imageData.max()
    imageData.clip(min=scale_min, max=scale_max)
    imageData = (imageData -scale_min) / (scale_max - scale_min)
    indices = numpy.where(imageData < 0)
    imageData[indices] = 0.0

    return imageData
