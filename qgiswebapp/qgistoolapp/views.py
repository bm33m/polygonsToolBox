from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import make_aware
from django.conf import settings
from qgistoolapp.spikestool import xmlData, htmlData, fileCleanup
import datetime
import time
import asyncio

def index(request):
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    df, imagePath = xmlData()
    info = df.to_html()
    try:
        xml = xmlinfo(request, df, info, imagePath)
        cleanupFile(imagePath)
        print(f'{now} done...@1 index.')
    except Exception as e:
        print(f'{now} index: {e}')
    return xml

def xmlinfo(request, df, info, imagePath):
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    return render(
        request, 'datatool.html', context={'pname': pname, 'message': now,
        'df': df, 'info': info, 'des': imagePath, 'ip': ip, 'year': year},
    )

def htmlinfo(request):
    pname = settings.PRO_NAME
    ip = request.META['REMOTE_ADDR']
    now = mytime2()
    year = now.year
    df = htmlData()
    return render(
        request, 'datatool.html', context={'pname': pname, 'message': now,
        'df': df, 'ip': ip, 'year': year},
    )

fileList = []
def cleanupFile(path):
    try:
        asyncio.run(tasks(path))
        print(f'{mytime2()} done: {path} @2 cleanupFile.')
    except Exception as e:
        print(f'# {mytime2()} cleanupFile: {e}')

async def tasks(path):
    try:
        #fileCleanup(fileList, path, max=10, delay=10)
        task1x = asyncio.create_task(fileCleanup(fileList, path, 5, 3))
        print(f'{mytime2()} task1x: {task1x}')
        print(f'{mytime2()} done @3 tasks...')
    except Exception as e:
        print(f'{mytime2()} tasks: {e}')

def mytime2():
    now = datetime.datetime.now()
    dnow = make_aware(now)
    utcnow = datetime.datetime.utcnow()
    unow = make_aware(utcnow)
    dt = (dnow - unow)
    print("UTC:  %s,   %s, %s-%s"%(utcnow, dt, unow, unow.tzinfo))
    print("Home: %s-%s,       %s-%s"%(now, now.tzinfo, dnow, dnow.tzinfo))
    return dnow
