from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addserver', views.addserver, name='addserver'),
    path('mytest', views.mytest, name='mytest'),
    path('deploy', views.deploy, name='deploy'),
    path('checkping', views.checkping, name='checkping'),
    path('checkport443', views.checkport443, name='checkport443'),
    path('checkport22', views.checkport22, name='checkport22'),

]