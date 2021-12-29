from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imagefilter', views.imagefilter, name='imagefilter'),
    path('qgisinfo', views.qgisinfo, name='qgisinfo'),
]
