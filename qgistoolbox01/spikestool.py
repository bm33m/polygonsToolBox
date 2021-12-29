#!/usr/bin/env python
"""
Spikes remover tool.
Version 01.
"""
#from django.db import models
#from django.utils.timezone import make_aware
import datetime
import time
import sys
import argparse
import itertools as it
import math
from math import sqrt
import pprint
import asyncio
import logging
logfile = 'qtoolapp.log'
logging.basicConfig(format='%(asctime)s %(message)s', filename=logfile,\
    level=logging.DEBUG)

def mytime2b():
    now = datetime.datetime.now()
    return now
try:
    import cv2 as cv
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    import networkx as nx
    from scipy import linalg
except Exception as e:
    logging.critical('%s qgistoolpp models: %s'%(mytime2b(), e))
regions0X = 'region11 %s region23 %s region35 %s region47 %s'%(
    'north12', 'east24', 'south36', 'west48')
regionNames = it.cycle(regions0X.split())
#regionName = next(regionNames)

class QgistoolApp(object):
    """
    Tool to remove spikes on the polygons.
    Version 001: Uses open CV, numpy,
    pandas matplotlib, networkx, scipy.
    Read common GIS Raster and DEM files
    to display and manipulate geographic data.
    Uses Image Input and Output (imgcodecs module)
    Version 002: Uses Qgis.
    """
    image = []

    def __init__(self, arg):
        super().__init__()
        self.links = arg
        self.image = self.imageData(arg)
        self.windowname = arg
        self.ref = self.image['data']
        self.tasks = []
        self.xcolor = (0, 0, 0)
        self.points = np.copy(self.image['data'])
        logging.info('QgistoolApp init: %s'%(arg))

    def imageData(self, link):
        logging.info('imageData: %s'%(link))
        return imageInfo(link)

    def lineStrings(self):
        return self.points

    def imageGraph(self):
        try:
            xy = 0
            xyz = 0
            hstack = np.hstack(self.image['data'])
            print('hstack: %s\n'%(self.links), hstack)
            G = nx.Graph()
            time = {}
            for i in hstack:
                for x in i:
                    G.add_node(x)
                    xy += 1
                xyz += 1
            print('xy: %s, '%(xy), xyz)
            nx.draw(G)
            plt.show()
        except Exception as e:
            logging.error('imageGraph: %s'%(e))

    def hstackDataframe(self):
        try:
            hstack = np.hstack(self.image['data'])
            des = pd.DataFrame(hstack[0:])
            print('hstackDataFrame: %s\n'%(self.links), des)
            plt.title('hstack: %s'%(self.links))
            plt.plot(des)
            plt.show()
        except Exception as e:
            logging.error('hstackDataframe: %s'%(e))

    def vstackDataframe(self):
        try:
            hstack = np.vstack(self.image['data'])
            des = pd.DataFrame(hstack[0:])
            print('vstackDataFrame: %s\n'%(self.links), des)
            plt.title('vstack: %s'%(self.links))
            plt.plot(des)
            plt.show()
        except Exception as e:
            logging.error('vstackDataframe: %s'%(e))

    def imageHistogram(self):
        """Create color histogram."""
        try:
            image = np.copy(self.image['data'])
            colors = ('Blue', 'Green', 'Red')
            channels = (0, 1, 2)
            plt.xlim([0, 256])
            for channel, c in zip(channels, colors):
                histogram, edges = np.histogram(
                    image[:,:,channel], bins=256, range=(0,256)
                )
                plt.plot(edges[0:-1], histogram, color=c)
            name = self.links.split('/')
            plt.title('histogram: %s'%(name[len(name)-1]))
            plt.xlabel('Color')
            plt.ylabel('Pixels')
            plt.show()
        except Exception as e:
            logging.error('imageHistogram: %s'%(e))

    def toint(self, p):
        try:
            points  = tuple(map(int, p))
            #print('points: ', points)
            return points
        except Exception as e:
            print('toint: %s'%(e))
        return p

    def checkLine(self, p1, p2, n, noise=0.0):
        p1 = np.float32(p1)
        t = np.random.rand(n, 1)
        line = p1 + (p2 - p1)*t + np.random.normal(size=(n, 2))*noise
        return line

    def imageErosion(self, p1=3, p2=3, display=False):
        try:
            iteration = 2 #1
            #p1 = 10 #25 #5
            #p2 = 10 #25 #5
            noise = 0.5 #0.0
            kernel = np.ones((p1,p2), np.uint8)
            #kernel = self.checkLine(p1, p2, iteration, noise)
            erosion = cv.erode(self.image['data'],kernel,iteration)
            if display:
                imageShow('Erosion', erosion)
                cv.waitKey()
            return erosion
        except Exception as e:
            logging.error("imageErosion: %s"%(e))

    def imageDilation(self, p1=3, p2=3, display=False):
        try:
            iteration = 2 #1
            #p1 = 10 #50 #5
            #p2 = 10 #50 #5
            noise = 0.5 #0.0
            kernel = np.ones((p1,p2), np.uint8)
            #kernel = self.checkLine(p1, p2, iteration, noise)
            dilation = cv.dilate(self.image['data'],kernel,iteration)
            if(display):
                imageShow('Dilation', dilation)
                cv.waitKey()
            return dilation
        except Exception as e:
            logging.error("imageDilation: %s"%(e))

    def imageOpening(self, p1=3, p2=3, display=False):
        """Remove noise from the image."""
        try:
            #iteration = 2 #1
            #p1 = 10 #50 #5
            #p2 = 10 #50 #5
            #noise = 0.5 #0.0
            kernel = np.ones((p1,p2), np.uint8)
            #kernel = self.checkLine(p1, p2, iteration, noise)
            opening = cv.morphologyEx(
                self.image['data'], cv.MORPH_OPEN, kernel)
            if(display):
                imageShow('Opening', opening)
                cv.waitKey()
            else:
                return opening
        except Exception as e:
            logging.error("imageOpening: %s"%(e))

    def imageClosing(self, p1=3, p2=3, display=False):
        """Remove noise from the image."""
        try:
            #iteration = 2 #1
            #p1 = [0, 1, 2, 3, 4, 5, 7, 8, 10, 50]
            #p2 = [0, 1, 2, 3, 4, 5, 7, 8, 10, 50]
            #noise = 0.5 #0.0
            kernel = np.ones((p1, p2), np.uint8)
            #kernel = self.checkLine(p1, p2, iteration, noise)
            closing = cv.morphologyEx(
                self.image['data'], cv.MORPH_CLOSE, kernel)
            if(display):
                imageShow('Closing', closing)
                cv.waitKey()
            return closing
        except Exception as e:
            logging.error("imageClosing: %s"%(e))
        return self.image['data']

    def imageGradient(self, display=False, p1=2, p2=2):
        """Remove noise from the image."""
        try:
            iteration = 2 #1
            #p1 = [2, 8, 3, 4, 7, 10, 50, 5]
            #p2 = [2, 8, 3, 4, 7, 10, 50, 5]
            noise = 0.5 #0.0
            kernel = np.ones((p1, p2), np.uint8)
            #kernel = self.checkLine(p1, p2, iteration, noise)
            gradient = cv.morphologyEx(
                self.image['data'], cv.MORPH_GRADIENT, kernel)
            if (display):
                imageShow('Gradient', gradient)
                cv.waitKey()
            else:
                return gradient
        except Exception as e:
            logging.error("imageGradient: %s"%(e))

    def imageTophat(self, display=False, p1=2, p2=2):
        """Remove noise from the image."""
        try:
            iteration = 2 #1
            #p1 = 2 #8 #3 #4 #7 #10 #50 #5
            #p2 = 2 #8 #3 #4 #7 #10 #50 #5
            noise = 0.5 #0.0
            kernel = np.ones((p1, p2), np.uint8)
            #kernel = self.checkLine(p1, p2, iteration, noise)
            tophat = cv.morphologyEx(
                self.image['data'], cv.MORPH_TOPHAT, kernel)
            if (display):
                imageShow('Tophat', tophat)
                cv.waitKey()
            else:
                return tophat
        except Exception as e:
            logging.error("imageTophat: %s"%(e))

    def imageBlackhat(self, display=False, p1=2, p2=2):
        """Remove noise from the image."""
        try:
            iteration = 2 #1
            #p1 = 2 #8 #3 #4 #7 #10 #50 #5
            #p2 = 2 #8 #3 #4 #7 #10 #50 #5
            noise = 0.5 #0.0
            kernel = np.ones((p1, p2), np.uint8)
            #kernel = self.checkLine(p1, p2, iteration, noise)
            blackhat = cv.morphologyEx(
                self.image['data'], cv.MORPH_BLACKHAT, kernel)
            if (display):
                imageShow('Blackhat', blackhat)
                cv.waitKey()
            else:
                return blackhat
        except Exception as e:
            logging.error("imageBlackhat: %s"%(e))

    async def imageTool(self, display=False):
        tool = []
        try:
            alpha = 1.2 #1.0 #1.2 Simple contrast control
            beta = 23   #0    #23 Simple brightness control
            alpha1 = 1.0
            beta0 = 10
            print('try alpha: 1.2, beta: 34')
            #alpha = float(input('# Enter the alpha value [1.0-3.0]: '))
            #beta = int(input('# Enter the beta value [0-100]: '))
            imageSpikes = np.copy(self.image['data'])
            y0 = imageSpikes.shape[0] #rows
            x1 = imageSpikes.shape[1] #columns
            c2 = imageSpikes.shape[2] #Channels
            print('''Spikes image procesing...
            Height => rows(y): %s,
            Width => columns(x): %s,
            Channels => c: %s,
            (Alpha: %s, Beta: %s)'''%(y0, x1, c2, alpha, beta))
            imagey0x0c0 = self.image['data'][0,0,0]
            imagey0x0 = self.image['data'][0,0]
            imagec0 = self.image['data'][0]
            #color at the center
            colorXY204 = getColor(self.image['data'])
            print("image[0, 0, 0]: %s \nimage[0, 0]: %s\n"%(
                imagey0x0c0, imagey0x0))
            print("image[0]: %s\n"%(imagec0))
            print("image[h/2, w/2]: %s\n"%([colorXY204]))
            print('Image procesing... y: %s, x: %s, c: %s, (%s, %s)'%(
                y0, x1, c2, alpha, beta))
            gradient = self.imageGradient(False)
            #tophat = self.imageTophat(False)
            #blackhat = self.imageBlackhat(False)
            closing = self.imageClosing()
            opening = self.imageOpening()
            #template1 = convertScaleImage(closing, alpha1, beta0, False)
            #template2 = convertScaleImage(opening, alpha, beta, False)
            #tool2 = imageTool2(self.image['data'], colorXY204, False)
            #tool2 = imageTool2(template2, colorXY204, False)
            tool2 = imageTool2(opening, colorXY204, False)
            #tool2 = imageTool2(closing, colorXY204, False)
            self.ref = tool2[7]
            #print('template shape: (%s), dtype %s'%(
            #    template1.shape, template1.dtype))
            #tool = removeSpikes(
            #    gradient, tool2, y0, x1, c2, alpha, beta, False)
            tool = await removeSpikes(
                closing, tool2, y0, x1, c2, alpha, beta, False)
            drawStr(gradient, (0,10), 'gradient')
            regions = np.copy(self.image['data'])
            drawRegions(regions, x1, y0)
            if (display):
                print(f'{mytime2b()} \nPress [esc] to quit..... ')
                imageShow('1a. Image: ', imageSpikes)
                imageShow('1b. Opening: ', opening)
                imageShow('1c. Closing: ', closing)
                imageShow('2. Template: ', tool[0])
                imageShow('3. Gradient: ', gradient)
                imageShow('4. Regions:', regions)
                imageShow('5. Spikes: ', tool[1])
                imageShow('6. Template1a: ', tool2[3])
                imageShow('7. Template1b: ', tool2[4])
                imageShow('8. Template2a:', tool[2])
                imageShow('9. Template2b:', tool[3])
                def onTasks(event='a',x='b',y='c',flags='d',param='e'):
                    self.tasks.append([event, x, y, flags, param])
                cv.setMouseCallback('4. Regions:',  onTasks)
                cv.setMouseCallback('8. Template2a:', onTasks)
                cv.setMouseCallback('9. Template2b:', onTasks)
                while True:
                    ch = cv.waitKey(0)
                    if(ch == 27):
                        print('ch27(esc): %s'%(ch))
                        break
                    if(ch == ord('r')):
                        print('#\n   #   \n#\nch r: %s, tasks: %s'%(
                            ch, len(self.tasks)))
                        for x in self.tasks:
                            await self.onChange(x[0], x[1], x[2], x[3], x[4])
                        print('#\n   #   \n#\nch r: %s, done: %s'%(
                            ch, len(self.tasks)))
                    print('ch: ', ch)
        except Exception as e:
            logging.error('imageTool: %s'%(e))
        print('Done')
        return tool

    async def onChange(
        self, event='a', x='b', y='c', flags='d', param='e'):
        try:
            if((mcount[0] < 25) or (mcount[0] % 350) == 0 ):
                print('#%s onChange...%s, Region(%s, %s)'%(
                    mcount[0], event, x, y))
            if (event == cv.EVENT_LBUTTONDOWN):
                print('#%s onChange...%s, Region(%s, %s)'%(
                    mcount[0], event, x, y))
                print(self.xcolor)
                b, g, r = await nearestNeighborColor(
                    self.image['data'], x, y, self.ref)
                self.xcolor = (b, g, r)
                print('nncolor: (%s,%s,%s)'%(self.xcolor))
                #p = self.toint(nncolor)
                #print('points: (%s,%s,%s)'%(p))
            mcount[0] += 1
        except Exception as e:
            print('onChange: %s'%(e))

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

