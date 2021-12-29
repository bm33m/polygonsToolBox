from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('xmlinfo', views.xmlinfo, name='xmlinfo'),
    path('htmlinfo', views.htmlinfo, name='htmlinfo'),
]
