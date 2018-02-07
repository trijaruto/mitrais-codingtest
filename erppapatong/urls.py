"""erppapatong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #USER
    url(r'^', include('erpp_main.urls')),
    #url(r'^', include('erpg_auth.urls')),
    #url(r'^', include('erpg_dasboard.urls')),
    #ADMIN
    #url(r'^erpg/admin/', include('_erpg_mainadmin.urls')),
    #url(r'^erpg/admin/', include('_erpg_authadmin.urls')),
    #url(r'^erpg/admin/', include('_erpg_dasboardadmin.urls')),
    #API
    #url(r'^api/', include('erpg_api.urls')),
]
