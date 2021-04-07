from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('index/', views.sshindex),
    path('myterm/', views.myterm),
    path('myterm2/', views.myterm2),
    path('myterm3/', views.myterm3),
    path('mywebsocket/', views.mywebsocket),
    path('echo/', views.echo),
]
