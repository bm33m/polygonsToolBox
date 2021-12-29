import datetime
import time
import sys
import os
import pprint
import asyncio
import pytest
from . import spikestool as st

def getDir():
    proname = 'polygonsToolBox'
    dpath = os.getcwd()
    print(f'dpath: {dpath}')
    dp2 = dpath.split(proname)
    print(f'dp2: {dp2}')
    dp3 = dp2[0]+proname+'/qgistoolbox01'
    print(f'dp3: {dp3}')
    dn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f'dn: {dn}')
    return dp3

spikes01 = 'tmp220.png'
link = f'{getDir()}/data01/{spikes01}'
app = st.QgistoolApp(link)

def test_closedOpenExperiment():
   lineStrings = st.closedOpenExperiment(app.lineStrings())
   #assert lineStrings == 1
   #assert lineStrings == 0
   assert lineStrings == True
   #assert lineStrings == False

def test_imageInfo():
    #'shape': (298, 793, 3),
    #'size': 708942,
    #'dtype': dtype('uint8')
    image = st.imageInfo(link)
    print(f'image: {image}')
    sizeX = image['shape'][0] * image['shape'][1] * image['shape'][2]
    assert image['size'] == sizeX

def test_imageTool2():
    """
    Test image tapology.
    Press [esc] to quit.....
    If display is True.
    """
    display = False
    #display = True
    p1 = 3
    p2 = 3
    #color0X = (25, 70, 250)
    opening = app.imageOpening(p1, p2)
    #closing = app.imageClosing(p1, p2)
    y0X, x1X, c2X = opening.shape
    colorX = opening[y0X//2, x1X//2]
    tool2 = st.imageTool2(opening, colorX, display)
    print(f'tool2: {tool2[0]}')
    y0, x1, c2 = tool2[0].shape
    assert tool2[0].size == y0 * x1 * c2

def test_imageTool():
    """
    Test image tapology.
    Press [esc] to quit.....
    If display is True.
    """
    display = False
    #display = True
    async def spikes():
        tool = await app.imageTool(display)
        return tool
    tool = asyncio.run(spikes())
    pprint.pprint(tool[2])
    y0, x1, c2 = tool[2].shape
    assert tool[2].size == y0 * x1 * c2

def test_removeSpikes():
    """
    Test image tapology.
    Press [esc] to quit.....
    If display is True.
    """
    display = False
    #display = True
    p1 = 3
    p2 = 3
    alpha = 3
    beta = 3
    opening = app.imageOpening(p1, p2)
    closing = app.imageClosing(p1, p2)
    y0X, x1X, c2X = opening.shape
    #colorX = opening[y0X//2, x1X//2]
    colorX = st.getColor(opening)
    tool2 = st.imageTool2(opening, colorX, display)
    print(f'colorX: {colorX}')
    async def spikes():
        tool = await st.removeSpikes(
            closing, tool2, y0X, x1X, c2X, alpha, beta, display)
        return tool
    tool = asyncio.run(spikes())
    pprint.pprint(tool[3])
    y0, x1, c2 = tool[3].shape
    assert tool[3].size == y0 * x1 * c2
