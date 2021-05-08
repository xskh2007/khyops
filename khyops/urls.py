"""khyops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

    include('deploy.urls')
    include(('home.urls', 'home'), namespace='home')
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls import url
from deploy import views
from django_webssh import views as websshviews

urlpatterns = [
    path('',views.index,name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('deploy/', include(('deploy.urls', 'deploy'), namespace='deploy')),
    path('admin/', admin.site.urls),
    path('webssh/', websshviews.sshindex),
    url(r'^mywebssh/', include('mywebssh.urls')),


]
