from django.db import models
import os
import asyncio
from filecmp import dircmp
from . import spikestool as st

mpath = os.getcwd()
print(f'mpath: {mpath}')
mp2 = mpath.split('qgiswebapp')
print(f'mp2: {mp2}')
mp3 = mp2[0]+'qgistoolbox01'
print(f'mp3: {mp3}')
dn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f'dn: {dn}')

async def tasks():
    task1x = asyncio.create_task(
        st.tempFiles(dircmp(st.tempDir()[0], st.tempDir()[2]))
    )
    print('task1x: ', task1x)

asyncio.run(tasks())
