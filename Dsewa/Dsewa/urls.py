"""Dsewa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from hospital.views import *
from django.conf import settings

admin.site.site_header = "D-Sewa Administration"
admin.site.site_title = "D-Sewa Administration"
admin.site.index_title = "Welcome to D-Sewa"


urlpatterns = [
   # path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls,name="admin"),
    path('', homepage, name='homepage'),
    path('doc-registration/', doc_register, name='doc-registration'),
    path('createaccount/', createaccount, name='createaccount'),
    path('login/', loginpage, name='loginpage'),
    path('logout/', Logout, name='logout'),
    path('home/', Home, name='home'),
    path('profile/', profile, name='profile'),
    path("update-profile/", update_profile, name='update_profile'),
    path('makeappointments/', MakeAppointments, name='makeappointments'),
    #path('khaltirequest/', khaltirequest, name='khaltirequest'),
    path('viewappointments/', viewappointments, name='viewappointments'),

    #khalti urls

    path('initiate',initkhalti, name='initiate'),
    path("verify",verifykhalti, name='verify'),
]
