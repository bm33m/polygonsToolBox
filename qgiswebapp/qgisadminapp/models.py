from django.db import models
from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from django.utils.timezone import make_aware
import sqlite3
import datetime
import time
import sys
import zipfile
import urllib.request
import logging
logfile = 'qadmin.log'
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filename=logfile,
    level=logging.DEBUG)
#import pandas as pd

# Create your models here.

def gisTablesAdmin(gpkg):
    """Connect to the database and get table names."""
    data = [{}]
    try:
        logging.info("%s gisTablesAdmin: %s"%(mytime2b(), gpkg))
        conn = sqlite3.connect(gpkg)
        cursor = conn.cursor()
        dbtables = ('table',)
        statement = "SELECT name FROM sqlite_master WHERE type=?"
        cursor.execute(statement, dbtables)
        data2 = cursor.fetchall()
        conn.close()
        for xlist in data2:
            for x in xlist:
                data.append(x)
    except Exception as e:
        logging.error("qgisadminpp gis tables: %s"%(e))
    #print("gisTablesAdmin: %s"%(data))
    return data

def gisDatabaseAdmin(gpkg, table):
    """Get data from the database on a specific table."""
    data = [{}]
    statement = "SELECT * FROM gpkg_contents;"
    try:
        logging.info("%s gisDatabaseAdmin: %s, %s"%(mytime2b(), gpkg, table))
        dbtables = gisTablesAdmin(gpkg)
        for x in dbtables:
            #print("dbtable: %s %s"%(x, table))
            if (x == table):
                statement = "SELECT * FROM '%s';"%(x)
                break
        conn = sqlite3.connect(gpkg)
        cursor = conn.cursor()
        cursor.execute(statement)
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        logging.error("qgisadminpp database: %s"%(e))
    #print("gisDatabaseAdmin: %s"%(data))
    return data

def readQgis(urlFile):
    """Read the qgis file."""
    df = {}
    data = {}
    try:
        with urllib.request.urlopen(urlFile) as response:
            df = response.read()
        data = df.decode('utf8')
        #data = {'headers': df.headers(),
        #    'body': df.body().data().decode('utf8')}
        #url = (urlFile)
        #df = pd.read_html(url)
        #df = pd.read_xml(url)
        #print(df)
    except Exception as e:
        logging.error("qgisadminpp readQgis: %s"%(e))
    return data

def readZip(qgzfile):
    zip1 = {}
    try:
        project = settings.QGIS_PROJECTS
        #print(project, qgzfile)
        logging.info('%s readZip: %s, %s'%(mytime2b(), project, qgzfile))
        zf = zipfile.ZipFile(qgzfile)
        lst = zf.namelist()
        #print(lst)
        qgs = lst[0]
        a = len(qgs) - 4
        if qgs[a:] == '.qgs':
            with zf.open(qgs) as f1:
                if(f1):
                    #print(f1)
                    zip1 = f1.read()
    except Exception as e:
        logging.error("readZip: %s"%(e))
    return zip1

class UploadFile(forms.Form):
    imageLink = forms.CharField(max_length=250)
    filename = forms.FileField(label=" ", label_suffix="+")

    def sanitizeFile(self):
        #print("Self: %s"%(self))
        file = self.cleaned_data['filename']
        ext = file.name.split('.')[-1].lower()
        if ext not in ['jpg', 'png']:
            return 0, 0
        return file, ext

def checkFile(request, folder, link, ref):
    if request.method == 'POST':
        try:
            req = request.POST
            req2 = request.FILES
            size = req2['filename'].size
            maxb = (1024 * 500)
            #print("File Size: %s / %s"%(size, maxb))
            if size > maxb:
                return 0
            form = UploadFile(req, req2)
            if form.is_valid():
                #freq = req2['filename'].file.read()
                ufile, ext =  form.sanitizeFile()
                if ext == 0:
                    return 0
                else:
                    filereq = ufile.file.read()
                    userfile = saveFile(filereq, folder, link, ref, ext)
                    file3 = "file: %s-%s"%(userfile, size)
                    #print(file3)
                    logging.info("saveFile: %s"%(file3))
                    return userfile
        except Exception as e:
            logging.error("qgisadminpp checkFile: %s"%(e))
    return 0

def saveFile(file, folder, link, ref, ext):
    try:
        pfile = 'assets/%s/%s/%s.%s'%(folder, link, ref, ext)
        path = default_storage.save(pfile, ContentFile(file))
        return path
    except Exception as e:
        logging.error("qgisadminpp saveFile: %s"%(e))
    return 0

def account2(ref):
    ref[0] += 1
    #d2 = mytime2b()
    d2 = mytimeDb()
    d3 = d2.microsecond
    accn = "%d%d%d%d%d%d%d"%(d2.year, d2.month, d2.day,
        d2.hour, d2.minute, d2.second, d3%1000)
    sern = int(accn) + ref[0]
    return sern

def mytime2b():
    now = datetime.datetime.now()
    return now

def mytimeDb():
    #now = datetime.datetime.now()
    #dnow2 = make_aware(now)
    utcnow = datetime.datetime.utcnow()
    dnow = make_aware(utcnow)
    #dt = (dnow2 - dnow)
    #print("Users model: %s, %s"%(dnow, dt))
    return dnow

def cleanupLog(filelog):
    """Cleanup log file.
    """
    try:
        with open(filelog, 'w') as file:
            file.write('#\n# logs: %s\n#\n'%(mytime2b()))
    except Exception as e:
        print("cleanupLog: %s"%(e))

cleanupLog(logfile)
