from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addserver', views.addserver, name='addserver'),
    path('mytest', views.mytest, name='mytest'),
    path('deploy', views.deploy, name='deploy'),
]