import sys
import filecmp
from multiprocessing import Pool, TimeoutError
import os
import datetime
import time
import asyncio
import pprint
import json
import logging
from qgisadminapp.models import account2, cleanupLog

logfile1 = 'qadmin.log'
logfile = 'qgistoolapp/qtoolapp2.log'
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filename=logfile,
    level=logging.DEBUG)

def mytime2b():
    now = datetime.datetime.now()
    return now

logging.info(mytime2b())

try:
    import cv2 as cv
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    import networkx as nx
    from scipy import linalg
except Exception as e:
    logging.critical('%s qgistoolapp models: %s'%(mytime2b(), e))

def xmlData(urlFile=None, save=True):
    """Read the content of the qgs project file.
    """
    df = {}
    des = ''
    try:
        if(urlFile is None):
            urlFile = 'qgistoolapp/templates/spikesdata.qgs'
        url = (urlFile)
        df = pd.read_xml(url)
        #info = df.info()
        print('df: \n', len(df))
        d2 = df.to_numpy()
        #df2 = pd.DataFrame(df[0:])
        pprint.pprint(d2)
        #for rows in df:
        #    print(rows)
        #    #print(df[rows])
        if (save):
            des = dataDes(df)
        #print('data: \n', df)
    except Exception as e:
        print('xmlData: ', e)
        logging.error('xmlData: %s'%(e))
    return df, des

ref3 = [0]
def dataDes(info):
    """Create a stats image and save it on tempDir for web rendering.
    """
    path = ''
    try:
        des = info.describe()
        #print('des: \n', des)
        ref = account2(ref3)
        path1 = 'qgistoolapp/static/qgistoolapp/assets/%s.png'%(ref)
        plt.title('info: %s'%(path1))
        plt.plot(des)
        #plt.show()
        #
        # Save the temp image for web rendering.
        #
        plt.savefig(path1)
        path = path1.split('static/')[1]
        cleanupLog(logfile1)
    except Exception as e:
        print('dataDes: ', e)
        logging.error('dataDes: %s'%(e))
    return path

def htmlData(urlFile=None):
    df = {}
    try:
        if(urlFile is None):
            urlFile = 'qgistoolapp/templates/spikesdata.qgs'
        url = (urlFile)
        df = pd.read_html(url)
        #print(df)
    except Exception as e:
        logging.error('htmlData: %s'%(e))
    return df

def imageInfo(link):
    """Read the content of the image file.
    """
    image = {}
    try:
        image1 = cv.imread(link)
        image["data"] = image1
        image["shape"] = image1.shape
        image["size"] = image1.size
        image["dtype"] = image1.dtype
    except Exception as e:
        print("imageInfo: %s"%(e))
    return image

async def fileCleanup(fileList, path, max=10, delay=10):
    """Cleanup temp files.
    """
    try:
        path1 = '%s%s'%(tempDir()[1], path)
        print('\n#\n%s \nfileCleanup: %s, %s, \nList: %s\n#\n'%(
           mytime2b(), path, delay, len(fileList)))
        #await asyncio.sleep(delay)
        time.sleep(delay)
        fileList.append(path1)
        if (len(fileList) > max):
            path2 = fileList.pop([0])
            #os.remove(path2)
            os.unlink(path2)
            print('%s fileCleanup: %s, %s'%(mytime2b(), path2, delay))
        print(f'\n#\n#{mytime2b()}, fileList: {len(fileList)}\n#\n#\n')
    except Exception as e:
        print('# fileCleanup: ', e)

async def tempFiles(dcmp):
    """Cleanup temp files.
    """
    try:
        print('\n%s tempFiles: \n%s, \n765433$, \n%s\n'%(
            mytime2b(), dcmp.left, dcmp.right))
        names = os.listdir(dcmp.right)
        i = 0
        for name in names:
            print('#%s tempFiles: %s'%(i, name))
            os.remove('%s%s'%(dcmp.right, name))
            i += 1
    except Exception as e:
        print(f'{mytime2b()} tempFiles: {e}')
        logging.error('tempFiles: %s'%(e))

def tempDir():
    dir1 = 'qgistoolapp/data/'
    dir2 = 'qgistoolapp/static/'
    dir3 = 'qgistoolapp/static/qgistoolapp/assets/'
    return [dir1, dir2, dir3]

cleanupLog(logfile)
cleanupLog(logfile1)
print('%s'%(
"""
   We are done.
   Version 02 uses pyqgis to implement the solution.
   Enjoy :-)
""")
)
