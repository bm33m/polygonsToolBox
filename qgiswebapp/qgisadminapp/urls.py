from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('qgisdata', views.qgisdata, name='qgisdata'),
    path('dbtables', views.dbtables, name='dbtables'),
    path('qgis', views.qgis, name='qgis'),
]
