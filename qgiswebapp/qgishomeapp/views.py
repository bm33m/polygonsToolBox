#
# @author: Brian
#
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import make_aware
from django.conf import settings
from qgishomeapp.models import gisTablesHome, mapHome, maps
from qgisadminapp.models import account2, checkFile
from qgistoolapp.spikestool import imageInfo
import pprint
import json
import datetime
import time


def index(request):
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    map = mapHome()
    app = {"map": map[0], "info": "%s %s"%(now, map[1])}
    return render(
        request, 'home.html', context={'pname': pname, 'message': now,
        "app": app, 'ip': ip, 'year': year},
    )

ref3 = [0]
def imagefilter(request):
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    info = gisTablesHome()
    map = maps()
    image = {}
    link = ""
    imageName = ""
    try:
        if request.method == 'POST':
            req = request.POST
            link = req['imageLink'].strip()
            imageName = req['imageName'].strip()
            image = imageInfo(link)
            if(image["data"] is None):
                profile = "maps"
                ref = account2(ref3)
                link = checkFile(request, profile, link, ref)
                print("imageLink: %s"%(link))
                image = imageInfo(link)
    except Exception as e:
        print("imagefilter: %s"%(e))
    folder = "qgishomeapp"
    return render(
        request, 'info.html', context={'pname': pname,
        'message': "%s %s"%(now, link), "video1": map[1], "poster1": map[0],
        'imageName': imageName, "app": map, 'info': info, "folder": folder,
        "image": image, 'ip': ip, 'year': year},
    )

def qgisinfo(request):
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    info = gisTablesHome()
    map = maps()
    folder = "qgishomeapp"
    return render(
        request, 'info.html', context={'pname': pname, 'message': now,
        "video1": map[1], "poster1": map[0], "app": map, 'info': info,
        "folder": folder, 'ip': ip, 'year': year},
    )

def mytime2():
    now = datetime.datetime.now()
    dnow = make_aware(now)
    utcnow = datetime.datetime.utcnow()
    unow = make_aware(utcnow)
    dt = (dnow - unow)
    print("UTC:  %s,   %s, %s-%s"%(utcnow, dt, unow, unow.tzinfo))
    print("Home: %s-%s,       %s-%s"%(now, now.tzinfo, dnow, dnow.tzinfo))
    return dnow