def imageShow(link, image):
    """
    Show the image.
    """
    try:
        cv.imshow(link, image)
        #cv.waitKey()
    except Exception as e:
        logging.error('imageShow: %s'%(e))

def imageSave(filename, image):
    """
    Save the image.
    """
    try:
        cv.imwrite(filename, image)
        print("Image saved: %s"%(filename))
    except Exception as e:
        logging.error('imageSave: %s'%(e))

def convertScaleImage(image, alpha=1.2, beta=23, display=False):
    image1 = [{}]
    try:
        image1 = cv.convertScaleAbs(image, alpha, beta)
        if (display):
            imageShow('scaleAbs', image1)
            cv.waitKey()
    except Exception as e:
        logging.error('convertScaleImage: %s'%(e))
    return image1

async def removeSpikes(
        temp, tool2, y0, x1, c2=0,
        alpha=1.2, beta=23, display=False):
    try:
        template1 = np.zeros(tool2[0].shape, tool2[0].dtype)
        template2 = np.zeros(tool2[0].shape, tool2[0].dtype)
        spikes = np.zeros(tool2[0].shape, tool2[0].dtype)
        #b, g, r = getColor(temp)
        #spikesList = []
        #spikesyxList = []
        #print('T0all: ', tool2[0][y0//4, x1//4].all())
        #print('T0any: ', tool2[0][y0//4, x1//4].any())
        #print('T0yx: ', tool2[0][y0//4, x1//4])
        #print('ref3: ', tool2[3].shape)
        #print('ref4: ', tool2[4].shape)
        print('tool2list = [image0, imageSpikes1, cdstPspikes2,\
        cdstPblack3, cdstPwhite4, imageWhite5, imageGray6, template7]')
        for y in range(y0):
            for x in range(x1):
                a = tool2[3][y,x]
                b = tool2[4][y,x]
                if ((a[0], a[1], a[2]) != (b[0], b[1], b[2])):
                    #spikes[y,x] = temp[y,x]
                    #spikesList.append(spikes[y,x])
                    #spikesyxList.append([y,x])
                    #template1[y,x] = [255,255,255]
                    #template2[y,x] = [222, 234, 236]
                    #b, g, r = nearestNeighborColor(tool2[0], x, y)
                    #b2, g2, r2 = nearestNeighborColor(temp, x, y)
                    #b2, g2, r2 = temp[y, x]
                    #template1[y,x] = [b, g, r]
                    #template2[y,x] = [b2, g2, r2]
                    template1[y,x] = await nearestNeighborColor(
                        tool2[0], x, y, tool2[7])
                    template2[y,x] = temp[y, x]
                    spikes[y,x] = tool2[0][y,x]
                else:
                    template1[y,x] = tool2[0][y,x]
                    template2[y,x] = tool2[0][y,x]
                #for c in range(c2):
                #    spikes[y,x,c] = np.clip(
                #        alpha*tool2[0][y,x,c] + beta, 0, 255)
        if(display):
            print(f'{mytime2b()} \nPress [esc] to quit..... ')
            imageShow('0. Image: ', tool2[0])
            imageShow('1. Spikes: ', spikes)
            imageShow('2. Temp: ', tool2[2])
            imageShow('3. Temp: ', tool2[3])
            imageShow('4. Temp: ', tool2[4])
            imageShow('5. Temp: ', tool2[7])
            imageShow('6. Template1: ', template1)
            imageShow('7. Template2: ', template2)
            print(f'# Step: [2/2] #### {mytime2b()}   ####\n'
            'Press: ctrl+s to save...........step 2/2 \n'
            'Press: esc to quit. \nEnjoy...\n#')
            while True:
                ch = cv.waitKey(0)
                if(ch == 27):
                    break
                if(ch == 19):
                    png = input('# Enter the filename: ')
                    imageSave('./data/%s0.png'%(png), tool2[0])
                    imageSave('./data/%s1.png'%(png), spikes)
                    imageSave('./data/%s2.png'%(png), tool2[2])
                    imageSave('./data/%s3.png'%(png), tool2[3])
                    imageSave('./data/%s4.png'%(png), tool2[4])
                    imageSave('./data/%s5.png'%(png), template1)
                    imageSave('./data/%s6.png'%(png), template2)
                print('ch: %s'%(ch))
        return [tool2[0], spikes, template1, template2]
    except Exception as e:
        logging.error('removeSpikes: %s'%(e))
    return tool2

