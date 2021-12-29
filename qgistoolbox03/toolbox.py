"""
toolbox.py
Tools to remove spikes from the polygons.
Using Qgis, PyQt.
"""

import sys
import os
import datetime
import time
import argparse
import itertools as it
import math
from math import sqrt
import pprint

try:
    print('Step 01. Enter gpkgPath.')
    from qgis.core import (
        edit,
        Qgis,
        QgsCircle,
        QgsCoordinateReferenceSystem,
        QgsCoordinateTransform,
        QgsDataProvider,
        QgsExpression, QgsExpressionContext,
        QgsExpressionContextUtils,
        QgsFeature, QgsFeatureRequest, QgsField, QgsFields,
        QgsGeometry,
        QgsMessageLog,
        QgsPoint, QgsPointXY,
        QgsProject,
        QgsVectorLayer,
    )
    print('Step 02. Press Start Button.')
    from qgis.gui import (
        QgsMapCanvas,
        QgsMessageBar,
    )
    print('Step 03...')
    from qgis.PyQt.QtWidgets import (
        QDialog,
        QDialogButtonBox,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QSizePolicy,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
    from qgis.PyQt.QtCore import (
        Qt,
        QVariant,
    )
    print('Done....:-)')
except Exception as e:
    print(f'toolbox.py: {e}')


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

title = f'Polygons Spikes ToolBox: {account_02(ref01)}'
print(f'#{title}, Hello World!')
cwdpath = os.getcwd()
print(f'#{account_02(ref01)} cwdpath: \n{cwdpath}')

#
#InfoSpikes.
#Creates an object instance.
#

class InfoSpikes(QDialog):
    """
    Tool to remove spikes from the polygons.
    """
    #Path to your gpkg e.g.
    gpkgpath = 'C:/qgisprojects/qgistoolbox03/db'
    gpkg = f'{gpkgpath}/dblayers005.gpkg'
    spikesList = []
    pointsList = []
    vlayers = []
    newvlayers = []
    canvas01 = QgsMapCanvas()
    canvas02 = QgsMapCanvas()
    canvas03 = QgsMapCanvas()
    canvas04 = QgsMapCanvas()
    layout01 = QHBoxLayout()
    layout02 = QHBoxLayout()
    layout03 = QHBoxLayout()
    layout04 = QHBoxLayout()
    layout05 = QHBoxLayout()
    canvas05 = []
    rcanvas05 = []
    canvas06 = QgsMapCanvas()
    canvas07 = QgsMapCanvas()

    def __init__(self, args):
        QDialog.__init__(self)
        self.title = 'Spikes Tool Box.'
        self.links = args if args else self.gpkg
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonbox.accepted.connect(self.run)
        self.lblGpkg = QLabel(
            f'  {self.title}: {account_02(ref01)} \n  Enter gpkg path: ')
        self.txtGpkg = QLineEdit(self.links)
        self.lblAlphaDistance = QLabel('  max Distance Alpha(0.01 - 1000+)')
        self.spbAlphaDistance = QDoubleSpinBox()
        self.lblBetaAngle = QLabel('  min Angle Beta(0.01 - 360)')
        self.spbBetaAngle = QDoubleSpinBox()
        self.btnGpkg = QPushButton('Start')
        self.btnSpikes = QPushButton('spikesInfo')
        self.btnReset = QPushButton('Reset')
        self.btnHelp = QPushButton('Help')
        self.txtInfo = QTextEdit(self.title)
        self.addComponents_02()
        self.spbAlphaDistance.setMaximum(9999999999.99)
        self.spbAlphaDistance.setValue(98761.90)
        self.spbBetaAngle.setMaximum(360.00)
        self.spbBetaAngle.setValue(1.01)
        self.btnGpkg.clicked.connect(self.loadProjectLayers)
        self.btnSpikes.clicked.connect(self.spikesInfo)
        self.btnReset.clicked.connect(self.reset)
        self.btnHelp.clicked.connect(self.help)

    def addComponents_02(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        #addWidget
        self.layout().addWidget(self.bar)
        self.layout().addWidget(self.buttonbox)
        self.layout().addWidget(self.lblGpkg)
        self.layout().addWidget(self.txtGpkg)
        self.layout01.addWidget(self.lblAlphaDistance)
        self.layout01.addWidget(self.spbAlphaDistance)
        self.layout02.addWidget(self.lblBetaAngle)
        self.layout02.addWidget(self.spbBetaAngle)
        self.layout03.addWidget(self.btnGpkg)
        self.layout03.addWidget(self.btnSpikes)
        self.layout03.addWidget(self.btnReset)
        self.layout03.addWidget(self.btnHelp)
        #addLayout
        self.layout().addLayout(self.layout01)
        self.layout().addLayout(self.layout02)
        self.layout().addLayout(self.layout03)
        #addWidget
        self.layout().addWidget(self.txtInfo)
        #add canvas
        self.layout04.addWidget(self.canvas01)
        self.layout04.addWidget(self.canvas02)
        self.layout05.addWidget(self.canvas03)
        self.layout05.addWidget(self.canvas04)
        #addLayout
        self.layout().addLayout(self.layout04)
        self.layout().addLayout(self.layout05)
        #done.

    def loadProjectLayers(self):
        """
        Step 01, load the gpkg.
        From gpkg file.
        """
        gpkg = 'path/to/dbfile.gpkg'
        gpkgPath = self.txtGpkg.text()
        print(f'{account_02(ref01)}, gpkgpath: \n{gpkg}, \n{gpkgPath}')
        self.vlayers, subvLayersList, geometryList = loadLayers(gpkgPath)
        info = f'vlayer: \n{self.vlayers}, \n\
            subvLayersList: {len(subvLayersList)}, \n{subvLayersList}, \n\
            geometryList: {len(geometryList)}, \n{geometryList}'
        self.txtInfo.setText(f'{account_02(ref01)}, {info}')
        print(f'{account_02(ref01)}')
        if (len(geometryList) > 0):
            print(f'{account_02(ref01)} Done {len(geometryList)}')
            self.canvasTool(self.canvas01,
                self.vlayers, gpkgPath, False, True)
            self.canvasTool(self.canvas02,
                subvLayersList, gpkgPath, True, True)
            self.canvasTool(self.canvas06,
                self.vlayers, gpkgPath, False, True)
            self.canvas06.show()
            self.removeSpikes(geometryList, subvLayersList, gpkgPath)
        self.bar.pushMessage(f'#{account_02(ref01)}, {gpkgPath}',
            level=Qgis.Info)

    def removeSpikes(self, geometryList, subvLayersList, gpkgPath):
        """
        Step 02 Remove Spikes.
        """
        try:
            alphaDistance01 = self.spbAlphaDistance.value()
            betaAngle01 = self.spbBetaAngle.value()
            print(f'#{account_02(ref01)} Done...\n\
                geometryList: {len(geometryList)}, \n\
                AlphaDistance: {alphaDistance01}, \n\
                BetaAngle: {betaAngle01}')
            v1, v2, v3, v4, v5 = removeSpikes(
                geometryList, alphaDistance01, betaAngle01)
            pxyPointsXY, vindex, vpoints = v1, v2, v3
            geometryListSize, xyLists01 = v4, v5
            pxyPolygon02 = QgsGeometry.fromPolygonXY(pxyPointsXY)
            pxyPolygon01 = QgsGeometry.fromPolygonXY(xyLists01)
            pprint.pprint(pxyPolygon01)
            pprint.pprint(vindex)
            pprint.pprint(pxyPolygon02)
            gtype = pxyPolygon02.type()
            garea = pxyPolygon02.area()
            glength = pxyPolygon02.length()
            print(f'gtype: {gtype}, area: {garea}, length: {glength}')
            def showCanvas(qcolor0X, polygon0X, canvas0X, layer0X, gpkg0X,
                vlist=False, qwidth0X=1):
                self.canvasTool(canvas0X, layer0X, gpkg0X, vlist)
                r01 = QgsRubberBand(canvas0X, True)
                r01.setToGeometry(polygon0X, None)
                r01.setColor(qcolor0X)
                r01.setWidth(qwidth0X)
                return r01
            qcolor01 = QColor(255, 45, 234)
            rc03 = showCanvas(qcolor01, pxyPolygon01,
                self.canvas03, subvLayersList[0:1], gpkgPath, True)
            pprint.pprint(pxyPointsXY)
            qcolor02 = QColor(25, 245, 134)
            rc04 = showCanvas(qcolor02, pxyPolygon02, self.canvas04,
                subvLayersList[0:1], gpkgPath, True)
            print(f'#{account_02(ref01)} show canvas ..........')
            #self.canvas05 = iface.mapCanvas()
            #self.rcanvas05 = showCanvas(qcolor02, pxyPolygon02,
            #    self.canvas05, subvLayersList[0:1], gpkgPath, True)
            #gpkgPath = self.txtGpkg.text()
            print(f'pxyPointsXY: {len(pxyPointsXY)}, \n\
                vindex: {len(vindex)}, \nvpoints: {vpoints}, \n\
                geometryListSize: {geometryListSize}')
            self.addpLayer(pxyPolygon02, self.vlayers, gpkgPath)
            self.spikesList = pxyPolygon01
            self.pointsList = pxyPolygon02
        except Exception as e:
            print(f'{account_02(ref01)} removeSpikes: {e}')
        print(f'{account_02(ref01)}, removeSpikes: Done....')

    def addpLayer(self, pxyPolygon02, layer, gpkg):
        """
        Step 03 add new Polygons.
        """
        try:
            print(f'{account_02(ref01)}, addpLayer...')
            valayer01 = f'vlayers{account_02(ref01)}.gpkg'
            assets01 = f'{gpkg.split(".gpkg")[0]}{valayer01}'
            print(f'save...{assets01}')
            def addLayers():
                try:
                    fields = QgsFields()
                    fields.append(QgsField('info01', QVariant.Int))
                    fields.append(QgsField('info02', QVariant.String))
                    #
                    crs = QgsProject.instance().crs()
                    transformContext = QgsProject.instance(
                        ).transformContext()
                    saveOptions = QgsVectorFileWriter.SaveVectorOptions()
                    #
                    writer = QgsVectorFileWriter.create(
                        assets01,
                        fields,
                        QgsWkbTypes.Polygon,
                        crs,
                        transformContext,
                        saveOptions
                    )
                    #
                    if writer.hasError() != QgsVectorFileWriter.NoError:
                        print(f'{account_02(ref01)} \
                            addLayers: {writer.errorMessage()}')
                    #
                    feat = QgsFeature()
                    feat.setGeometry(pxyPolygon02)
                    feat.setAttributes([1, 'polygons2022'])
                    writer.addFeature(feat)
                    del writer
                except Exception as e:
                    print(f'{account_02(ref01)}, addLayers: {e}')
            try:
                addLayers()
                self.newvlayers, subvLayersList, geometryList = loadLayers(
                    assets01)
                if (len(geometryList) > 0):
                    print(f'{account_02(ref01)} Done {len(geometryList)}')
                    self.canvasTool(self.canvas07,
                        self.newvlayers, assets01, False, True)
                    self.canvas07.show()
            except Exception as e:
                print(f'{account_02(ref01)}, addpLayers: {e}')
            for f in self.newvlayers.getFeatures():
                print(f)
        except Exception as e:
            print(f'{account_02(ref01)}, addpLayer: {e}')

    def help(self):
        """
        Step 04 help.
        """
        try:
            help01 = f'{account_02(ref01)}, help...'
            h02 = 'Step 01. Enter gpkgPath.'
            h03 = 'Step 02. Press Start Button.'
            h04 = 'Step 03...adjust the maxDistance and \
                minAngle Settings, \nand do step02...'
            h05 = f'{help01} \n{h02} \n{h03}, \n{h04}'
            print(h05)
            self.txtInfo.setText(h05)
        except Exception as e:
            print(f'{account_02(ref01)}, save: {e}')

    def canvasTool(self, canvasXY, vlayers, gpkg, vlist=False, snap=False):
        try:
            i = [0]
            def addvLayer(vlayer):
                print(f'{i[0]}, {account_02(ref01)} \n{vlayer}')
                if not vlayer.isValid():
                   print('vLayer error...')
                QgsProject.instance().addMapLayer(vlayer)
                canvasXY.setExtent(vlayer.extent())
                i[0] += 1
            if (vlist):
                for subLayer in vlayers[::-1]:
                    addvLayer(subLayer)
                canvasXY.setLayers(vlayers[::-1])
            else:
                addvLayer(vlayers)
                canvasXY.setLayers([vlayers])
            if (snap):
                snapShot(gpkg, vlayers, vlist)
        except Exception as e:
            print(f'canvasTool: {e}')

    def spikesInfo(self):
        try:
            print(f'{account_02(ref01)} geom: spikesInfo...')
            print(f'geom SpikesList: {self.spikesList.length()}, \n\
                pointsList: {self.pointsList.length()}')
            pprint.pprint(self.spikesList)
            print('\n### ### ### ### ### #\n')
            pprint.pprint(self.pointsList)
            info1 = f'info1: {account_02(ref01)}, \n\
                Spikes: {self.spikesList.length()} \n{self.spikesList}'
            info2 = f'info2: {account_02(ref01)}, \n\
                Points: {self.pointsList.length()} \n{self.pointsList}'
            info00 = '#'
            d = QgsDistanceArea()
            d.setEllipsoid('WGS84')
            def info(geom, ginfo):
                gtype = geom.type()
                garea = geom.area()
                glength = geom.length()
                gaream2 = d.measureArea(geom)
                gperimeterm = d.measurePerimeter(geom)
                info0X = f'{ginfo}: {account_02(ref01)},\n\
                    gtype: {gtype}, \nArea: {garea}, \nLength: {glength}, \n\
                    gaream2: {gaream2},  \ngperimeterm: {gperimeterm}'
                print(info0X)
                return info0X
            info3 = info(self.spikesList, 'info3')
            info4 = info(self.pointsList, 'info4')
            info5 = [layer.name() for layer in QgsProject.instance(
                ).mapLayers().values()]
            print(f'layers: {len(info5)}, \n{info5}')
            self.txtInfo.setText(
                f'{info1} \n{info2} \n{info3} \n{info4}, \n{info5}')
        except Exception as e:
            print(f'{account_02(ref01)}, {e}')

    def reset(self):
        try:
            print(f'#{account_02(ref01)} \
                reset SpikesList: {self.spikesList}, \n\
                PointsList: {self.pointsList}')
            self.spikesList = []
            self.pointsList = []
            self.vlayers = []
            self.title = (f'SpikesToolBox: {account_02(ref01)}')
            self.txtInfo.setText(self.title)
            QgsProject.instance().clear()
            #self.canvas05.scene().removeItem(self.rcanvas05)
        except Exception as e:
            print(f'{account_02(ref01)} reset: {e}')

    def run(self):
        pref = account_02(ref01)
        toggleLayers(pref)
        self.bar.pushMessage(f'#{pref} Hello', "World", level=Qgis.Info)

#
#Open the gpkg.
#Process the polygons
#

def loadLayers(fileName=None):
    """
    Open the gpkg.
    return vlayer, subvLayersList, geometryList
    """
    vlayer = ''
    subvLayersList = []
    geometryList = []
    try:
        #path to your gpkg e.g.
        gpkgpath = 'C:/qgisprojects/qgistoolbox03/db'
        gpkg = f'{gpkgpath}/dblayers005.gpkg'
        fileName = fileName if fileName else gpkg
        vlayer = QgsVectorLayer(fileName, f'spikes{account_02(ref01)}', "ogr")
        subLayers = vlayer.dataProvider().subLayers()
        project01 = QgsProject.instance()
        d = QgsDistanceArea()
        d.setEllipsoid('WGS84')
        print(f'file: {fileName}')
        for subLayer in subLayers[::-1]:
            name = subLayer.split(QgsDataProvider.SUBLAYER_SEPARATOR)[1]
            uri = "%s|layername=%s" % (fileName, name,)
            # Create layer
            sub_vlayer = QgsVectorLayer(uri, name, 'ogr')
            # Add layer to map
            project01.addMapLayer(sub_vlayer)
            lyrs = qgis.utils.iface.activeLayer()
            print('layer id: ', lyrs.id())
            features = lyrs.getFeatures()
            for ft in features:
                print('feature id: ', ft.id())
                geom = ft.geometry()
                gtype = geom.type()
                garea = geom.area()
                glength = geom.length()
                gaream2 = d.measureArea(geom)
                gperimeterm = d.measurePerimeter(geom)
                gareakm2 = d.convertAreaMeasurement(gaream2,
                    QgsUnitTypes.AreaSquareKilometers)
                print(f'gtype: {gtype}, \ngarea: {garea}, \n\
                    glength: {glength}')
                print(f'gaream2: {gaream2}, \ngperimeterm: {gperimeterm}')
                print(f'gareakm2: {gareakm2}, \ngeom:')
                pprint.pprint(geom)
                geometryList.append(geom)
            subvLayersList.append(sub_vlayer)
        return vlayer, subvLayersList, geometryList
    except Exception as e:
        print(f'loadLayers: {e}')
    print(f'{account_02(ref01)} geometryList: {len(geometryList)}')
    return vlayer, subvLayersList, geometryList

def removeSpikes(geometryList, alphaDistance01=1000.00, betaAngle01=1.00):
    pxyPointsXY = []
    vpoints = 0
    i = 0
    vindex = []
    xySpikesLists = []
    try:
        glist = len(geometryList)
        print(f'{account_02(ref01)} removeSpikes....{glist}')
        #geom = geometryList[glist-1]
        maxAngle = 360.00
        midAngle = maxAngle // 2
        cutoffAngle = (betaAngle01 + 0.10) - (
            betaAngle01 * 1.00) + (betaAngle01 * 1.00)
        maxDistance = alphaDistance01 * 1.00
        for geom in geometryList:
            gtype = geom.type()
            garea = geom.area()
            glength = geom.length()
            d = QgsDistanceArea()
            d.setEllipsoid('WGS84')
            gaream2 = d.measureArea(geom)
            gperimeterm = d.measurePerimeter(geom)
            gareakm2 = d.convertAreaMeasurement(gaream2,
                QgsUnitTypes.AreaSquareKilometers)
            #print(f'geometryList[{i}], \ngtype: {gtype}, \n\
            #    garea: {garea}, \nglength: {glength}')
            #print(f'gaream2: {gaream2}, \ngperimeterm: {gperimeterm}')
            #print(f'gareakm2: {gareakm2}, \ngeometryList[{i}]:')
            try:
                xyGeom = geom.asPolygon()
                pprint.pprint(xyGeom)
                p0 = QgsPointXY(0.0, 0.0)
                j = 0
                j01 = len(xyGeom)
                print(f'j01: {j01}')
                for xy in xyGeom:
                    xyLists02 = []
                    xyLists01 = []
                    #print(f'geometry{i}{j}: ')
                    #pprint.pprint(xy)
                    v1 = 0
                    #p0 = xy[v1]
                    x01 = len(xy)
                    v01 = len(xy)
                    pv = [xyp for xyp in xy]
                    p1 = pv[v1]
                    print(f'pv{i}{j}{v1}, pv[{v1}]: {p1}')
                    pprint.pprint(pv)
                    print(f'v01: {v01}')
                    print(f'x01: {x01}')
                    pprint.pprint(xy)
                    for p in xy:
                        v0, v2 = geom.adjacentVertices(v1)
                        p0 = pv[v0]
                        p1 = pv[v1]
                        p2 = pv[v2]
                        pAdj = (p0, p1, p2)
                        dxy = d.measureLine(p1, p)
                        print(f'geom{i}{j}{v1}, \n\
                            d.measureLine: ({p1}, {p}), \ndxy: {dxy}')
                        print(f'adjacentVertices({v1}), \n\
                            ({v0}, {v1} ,{v2}): \n{pAdj}')
                        adjacentVDistance0 = d.measureLine(p1, p0)
                        adjacentVDistance2 = d.measureLine(p1, p2)
                        azimut01 = p0.azimuth(p1)
                        azimut02 = p2.azimuth(p1)
                        qpAngle = abs(azimut01 - azimut02)%maxAngle
                        angleW = (maxAngle - cutoffAngle)
                        lineAngle = angleW if qpAngle > midAngle else qpAngle
                        print(f'#{account_02(ref01)}')
                        print(f'vertice{v1}, \ndxy: {dxy}')
                        print(f'azimut01: {azimut01}, \nazimut02: {azimut02}')
                        print(f'qpAngle: {qpAngle}, \nlineAngle: {lineAngle}')
                        print(f'adjacentVDistance0: {adjacentVDistance0}')
                        print(f'adjacentVDistance2: {adjacentVDistance2}')
                        dv0 = (adjacentVDistance0 <= maxDistance)
                        dv2 = (adjacentVDistance2 <= maxDistance)
                        distanceXY = (dv0 or dv2)
                        angleW = (cutoffAngle <= lineAngle)
                        if (angleW and distanceXY):
                            xyLists02.append(p1)
                            vindex.append((i, j, v1))
                            print(f'#{v1} OK................')
                        else:
                            print(f'#\n#{v1} ...cutoff.....#{lineAngle}\n#')
                        xyLists01.append(p1)
                        vpoints += 1
                        v1 += 1
                    j += 1
                    xlist = len(xyLists02)
                    print(xyLists02[0].x(), xyLists02[xlist-1].x())
                    print(xyLists02[0].y(), xyLists02[xlist-1].y())
                    if (xlist > 0):
                        pX0 = (xyLists02[0].x() == xyLists02[xlist-1].x())
                        pY0 = (xyLists02[0].y() == xyLists02[xlist-1].y())
                        if(pX0 and pY0):
                            print(f'#1 xyLists02[0]: {xyLists02[0]} \n\
                                len: {xlist}')
                            pprint.pprint(xyLists02)
                            xyLists2 = [xyp0 for xyp0 in xyLists02[:xlist-1]]
                            xlist2 = len(xyLists2)
                            pprint.pprint(xyLists2)
                            print(f'#2 xyLists2[{xlist2-1}]: \
                                {xyLists2[xlist2-1]}, \nlen2: {xlist2}, \n\
                                len1: {xlist}')
                            pxyPointsXY.append(xyLists2)
                        else:
                            pxyPointsXY.append(xyLists02)
                    xySpikesLists.append(xyLists01)
            except Exception as e:
                print(f'geom{i}, {account_02(ref01)} removeSpikes: {e}')
            i += 1
    except Exception as e:
        print(f'{account_02(ref01)} removeSpikes: {e}')
    return pxyPointsXY, vindex, vpoints, i, xySpikesLists

def save(layer, gpkg):
    try:
        print('save...')
        assets01 = f'{gpkg.split(".gpkg")[0]}{account_02(ref01)}.gpkg'
        print(f'save...{assets01}')
        saveOptions = QgsVectorFileWriter.SaveVectorOptions()
        transformContext = QgsProject.instance().transformContext()
        error = QgsVectorFileWriter.writeAsVectorFormatV2(layer,
            assets01, transformContext, saveOptions)
        if (error[0]) == QgsVectorFileWriter.NoError:
            print(f'{account_02(ref01)} Done...{assets01}')
        else:
            print(f'{account_02(ref01)}, {error}')
    except Exception as e:
        print(f'{account_02(ref01)} Save: {e}')

def snapShot(gpkg, vlayers, vlist=False):
    try:
        assets01 = f'{gpkg.split(".gpkg")[0]}{account_02(ref01)}.png'
        print(f'snapShot...{assets01}')
        settings = QgsMapSettings()
        i = [0]
        def addvLayer(vlayer):
            print(f'{i[0]}, {account_02(ref01)} \n{vlayer}')
            if not vlayer.isValid():
               print('vLayer error...')
            QgsProject.instance().addMapLayer(vlayer)
            settings.setExtent(vlayer.extent())
            i[0] += 1
        if (vlist):
            for subLayer in vlayers[::-1]:
                addvLayer(subLayer)
            settings.setLayers(vlayers[::-1])
        else:
            addvLayer(vlayers)
            settings.setLayers([vlayers])
        settings.setBackgroundColor(QColor(20, 50, 255))
        settings.setOutputSize(QSize(940, 640))
        render = QgsMapRendererParallelJob(settings)
        def finished():
            img = render.renderedImage()
            img.save(assets01, 'png')
        render.finished.connect(finished)
        render.start()
    except Exception as e:
        print(f'{account_02(ref01)} snapShot: {e}')

def toggleLayers(pref):
    try:
        project01 = QgsProject.instance()
        root01 = project01.layerTreeRoot()
        layer01 = iface.activeLayer()
        node01 = root01.findLayer(layer01.id())
        newState01 = Qt.Checked if node01.isVisible(
            ) == Qt.Unchecked else Qt.Unchecked
        node01.setItemVisibilityChecked(newState01)
        print(f'{pref} toggle: \n{layer01.id()}, {newState01}')
    except Exception as e:
        print(f'toggleLayers {pref}:, {e}')

#
#main
#
def main():
    try:
        parser = argparse.ArgumentParser(
            description='Tool to remove spikes from the polygons.')
        link = 'C:/qgisprojects/qgistoolbox02/db/spiky-polygons.gpkg'
        parser.add_argument(
            '--input', help='Path to input gpkg.', default=link)
        args = parser.parse_args()
        infoTool = InfoSpikes(args)
        infoTool.setWindowTitle(title)
        infoTool.show()
    except Exception as e:
        print(f'{account_02(ref01)} main: {e}')

if __name__ == '__main__':
    print(f'{account_02(ref01)}, {__name__}')
    main()
else:
    try:
        print(f'{account_02(ref01)}, Enter gpkg path.')
        #args1 = str(input('#Enter the gpkgpath: '))
        #args2 = 'C:/qgisprojects/qgistoolbox03/db/dblayers005.gpkg'
        args = 'C:/qgisprojects/qgistoolbox03/db/spiky-polygons.gpkg'
        args = None
        infoTool = InfoSpikes(args)
        infoTool.setWindowTitle(title)
        infoTool.show()
        print(f'{account_02(ref01)}, {args}')
    except Exception as e:
        print(f'toolbox: {e}')
#
#We are Done...:-)
#
