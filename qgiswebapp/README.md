#polygonsToolBox

Steps by steps to remove spikes from the polygons:

Our mission is to remove spikes from the image.
We are focusing on Polygons.

Any thing that doesnʼt form a polygon we remove it from the image, of course if and only if it is a spike.

We do this by checking if the image have spikes.

A Polygon is represented by a list of linear rings (i.e. closed linestrings).
The first ring is the outer ring (boundary), optional subsequent rings are holes in the polygon.
QGIS will close the ring for you so there is no need to duplicate the first point as the last.
So if it is not a closed linestring or linear ring or polygon then it is a good candidate for a spike.

The first shall be the last and the last shall be the first.
In a closed linestrings system the first or starting point is the same as the last or end point.
In an open linestrings system the opposite is true.
The first point and the last point are outliers or noise or not the same.

On the other hand what if the tricky polygon that looks like a line is a spike?
As far as the computer system is concerned it is still a polygon if the linestring is closed.
So, what do we do?
Maths, algebra can come to our rescue!
We check the linestrings of each and every vector in the polygon i.e. vectorLayers.
We focus on the distance between the two adjacent points, and the angle between them.
If the distance is greater than the maxDistance and the angle is less than the minLineAngle we exclude the point.

We are done :)

This project is divided into 3 versions.

Version 3 uses qgis and pyqgis to implement the solution.

Version 2 uses opencv, numpy, pandas, scipy, matplotlib and networkx to analyze the data structures.

Version 1 uses django to explore the content of the database package file gpkg and to perform spatial data analysis on spatial databases.

Source code:
'''
git clone https://github.com/bm33m/polygonsToolBox.git
'''


Enjoy.
