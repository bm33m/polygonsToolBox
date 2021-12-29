from django.db import models
from django.conf import settings
import sqlite3
import random

# Create your models here.

def gisInfo():
    """Info relevent to GIS."""
    info = [{'info': 'Objects are Python’s abstraction for data.'
        ' All data in a Python program is represented by objects'
        ' or by relations between objects.'},
        {'info': 'Every object has an identity, a type and a value.'
        ' An object’s identity never changes once it has been created;'
        ' you may think of it as the object’s address in memory.'},
        {'info': 'The "is" operator compares the identity of two objects;'
        ' the id() function returns an integer representing its identity.'},
        {'info': 'An object’s type determines the operations that the object'
        ' supports (e.g., "does it have a length?") and also defines'
        ' the possible values for objects of that type.'
        ' The type() function returns an object’s type'
        ' (which is an object itself). Like its identity, an object’s type'
        ' is also unchangeable.'},
        {'info': 'The value of some objects can change. Objects whose value'
        ' can change are said to be mutable;'
        ' objects whose value is unchangeable once they are created'
        ' are called immutable.'},
        {'info': 'An object’s mutability is determined by its type;'
        ' for instance, numbers, strings and tuples are immutable,'
        ' while dictionaries and lists are mutable.'},
        #{},
        {'info': '"Layer" is a QgsVectorLayer instance'},
        {'info': 'Points, linestrings and polygons that represent'
        ' a spatial feature are commonly referred to as geometries.'
        ' In QGIS they are represented with the QgsGeometry class.'},
        {'info': 'Sometimes one geometry is actually a collection'
        ' of simple (single-part) geometries. Such a geometry is called'
        ' a multi-part geometry. If it contains just one type of'
        ' simple geometry, we call it multi-point, multi-linestring'
        ' or multipolygon. For example, a country consisting of'
        ' multiple islands can be represented as a multi-polygon.'},
        {'info': 'The coordinates of geometries can be in'
        ' any coordinate reference system (CRS).'
        ' When fetching features from a layer, associated geometries'
        ' will have coordinates in CRS of the layer.'},
        {'info': 'Description and specifications of all possible geometries'
        ' construction and relationships are available in the'
        ' OGC Simple Feature Access Standards for advanced details.'},
        {'info': 'The area of availability for vertex A is the subset of'
        ' graph vertexes that are accessible from vertex A and the cost of'
        ' the paths from A to these vertexes are not greater than'
        ' some values.'},
        {'info': 'The QGS format is an XML format for storing QGIS projects.'
        ' The QGZ format is a compressed (zip) archive containing a QGS file'
        ' and a QGD file. The QGD file is the associated sqlite database of'
        ' the qgis project that contain auxiliary data for the project.'
        ' If there are no auxiliary data, the QGD file will be empty.'
        ' A QGIS file contains everything that is needed for storing'
        ' a QGIS project, including: project title, project CRS,'
        ' the layer tree, etc.'},
        {'info': 'A Coordinate Reference System, or CRS,'
        ' is a method of associating numerical coordinates with a position'
        ' on the surface of the Earth.'},
        {'info': 'QGIS has support for approximately 7,000 known CRSs.'
        ' These standard CRSs are based on those defined by the'
        ' European Petroleum Search Group (EPSG) and the'
        ' Institut Geographique National de France (IGNF), and are made'
        ' available in QGIS through the underlying “Proj” projection library.'
        ' Commonly, these standard projections are identified through use'
        ' of an authority:code combination, where the authority is an'
        ' organisation name such as "EPSG" or "IGNF", and the code is'
        ' a unique number associated with a specific CRS. For instance,'
        ' the common WGS 84 latitude/longitude CRS is known by the'
        ' identifier EPSG:4326, and the web mapping standard CRS is'
        ' EPSG:3857.'},
        {'info': 'A mesh is an unstructured grid usually with temporal and'
        ' other components. The spatial component contains a collection of'
        ' vertices, edges and faces in 2D or 3D space.'},
        {'info': 'The GeoPackage (GPKG) format is platform-independent, and'
        ' is implemented as a SQLite database container, and can be used'
        ' to store both vector and raster data. The format was defined by'
        ' the Open Geospatial Consortium (OGC), and was published in 2014.'},
        {'info': 'GeoPackage can be used to store the following in'
        ' a SQLite database: vector features, tile matrix sets of imagery and'
        ' raster maps, attributes (non-spatial data), extensions, etc.'},
        #{},
        {'info': 'Images in a digital world can be transformed into numerical'
        ' matrices and other information describing the matrix itself.'
        ' We can also process, manipulate this digital information,'
        ' access pixel values and modify them.'},
        {'info': 'Cartography is the study and practice of making and'
        ' using maps. Combining science, aesthetics and technique,'
        ' cartography builds on the premise that reality can be modeled'
        ' in ways that communicate spatial information effectively.'
        ' It is the discipline dealing with the conception, production,'
        ' dissemination and study of maps.'},
        {'info': 'PyQGIS provides several options for creating a geometry:'
        ' From well-known text (WKT), from well-known binary (WKB),'
        ' from coordinates, etc. e.g.'
        ' Coordinates are given using QgsPoint class or QgsPointXY class.'
        ' The difference between these classes is that QgsPoint supports'
        ' M and Z dimensions.'
        ' A Polyline (Linestring) is represented by a list of points.'
        ' A Polygon is represented by a list of linear rings'
        ' (i.e. closed linestrings).'
        ' The first ring is the outer ring (boundary), optional subsequent'
        ' rings are holes in the polygon. QGIS will close the ring for you'
        ' so there is no need to duplicate the first point as the last.'},
        #{},
    ]
    return info

def gisTablesHome():
    """Return the database."""
    data = [{}]
    try:
        gpkg = settings.QGIS_PKG
        conn = sqlite3.connect(gpkg)
        cursor = conn.cursor()
        dbtables = ('table',)
        statement = "SELECT name FROM sqlite_master WHERE type=?"
        cursor.execute(statement, dbtables)
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        print("Gis tables: %s"%(e))
    #print("gisTables: %s"%(data))
    return data

def maps():
    """Return maps, graphs and images."""
    qmap = "qgishomeapp/assets/"
    temp = ["%s%s"%(qmap, "iotml200l.jpg"), "%s%s"%(qmap, "spikes200l.mp4"),
        "%s%s"%(qmap, "elevation.jpg"), "%s%s"%(qmap, "elevation2.jpg"),
        "%s%s"%(qmap, "graph.png"), "%s%s"%(qmap, "logicaldiagram.jpg"),
        "%s%s"%(qmap, "spatial.png"), "%s%s"%(qmap, "spikes.jpg"),
        "%s%s"%(qmap, "wgs84.jpg"), "%s%s"%(qmap, "wgs84map.jpg"),
        "%s%s"%(qmap, "dataframe.png"), "%s%s"%(qmap, "regions.png"),
        "%s%s"%(qmap, "pro3ml02l.png"), "%s%s"%(qmap, "wwwmap.jpg"),
        "%s%s"%(qmap, "map02.png"), "%s%s"%(qmap, "mapremove02.png"),
        "%s%s"%(qmap, "202112102152088.png"), "%s%s"%(qmap, "tmp76.png"),
        "%s%s"%(qmap, "toolbox.png"),
    ]
    return temp

def mapHome():
    """Return a random map or image and info."""
    map = maps()
    rand1 = random.randint(0, (len(map) - 1))
    info = gisInfo()
    rand2 = random.randint(0, (len(info) - 1))
    return [map[rand1], info[rand2]]
