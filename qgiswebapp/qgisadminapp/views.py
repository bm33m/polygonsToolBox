#
#@author: Brian
#
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import make_aware
from django.conf import settings
from qgisadminapp.models import (gisTablesAdmin,
    gisDatabaseAdmin, readQgis, readZip)
import pprint
import json
import datetime
import time

def index(request):
    """QGIS Admin Index, return table names."""
    subject = 'QGIS Admin Info101.'
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    ref = [0]
    dbtables = []
    numberOfTables = 0
    display = 3
    try:
        gpkg = settings.QGIS_PKG
        dbtables = gisTablesAdmin(gpkg)
        numberOfTables = len(dbtables)
        if(numberOfTables > 0):
            display = 60 if(numberOfTables > 60) else 25
            pprint.pprint(dbtables)
    except Exception as e:
        print("Qgisadmin1 error: ", e)
    paginator = Paginator(dbtables, display)
    page = request.GET.get('page')
    tablesinfo = paginator.get_page(page)
    return render(
        request, 'qgisadmin.html', context={'pname': pname, 'message': now,
        'numberOfTables': numberOfTables, 'tables': tablesinfo,
        'subject': subject, 'admin': subject,
        'ip': ip, 'year': year},
    )

ref3 = [0]
def dbtables(request):
    """Request info about the db tables."""
    subject = 'Qgis data Info202.'
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    ref = [0]
    dbtables = []
    numberOfTables = 0
    display = 3
    data = [{}]
    table = ""
    try:
        gpkg = settings.QGIS_PKG
        dbtables = gisTablesAdmin(gpkg)
        numberOfTables = len(dbtables)
        if(numberOfTables > 0):
            display = 60 if(numberOfTables > 60) else 25
        if request.method == 'POST':
            req = request.POST
            table = req['dbtable'].strip()
            data = gisDatabaseAdmin(gpkg, table)
            subject = table
    except Exception as e:
        print("dbtables Qgisadmin2 error: ", e)
    paginator = Paginator(dbtables, display)
    page = request.GET.get('page')
    tablesinfo = paginator.get_page(page)
    return render(
        request, 'qgisadmin.html', context={'pname': pname,
        'message': "%s %s"%(now, subject), 'numberOfTables': numberOfTables,
        'tables': tablesinfo, 'subject': subject, 'table': table,
        'admin': subject, 'data': data, 'ip': ip, 'year': year},
    )

def qgisdata(request):
    """Read/request qgs file."""
    pname = settings.PRO_NAME
    projectUrl = settings.PRO_URL
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    app = {}
    qgs = 'spiky-polygons.qgs'
    qgis = qgs
    qgisFile = qgs
    try:
        if request.method == 'GET':
            req = request.GET
            qgz = req["qgz"].strip()
            qUrl = "%s%s/%s?qgz=%s"%(projectUrl, 'qgisadmin', 'qgis', qgz)
            qgisFile = readQgis(qUrl)
    except Exception as e:
        print("qgisdata: %s"%(e))
    return render(
        request, 'qgisadmin.html', context={'pname': pname, 'app': app,
        'qgis': qgis, 'qgs': qgs, 'qgisFile': qgisFile, 'message': now,
        'admin': qgs, 'ip': ip, 'year': year},
    )

def qgis(request):
    """Request qgs file."""
    project = settings.QGIS_PROJECTS
    qgs = 'spiky-polygons.qgs'
    qgz = '%sspiky-polygons.qgz'%(project)
    try:
        if request.method == 'GET':
            req = request.GET
            qgs = req["qgz"].strip()
            a = len(qgs) - 4
            if qgs[a:] == '.qgz':
                qgz = '%s%s'%(project, qgs)
                #print(qgz)
                qgs = readZip(qgz)
    except Exception as e:
        print("qgis: %s"%(e))
    return HttpResponse(qgs)

def graphVertexes(request):
    """Request graph vertexes."""
    qgs = 'spikes.jpg'
    graph = {}
    try:
        qgs = request["image"]
    except Exception as e:
        print("graphVertexes: %s"%(e))
    return render(
        request, 'qgisdata.html', context={'qgs': qgs},
    )

def removeSpikes(request):
    """Remove spikes from the polygons."""
    qgs = 'spikes.jpg'
    graph = {}
    try:
        qgs = request["image"]
    except Exception as e:
        print("graphVertexes: %s"%(e))
    return render(
        request, 'qgisdata.html', context={'qgs': qgs},
    )

def mytime2():
    """What is the time now?"""
    now = datetime.datetime.now()
    dnow = make_aware(now)
    utcnow = datetime.datetime.utcnow()
    unow = make_aware(utcnow)
    dt = (dnow - unow)
    print("UTC:  %s,   %s, %s-%s"%(utcnow, dt, unow, unow.tzinfo))
    print("Home: %s-%s,       %s-%s"%(now, now.tzinfo, dnow, dnow.tzinfo))
    return dnow
