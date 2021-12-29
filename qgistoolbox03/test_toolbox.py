import datetime
import time
import sys
import os
import pprint
import asyncio
import pytest

try:
    #from . import toolbox as tbx
    from . import imagetools as imts
except Exception as e:
    print(f'testToolBox: {e}')

def getDir():
    proname = 'polygonsToolBox'
    dpath = os.getcwd()
    print(f'dpath: {dpath}')
    dp2 = dpath.split(proname)
    print(f'dp2: {dp2}')
    dp3 = dp2[0]+proname+'\/qgistoolbox03'
    print(f'dp3: {dp3}')
    dn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f'dn: {dn}')
    return dp3

def test_InfoSpikes():
    testing = 'Testing 123.................................................'
    print(f'{getDir()}\ntesting: {len(testing)}')
    assert len(testing) + 16 == 76
#    title = f'Polygons Spikes ToolBox: {tbx.account_02(tbx.ref01)}'
#    print(f'#{title}, Hello World!')
#    spikes01 = 'spiky-polygons.gpkg'
#    link = f'./info/{spikes01}'
#    print(f'{tbx.account_02(tbx.ref01)}, {link}')
#    infoTool = tbx.InfoSpikes(link)
#    infoTool.setWindowTitle(title)
#    infoTool.show()

def info_ImageTools(imageX):
    """
    Display image tapology.
    Press [esc] to quit.....
    If display is True.
    """
    display = False
    #display = True
    print(f'{imts.account_02(imts.ref01)}: Testing123....')
    #image01 = 'dblayers0054.png'
    link = f'{getDir()}\/info\/{imageX}'
    print(f'link: {link}')
    info = imts.imageInfo(link)
    color = imts.getColor(info['data'])
    dataList = imts.imageTool2(info['data'], color, display)
    print(f'dataList: {len(dataList)}')
    assert len(dataList) == 8

def test_image01():
    spikes01 = f'dblayers0054.png'
    info_ImageTools(spikes01)

def test_image02():
    spikes02 = f'dblayers005v1.png'
    info_ImageTools(spikes02)
    #assert 64 == 4

def test_image03():
    polygons03 = f'dblayers005v2.png'
    info_ImageTools(polygons03)
    #assert 65 == 5
