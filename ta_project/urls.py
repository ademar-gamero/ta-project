"""
URL configuration for ta_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ta_app.views.Home import Home
from ta_app.views.courseList import courseList
from ta_app.views.accountList import accountList
from ta_app.views.accountView import accountView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home/',Home.as_view()),
    path('Home/courseList/',courseList.as_view(),name="courseList"),
    path('Home/accountList/',accountList.as_view(),name="accountList"),
    path('Home/accountList/<int:pk>/',accountView.as_view(),name="accountDetails")
]