def imageTool2(data, color=(255,255,255), display=False):
    """
    Check for spikes...
    """
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
                print('''%s Image procesing...
                Height => rows(y): %s,
                Width => columns(x): %s,
                Channels => c: %s
                Size: %s,
                '''%(mytime2b(), y, x, c, size))
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
        thicknessX = [2,3,4,5,6,7,8,9,10]
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
                cv.line(imageWhite, pt1, pt2, (255,255,255), thickness,\
                    cv.LINE_AA)
                cv.line(imageGray, pt1, pt2, (222, 234, 236), thickness,\
                    cv.LINE_AA)
                cv.line(imageSpikes, pt1, pt2, tointp((color[0], color[1],\
                    color[2])), thickness, cv.LINE_AA)
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
                cv.line(template, (l[0], l[1]), (l[2], l[3]), (255, 25, 25),
                    thickness, cv.LINE_AA)
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
            imageShow("9. Template1 black -\
                Probabilistic Line Transform", cdstPblack)
            imageShow("10. Template2 white -\
                Probabilistic Line Transform", cdstPwhite)
            imageShow("11. Template", template)
            print(f'# step: [1/2] #### {mytime2b()}   ####\n'
            'Press: ctrl+s to save........... step 1/2\n'
            'Press: esc to quit. \nEnjoy...\n#')
            while True:
                ch = cv.waitKey(0)
                if(ch == 27):
                    break
                if(ch == 19):
                    png = input('# Enter the filename: ')
                    imageSave('./data/%slstr0.png'%(png), cdstRed)
                    imageSave('./data/%slstr1.png'%(png), cdstPred)
                print('ch: ', ch)
        return [image, imageSpikes, cdstPspikes, cdstPblack, cdstPwhite,
            imageWhite, imageGray, template]
    except Exception as e:
        logging.error('imageTool2: %s'%( e))
    print('Done.')
    return [data]

