# polygonsToolBox
Polygons Tool Box.


![ptoolml22](https://user-images.githubusercontent.com/93065628/147403430-ffc8878a-26ed-4a37-b65f-31939251ea6f.png)
# polygonsToolBox
Polygons Tool Box.

Source code:
```
git clone https://github.com/bm33m/polygonsToolBox.git
```

This project is divided into 3 phases ( a.k.a. milestones).
Each phase could take up to 7 days or more.

Version 1 uses django to explore the content of the database package file gpkg and to perform spatial data analysis on spatial databases.

```
cd qgiswebapp
python manage.py runserver
```
visit:  http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

Version 2 uses opencv, numpy, pandas, scipy, matplotlib and networkx to analyze the data structures.

```
cd qgistoolbox01
python spikestool.py [-- input  image.png]
```

Version 3 uses qgis and pyqgis to implement the solution.
You can use the qgis python console to open and run:

```
qgistoolbox03/toolbox.py
```


![toolbox](https://user-images.githubusercontent.com/93065628/147651755-d8dbef1b-2b99-481b-a314-f072e1e07044.png)



Enjoy... :-)

So how does it work?

Our mission is to remove spikes from the image.
We are focusing on Polygons.

Any thing that doesnʼt form a polygon we remove it from the image, of course if and only if it is a spike.

We do this by checking if the image have spikes.


![logicaldiagram](https://user-images.githubusercontent.com/93065628/147652333-44431830-3dee-4f6b-a317-5a5116190dda.png)




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





We are done.
