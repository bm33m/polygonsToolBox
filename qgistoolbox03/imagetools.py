"""
imagetools.py
Tools for images.
Using Open CV and Numpy.
"""

import sys
import datetime
import time
import math
from math import sqrt
import pprint
#import asyncio
import logging
logfile = 'qtoolapp.log'
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filename=logfile,
    level=logging.DEBUG)

def mytime2b():
    now = datetime.datetime.now()
    return now

try:
    import cv2 as cv
    import numpy as np
    #import pandas as pd
    #from matplotlib import pyplot as plt
    #import networkx as nx
    #from scipy import linalg
except Exception as e:
    logging.critical('%s qgistoolpp models: %s'%(mytime2b(), e))

def imageInfo(link):
    """
    Read image data.
    """
    image = {}
    try:
        image1 = cv.imread(link)
        image['data'] = image1
        image['shape'] = image1.shape
        image['size'] = image1.size
        image['dtype'] = image1.dtype
    except Exception as e:
        logging.error('qgistoolapp imageInfo: %s'%(e))
    return image

def imageTool2(data, color=(255,255,255), display=False):
    try:
        # Loads an image
        #image = cv.imread(data, cv.IMREAD_GRAYSCALE)
        #image = cv.cvtColor(data, cv.COLOR_BGR2GRAY)
        image = np.copy(data)
        # Check if image is loaded fine
        if image is None:
            print ('Error opening image!')
            print ('Usage: spikestool.py [-- input ' + 'image.png' + '] \n')
            return -1
        else:
            size = 0
            try:
                size = data.size
                y, x, c = data.shape
                print('''Image procesing...
                Height => rows(y): %s,
                Width => columns(x): %s,
                Channels => c: %s
                Size: %s,
                '''%(y, x, c, size))
            except Exception as e:
                logging.error('imageTool2: size: %s, %s'%(size, e))
        # Spikes detection
        spikes = cv.Canny(image, 50, 200, None, 3)
        # Copy spikes to the images that will display the results in BGR
        cdst = cv.cvtColor(spikes, cv.COLOR_GRAY2BGR)
        cdstRed = np.copy(cdst)
        cdstBlack = np.copy(cdst)
        imageWhite = np.copy(image)
        imageGray = np.copy(image)
        imageSpikes = np.copy(image)
        cdstPspikes = np.copy(image)
        cdstPblack = np.copy(cdst)
        cdstPred = np.copy(cdst)
        cdstPwhite = np.copy(cdst)
        template = np.zeros(image.shape, image.dtype)
        #  Standard Hough Line Transform
        lines = cv.HoughLines(spikes, 1, np.pi / 180, 150, None, 0, 0)
        thicknessX = [1,2,3,4,5,6,7,8,9,10]
        thickness = thicknessX[0]
        # Draw the lines
        print('color: ', color)
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv.line(cdstRed, pt1, pt2, (0,0,255), thickness, cv.LINE_AA)
                cv.line(cdstBlack, pt1, pt2, (0,0,0), thickness, cv.LINE_AA)
                cv.line(imageWhite, pt1, pt2, (255,255,255), thickness,
                    cv.LINE_AA)
                cv.line(imageGray, pt1, pt2, (222, 234, 236), thickness,
                    cv.LINE_AA)
                cv.line(imageSpikes, pt1, pt2,
                    tointp((color[0], color[1], color[2])), thickness,
                    cv.LINE_AA)
        # Probabilistic Line Transform
        linesP = cv.HoughLinesP(spikes, 1, np.pi / 180, 50, None, 50, 10)
        # Draw the lines
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                cv.line(cdstPblack, (l[0], l[1]), (l[2], l[3]), (0, 0, 0),
                    thickness, cv.LINE_AA)
                cv.line(cdstPred, (l[0], l[1]), (l[2], l[3]), (0, 0, 255),
                    thickness, cv.LINE_AA)
                cv.line(cdstPwhite, (l[0], l[1]), (l[2], l[3]),
                    (255, 255, 255), thickness, cv.LINE_AA)
                cv.line(cdstPspikes, (l[0], l[1]), (l[2], l[3]),
                    tointp((color[0], color[1], color[2])),
                    thickness, cv.LINE_AA)
                cv.line(template, (l[0], l[1]), (l[2], l[3]),
                    (255, 25, 25), thickness, cv.LINE_AA)
        # Show results
        if(display):
            print(f'{mytime2b()} \nPress [esc] to quit..... ')
            imageShow("1. Source: 1", image)
            imageShow("2. imageSpikes", imageSpikes)
            imageShow("3. Detected spikes [in red] -\
                Standard Hough Line Transform", cdstRed)
            imageShow("4. Remove spikes -\
                Standard Hough Line Transform", cdstBlack)
            imageShow("5. Detected spikes [in red] -\
                Probabilistic Line Transform", cdstPred)
            imageShow("6. Image: white", imageWhite)
            imageShow("7. Image: gray", imageGray)
            imageShow("8. Spikes", cdstPspikes)
            imageShow("9. Template1 black - Probabilistic Line Transform",
                cdstPblack)
            imageShow("10. Template2 white - Probabilistic Line Transform",
                cdstPwhite)
            imageShow("11. Template", template)
            ch2 = cv.waitKey(0)
            print('ch2: ', ch2)
        return [image, imageSpikes, cdstPspikes, cdstPblack, cdstPwhite,
            imageWhite, imageGray, template]
    except Exception as e:
        logging.error('imageTool2: %s'%( e))
    print('Done.')
    return [data]

def imageShow(link, image):
    """Show the image."""
    try:
        cv.imshow(link, image)
        #cv.waitKey()
    except Exception as e:
        logging.error('imageShow: %s'%(e))

def imageSave(filename, image):
    """Save the image."""
    try:
        cv.imwrite(filename, image)
        print("Image saved: %s"%(filename))
    except Exception as e:
        logging.error('imageSave: %s'%(e))

def tointp(p):
    try:
        return tuple(map(int, p))
    except Exception as e:
        logging.error('tointp: %s'%(e))
    return tuple(map(int, p))

def getColor(image):
    y, x, c = image.shape
    print('y: %s, x: %s, c: %s'%(y,x,c))
    b, g, r = image[y//2, x//2]
    return (b, g, r)


ref01 = [0, 0, 0]
def account_02(pref):
    """
    Returns serial number.
    """
    pref[0] += 1
    d2 = mytime_02b()
    d3 = d2.microsecond
    accn = "%d%d%d%d%d%d%d"%(d2.year, d2.month, d2.day,
        d2.hour, d2.minute, d2.second, d3%1000)
    sern = int(accn) + pref[0]
    return sern

def mytime_02b():
    """
    Check the time now.
    """
    now = datetime.datetime.now()
    return now