spikes = [0,0,0]
def imageTool3(image, display=False):
    global spikes
    try:
        # Loads an image
        #src = cv.imread(image, cv.IMREAD_COLOR)
        # Check if image is loaded fine
        src = np.copy(image)
        if src is None:
            print ('Error opening image!')
            print ('Usage: model.py\
                [image_name -- input ' + 'image filename' + '] \n')
            return -1
        # Convert it to gray
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        # Reduce the noise to avoid false circle detection
        gray = cv.medianBlur(gray, 5)
        rows = gray.shape[0]
        circles = cv.HoughCircles(
            gray, cv.HOUGH_GRADIENT, 1, rows / 8,
            param1=100, param2=30,
            minRadius=1, maxRadius=30)
        #
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(src, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(src, center, radius, (255, 0, 255), 3)
        #
        #Remove Spikes
        b, g, r = getColor(image)
        color = (b,g,r)
        print('color: %s, %s, %s'%(color))
        spikes = imageTool2(src, color, False)
        if (display):
            print(f'{mytime2b()} \nPress [esc] to quit..... ')
            imageShow("Image", image)
            imageShow("Spikes: 1", spikes[0])
            imageShow("Spikes: 2", spikes[1])
            imageShow("Spikes: 3", spikes[2])
            cv.setMouseCallback('Image', onmouse)
            while True:
                ch = cv.waitKey(0)
                if(ch == 27):
                    print('ch27(esc): %s'%(ch))
                    break
                if(ch == ord('r')):
                    print('ch r: %s'%(ch))
                    #spikes = imageTool2(spikes[0], color, True)
        print('done..')
    except Exception as e:
        logging.error("imageTool3 %s"%(e))
    return 0

def drawKeypoints(vis, keypoints, color = (0, 255, 255)):
    for kp in keypoints:
        x, y = kp.pt
        cv.circle(vis, (int(x), int(y)), 2, color)

def drawStr(image, target, s):
    try:
        x, y = target
        lineType = cv.LINE_AA
        thickness = 2
        cv.putText(image, s, (x+1, y+1),
           cv.FONT_HERSHEY_PLAIN, 1.0, (0, 200, 0),
           thickness, lineType)
        cv.putText(image, s, (x, y),
           cv.FONT_HERSHEY_PLAIN, 1.0, (255, 25, 255),
           thickness, lineType)
    except Exception as e:
        logging.error('drawStr: %s'%(e))

def drawRect(image, pt1=(0,0), pt2=(100,100), color=(0, 255, 0)):
    try:
        lineType = cv.LINE_AA
        thickness = 2
        #pt1 = (x-x, y-x)
        #pt2 = (x//2, y//2)
        #color2 = (0, 255, 0)
        cv.rectangle(image, pt1, pt2, color, thickness, lineType)
    except Exception as e:
        logging.error('drawRect: %s'%(e))

def drawRegions(regions, x1, y0, display=False):
    try:
        drawRect(regions, (0, 0), (x1, y0), color=(0, 255, 0))
        drawRect(regions, (0, 0), (x1//2, y0//2), color=(230, 255, 0))
        drawRect(regions, ((x1 - x1//2), 0), (x1, y0//2),
            color=(0, 255, 230))
        drawRect(regions, (0, y0//2), (x1 - x1//2, y0), color=(230, 0, 0))
        drawRect(regions, ((x1 - x1//2), (y0 - y0//2)), (x1, y0),
            color=(100, 230, 23))
        drawStr(regions, (x1//2, y0//2), 'ROI 0')
        drawStr(regions, (x1//4, y0//4), 'ROI 1')
        drawStr(regions, ((x1 - x1//4), y0//4), 'ROI 2')
        drawStr(regions, (x1//4, (y0 - y0//4)), 'ROI 3')
        drawStr(regions, ((x1 - x1//4), (y0 - y0//4)), 'ROI 4')
        if(display):
            print(f'{mytime2b()} \nPress [esc] to quit..... ')
            imageShow('Regions', regions)
            cv.waitKey(0)
    except Exception as e:
        logging.error('drawRegions: %s'%(e))

mcount = [0]
def onmouse(event='a',x='b',y='c',flags='d',param='e'):
    global spikes
    try:
        if((mcount[0] < 10) or (mcount[0] % 250) == 0 ):
            print('#%s onmouse...event: %s, x: %s, y: %s,\
                flags: %s, param: %s'%(
                    mcount[0], event, x, y, flags, param))
        if (event == cv.EVENT_LBUTTONDOWN):
            color = spikes[0][y, x]
            print('#%s eventXY: %s @(%s, %s),\
                color: %s'%(mcount, event, x, y, color))
            spikes = imageTool2(spikes[0], color, True)
        mcount[0] += 1
    except Exception as e:
        logging.error('onmouse: %s'%(e))

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

async def nearestNeighborColor(image, dx, dy, ref, noise=5):
    color0 = (0,0,0)
    try:
        colors = []
        distance = []
        y, x, c = image.shape
        b0, g0, r0 = image[dy, dx]
        bref0, gref0, rref0 = ref[dy, dx]
        color0 = (b0, g0, r0)
        color0r = (bref0, gref0, rref0)
        #print('color0: (%s, %s, %s)'%(color0))
        #print('dy: %s, dx: %s'%(dy, dx))
        #Region 1
        task1x = asyncio.create_task(regionNorth(image, ref, x, y, c, dx, dy,
            color0, color0r, noise))
        #Region 2
        task2x = asyncio.create_task(regionEast(image, ref, x, y, c, dx, dy,
            color0, color0r, noise))
        #Region 4
        task3x = asyncio.create_task(regionSouth(image, ref, x, y, c, dx, dy,
            color0, color0r, noise))
        #Region 3
        task4x = asyncio.create_task(regionWest(image, ref, x, y, c, dx, dy,
            color0, color0r, noise))
        #
        #print(f'Tasks... {dy}, {dx}')
        distance1x = await task1x
        for x1 in distance1x:
            distance.append(int(x1[0]))
            colors.append(x1[1])
        #
        #print(f'd1: {distance1x[1][0]}, {distance1x[1][4]}')
        distance2x = await task2x
        for x2 in distance2x:
            distance.append(int(x2[0]))
            colors.append(x2[1])
        #
        distance3x = await task3x
        for x3 in distance3x:
            distance.append(int(x3[0]))
            colors.append(x3[1])
        #
        #print(f'd3: {distance3x[0][0]}, {distance3x[0][4]}')
        distance4x = await task4x
        for x4 in distance4x:
            distance.append(int(x4[0]))
            colors.append(x4[1])
        #
        '''#
        logging.info('###   ###\n#\n#\n'
        '(dy: %s, dx: %s) [%s], \n'
        '(%s, %s), d1: %s, [%s], Region: %s\n'
        '(%s, %s), d2: %s, [%s], Region: %s\n'
        '(%s, %s), d3: %s, [%s], Region: %s\n'
        '(%s, %s), d4: %s, [%s], Region: %s\n'
        '(%s, %s), d5: %s, [%s], Region: %s\n'
        '(%s, %s), d6: %s, [%s], Region: %s\n'
        '(%s, %s), d7: %s, [%s], Region: %s\n'
        '(%s, %s), d8: %s, [%s], Region: %s\n'%(
            dy, dx, color0,
            distance1x[0][3], distance1x[0][2], distance1x[0][0],
            distance1x[0][1], distance1x[0][4],
            distance1x[1][3], distance1x[1][2], distance1x[1][0],
            distance1x[1][1], distance1x[1][4],
            distance2x[0][3], distance2x[0][2], distance2x[0][0],
            distance2x[0][1], distance2x[0][4],
            distance2x[1][3], distance2x[1][2], distance2x[1][0],
            distance2x[1][1], distance2x[1][4],
            distance3x[0][3], distance3x[0][2], distance3x[0][0],
            distance3x[0][1], distance3x[0][4],
            distance3x[1][3], distance3x[1][2], distance3x[1][0],
            distance3x[1][1], distance3x[1][4],
            distance4x[0][3], distance4x[0][2], distance4x[0][0],
            distance4x[0][1], distance4x[0][4],
            distance4x[1][3], distance4x[1][2], distance4x[1][0],
            distance4x[1][1], distance4x[1][4])
        )
        #'''
        #
        min = distance[0]
        colorX = colors[0]
        n = 0
        xn = 0
        for d in distance:
            if(d < min):
                min = d
                colorX = colors[n]
                xn = n
            elif(d <= min):
                c1 = [(int(color0[0]) - int(colors[xn][0])),
                    (int(color0[1]) - int(colors[xn][1])),
                    (int(color0[2]) - int(colors[xn][2]))]
                #c2 = np.subtract(color0, colors[n])
                c2 = [(int(color0[0]) - int(colors[n][0])),
                    (int(color0[1]) - int(colors[n][1])),
                    (int(color0[2]) - int(colors[n][2]))]
                s1 = int(c1[0]) + int(c1[1]) + int(c1[2])
                s2 = int(c2[0]) + int(c2[1]) + int(c2[2])
                #logging.info('#\n# # #\n%s, d: %s, \nc: %s, c1: %s,\
                #    c2: %s,\n s1: %s, s2: %s'%(
                #        n, d,
                #        color0, colors[xn], colors[n],
                #        s1, s2))
                if(abs(s2) > abs(s1)):
                    min = d
                    colorX = colors[xn]
                    xn = n
                else:
                    min = d
                    colorX = colors[n]
                    xn = n
            n += 1
        return colorX
    except Exception as e:
        logging.error('nearestNeighborColor: %s'%(e))
    return color0

async def regionNorth(image, ref, x, y, c, dx, dy, color0, color0r, noise):
    distanceList = []
    try:
        #Region 1
        #print(f'North.........{dy}, {dx}........')
        color1 = color0
        color1r = color0r
        dx1 = dx - noise - 1
        dy1 = dy - noise - 1
        while ((dx1 > 0) and (dy1 > 0) and (color1r == color0r)):
            b1, g1, r1 = image[dy1, dx1]
            color1 = (b1, g1, r1)
            bref1, gref1, rref1 = ref[dy1, dx1]
            color1r = (bref1, gref1, rref1)
            dx1 -= 1
            dy1 -= 1
        dxdy1 = ((dx - dx1)*(dx - dx1)) + ((dy - dy1)*(dy - dy1))
        distance1 = sqrt(dxdy1)
        colors1 = [distance1, color1, dx1, dy1, next(regionNames)]
        distanceList.append(colors1)
        #North n
        colorn = color0
        colornr = color0r
        dxn = dx
        dyn = dy - noise - 1
        while ((dyn > 0) and (colornr == color0r)):
            bn, gn, rn = image[dyn, dxn]
            colorn = (bn, gn, rn)
            brefn, grefn, rrefn = ref[dyn, dxn]
            colornr = (brefn, grefn, rrefn)
            #dxn = dx
            dyn -= 1
        dxdyn = ((dx - dxn)*(dx - dxn)) + ((dy - dyn)*(dy - dyn))
        distancen = sqrt(dxdyn)
        colorsn = [distancen, colorn, dxn, dyn, next(regionNames)]
        distanceList.append(colorsn)
        #print(f'#\nNorth .....{dyn}, {dxn}..........done.\n#')
    except Exception as e:
        logging.error('regionNorth: %s'%(e))
    return distanceList

async def regionEast(image, ref, x, y, c, dx, dy, color0, color0r, noise):
    distanceList = []
    try:
        #print(f'East....{dy}, {dx}......')
        #print('regionEast: (%s, %s), %s, %s'%(dx, dy, color0, color0r))
        #Region 2
        color2 = color0
        color2r = color0r
        dx2 = dx + noise + 1
        dy2 = dy - noise - 1
        while ((dx2 < x) and (dy2 > 0) and (color2r == color0r)):
            b2, g2, r2 = image[dy2, dx2]
            color2 = (b2, g2, r2)
            bref2, gref2, rref2 = ref[dy2, dx2]
            color2r = (bref2, gref2, rref2)
            dx2 += 1
            dy2 -= 1
        dxdy2 = ((dx2 - dx)*(dx2 - dx)) + ((dy2 - dy)*(dy2 - dy))
        distance2 = sqrt(dxdy2)
        distanceList.append([distance2, color2, dx2, dy2, next(regionNames)])
        #East e
        colore = color0
        colorer = color0r
        dxe = dx + noise + 1
        dye = dy
        while ((dxe < x) and (colorer == color0r)):
            be, ge, re = image[dye, dxe]
            colore = (be, ge, re)
            brefe, grefe, rrefe = ref[dye, dxe]
            colorer = (brefe, grefe, rrefe)
            dxe += 1
            #dye = dy
        dxdye = ((dx - dxe)*(dx - dxe)) + ((dy - dye)*(dy - dye))
        distancee = sqrt(dxdye)
        colorse = [distancee, colore, dxe, dye, next(regionNames)]
        distanceList.append(colorse)
        #print(f'#\nEast..{dy2}, {dx2}....done.\n#')
    except Exception as e:
        logging.error('regionEast: %s'%(e))
    return distanceList

async def regionSouth(image, ref, x, y, c, dx, dy, color0, color0r, noise):
    distanceList = []
    try:
        #print(f'South...{dy}, {dx}.......')
        #print('regionSouth: (%s, %s), %s, %s'%(dx, dy, color0, color0r))
        #Region 4
        color4 = color0
        color4r = color0r
        dx4 = dx + noise + 1
        dy4 = dy + noise + 1
        while ((dx4 < x) and (dy4 < y) and (color4r == color0r)):
            b4, g4, r4 = image[dy4, dx4]
            color4 = (b4, g4, r4)
            bref4, gref4, rref4 = ref[dy4, dx4]
            color4r = (bref4, gref4, rref4)
            dx4 += 1
            dy4 += 1
        dxdy4 = ((dx4 - dx)*(dx4 - dx)) + ((dy4 - dy)*(dy4 - dy))
        distance4 = sqrt(dxdy4)
        distanceList.append(
           [distance4, color4, dx4, dy4, next(regionNames)])
        #South s
        colors = color0
        colorsr = color0r
        dxs = dx
        dys = dy + noise + 1
        while ((dys < y) and (colorsr == color0r)):
            bs, gs, rs = image[dys, dxs]
            colors = (bs, gs, rs)
            brefs, grefs, rrefs = ref[dys, dxs]
            colorsr = (brefs, grefs, rrefs)
            #dxs = dx
            dys += 1
        dxdys = ((dx - dxs)*(dx - dxs)) + ((dy - dys)*(dy - dys))
        distances = sqrt(dxdys)
        colorss = [distances, colors, dxs, dys, next(regionNames)]
        distanceList.append(colorss)
        #print(f'#\nSouth....{dys}, {dxs}.......done.\n#')
    except Exception as e:
        logging.error('regionSouth: %s'%(e))
    return distanceList

async def regionWest(image, ref, x, y, c, dx, dy, color0, color0r, noise):
    distanceList = []
    try:
        #print(f'West....{dy}, {dx}....')
        #print('regionWest: (%s, %s), %s, %s'%(dx, dy, color0, color0r))
        #Region 3
        color3 = color0
        color3r = color0r
        dx3 = dx - noise - 1
        dy3 = dy + noise + 1
        while ((dx3 > 0) and (dy3 < y) and (color3r == color0r)):
            b3, g3, r3 = image[dy3, dx3]
            color3 = (b3, g3, r3)
            bref3, gref3, rref3 = ref[dy3, dx3]
            color3r = (bref3, gref3, rref3)
            dx3 -= 1
            dy3 += 1
        dxdy3 = ((dx - dx3)*(dx - dx3)) + ((dy3 - dy)*(dy3 - dy))
        distance3 = sqrt(dxdy3)
        distanceList.append(
            [distance3, color3, dx3, dy3, next(regionNames)])
        #West w
        colorw = color0
        colorwr = color0r
        dxw = dx - noise - 1
        dyw = dy
        while ((dxw > 0) and (colorwr == color0r)):
            bw, gw, rw = image[dyw, dxw]
            colorw = (bw, gw, rw)
            brefw, grefw, rrefw = ref[dyw, dxw]
            colorwr = (brefw, grefw, rrefw)
            dxw -= 1
            #dyw = dy
        dxdyw = ((dx - dxw)*(dx - dxw)) + ((dy - dyw)*(dy - dyw))
        distancew = sqrt(dxdyw)
        colorsw = [distancew, colorw, dxw, dyw, next(regionNames)]
        distanceList.append(colorsw)
        #print(f'#\nWest ....{dyw}, {dxw}...... done.\n###')
    except Exception as e:
        logging.error('regionWest: %s'%(e))
    return distanceList

def closedOpenExperiment(image, display=False):
    """
    TDD: Version 01
    Experiment...
    If the linestrings is closed, it is a polygon.
    If the first point is the same as the last string,
    the linestrings is closed.
    If the first point is not the same as the last string,
    the linestrings is open.
    TDD: V01, Testing123.......
    Experiment.... Enjoy :)
    TDD: V02, uses qgis and pyqgis to implement the solution.
    """
    try:
        info = 'TDD: V01, Testing123... Experiment..., \n \
            TDD: V02, uses qgis and pyqgis to implement the solution.'
        size1 = len(image)
        pprint.pprint(image)
        y, x, c = image.shape
        size2 = image.size
        linestrings1 = []
        linestrings2 = []
        p3 = image[0,0,0]
        p2 = image[0,0]
        print(f'{mytime2b()} Testing123...Experiment... :)\
            \nclosedOpen: {size1}, \n(y: {y}, x: {x}, c: {c}),\
            \nsize: {size2}, \np3: {p3}, \np2: {p2}')
        # Convert it to gray
        A = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        lA = len(A)
        pa = image[y//2, x//2]
        M, N = A.shape
        #
        #svd: Singular Value Decomposition.
        #Vh: Hermitian matrix, A matrix V ϵ Ϲⁿˣⁿ is Hermitian if V = Vᴴ.
        #If there exists an orthogonal matrix X of eigenvectors and
        # diagonal matrix D of eigenvalues such that D = XᵀAX.
        #Therefore any y→ ϵ Rⁿ can be decomposed into a linear combination
        # of the eigenvectors of a Hermitian A.
        #
        unitaryMatrixU, spectrum, unitaryMatrixVh = linalg.svd(A)
        sig = linalg.diagsvd(spectrum, M, N)
        U, Vh = unitaryMatrixU, unitaryMatrixVh
        print(f'#\n#shape({M}, {N}), len: {lA}  \n#unitaryMatrixU,\
            sig, unitaryMatrixVh \n#')
        pprint.pprint(U)
        pprint.pprint(sig)
        pprint.pprint(Vh)
        for p1 in range(y):
            temp1 = []
            temp2 = []
            for p2 in range(x):
                pb = image[p1,p2]
                if (pb[0],pb[1],pb[2]) != (pa[0],pa[1],pa[2]):
                    temp1.append(pb)
                    temp2.append([0, 0, 250])
                elif (pb[0],pb[1],pb[2]) == (pa[0],pa[1],pa[2]):
                    temp2.append(pb)
                    temp1.append([0, 0, 250])
                else:
                    temp1.append([250, 0, 250])
                    temp2.append([250, 0, 250])
            linestrings1.append(temp1)
            linestrings2.append(temp2)
        print(f'#\n# upperShape: {U.shape}')
        print(f'#\n# sigShape: {sig.shape}')
        print(f'#\n# vhShape: {Vh.shape}')
        s2 = len(linestrings1)
        #unitaryMatrixQ, upperTrapezoidalMatrixR = linalg.qr(image[y//2])
        unitaryMatrixQ, upperTrapezoidalMatrixR = linalg.qr(A)
        template1 = np.array(linestrings1, dtype='uint8')
        template2 = np.array(linestrings2, dtype='uint8')
        print(f'#\n# unitaryMatrixQ: {unitaryMatrixQ.shape}, \n\
        upperTrapezoidalMatrixR: {upperTrapezoidalMatrixR.shape} \n\
        linestrings: {template1.shape}\n#')
        pprint.pprint(unitaryMatrixQ)
        pprint.pprint(upperTrapezoidalMatrixR)
        pprint.pprint(template1)
        pprint.pprint(template2)
        print(f'{mytime2b()} TDD, Version 01, \nclosedOpen: {size1}, \n \
            (y: {y}, x: {x}, c: {c}), \nsize: {size2}, \ns2: {s2}')
        print(f'{info} \nIt\'s time to use qgis and pyqgis. Enjoy :-)')
        logging.info(
            f'{info} \nIt\'s time to use qgis and pyqgis. Enjoy :-)')
        if (display):
            print(f'{mytime2b()} \nPress [esc] to quit..... ')
            imageShow('unitaryMatrixU', U)
            imageShow('sig', sig)
            #imageShow('unitaryMatrixVh', Vh)
            #imageShow('unitaryMatrixQ', unitaryMatrixQ)
            #imageShow('upperTrapezoidalMatrixR', upperTrapezoidalMatrixR)
            imageShow(f'linestrings: {next(regionNames)}', template1)
            imageShow(f'linestrings: {next(regionNames)}', template2)
            print(f'#\n# Press: {next(regionNames)[::-1][0]} to exit.\n#')
            cv.waitKey(0)
        return True
    except Exception as e:
        print(f'closedOpen: {e}')
    return False

def cleanupLog(filelog):
    try:
        with open(filelog, 'w') as file:
            file.write('#\n# logs: %s\n#\n'%(mytime2b()))
    except Exception as e:
        print("cleanupLog: %s"%(e))

def mytimeDb():
    dz = datetime.timezone.utc
    d2 = datetime.datetime.utcnow()
    d3 = d2.microsecond
    d4 = (d2.year, d2.month, d2.day,
        d2.hour, d2.minute, d2.second, d3%1000)
    utcnow = datetime.datetime(d4[0], d4[1], d4[2], d4[3], d4[4], tzinfo=dz)
    return utcnow

async def main():
    print('main...')
    #cleanupLog(logfile)
    try:
        parser = argparse.ArgumentParser(
           description='Tool to remove spikes from an image.')
        spikes01 = 'spikes.jpg'
        spikes02 = 'dblayers005v1.png'
        link = f'./data01/{spikes02}'
        parser.add_argument(
            '--input', help='Path to input image.', default=link)
        args = parser.parse_args()
        app = QgistoolApp(args.input)
        display = True
        closedOpenExperiment(app.lineStrings())
        #app.imageGraph()
        #app.vstackDataframe()
        #app.hstackDataframe()
        #app.imageHistogram()
        #imageShow(app.links, app.image['data'])
        colorX = getColor(app.image['data'])
        imageTool2(app.image['data'], colorX, display)
        #imageTool3(app.image['data'], display)
        p1 = 3
        p2 = 3
        #erosion = app.imageErosion(p1, p2, display)
        #dilation = app.imageDilation(p1, p2, display)
        opening = app.imageOpening(p1, p2)
        closing = app.imageClosing(p1, p2)
        #app.imageGradient(display)
        #app.imageTophat(display)
        #app.imageBlackhat(display)
        #
        await app.imageTool(display)
        y0X, x1X, c2X = opening.shape
        tool2 = imageTool2(opening, colorX)
        #tool2 = imageTool2(erosion, (25,70,250))
        regions = tool2[2]
        drawRegions(regions, regions.shape[1], regions.shape[0])
        y0, x1, c2 = tool2[0].shape
        tool = await removeSpikes(
            closing, tool2, y0, x1, c2,
            alpha=1.2, beta=5, display=display)
        #tool = await removeSpikes(
        #    dilation, tool2, y0, x1, c2,
        #    alpha=1.2, beta=5, display=display)
        closedOpenExperiment(app.lineStrings(), display)
        closedOpenExperiment(tool[2], display)
        closedOpenExperiment(tool[3], display)
        print('tool2list = [image0, imageSpikes1,\
            cdstPspikes2, cdstPblack3, cdstPwhite4,\
            imageWhite5, imageGray6, template7]')
        print('toolList = [tool2[0], spikes, template1, template2]')
    except Exception as e:
        logging.error('main: %s'%(e))
    print(f'{mytime2b()} Done.')

cleanupLog(logfile)

if __name__ == '__main__':
    try:
        asyncio.run(main())
        cv.destroyAllWindows()
    except Exception as e:
        logging.error('QgistoolApp model: %s'%(e))
