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

from ta_app.views.edit_SectionView import EditSectionView
from ta_app.views import removeCourseAssignment
from ta_app.views.deleteCourse import deleteCourse
from ta_app.views.Home import Home
from ta_app.views.courseList import courseList
from ta_app.views.accountList import accountList
from ta_app.views.accountInfoView import accountInfoView
from ta_app.views.createCourse import createCourse
from ta_app.views.accountCreation import accountCreation
from ta_app.views.loginView import login_view
from django.views.generic.base import RedirectView
from ta_app.views.SectionView import SectionView
from ta_app.views.deleteAccount import deleteAccount
from ta_app.views.deleteSection import deleteSection
from ta_app.views.accountAssignment import accountAssignment
from ta_app.views.courseSections import courseSections
from ta_app.views.removeCourseAssignment import removeCourseAssignment
from ta_app.views.editCourse import editCourse
from ta_app.views.removeSection import removeSection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home/',Home.as_view(), name="Home"),
    path('Home/courseList/',courseList.as_view(),name="courseList"),
    path('Home/createSection/',SectionView.as_view(),name="createSection"),
    path('Home/accountList/',accountList.as_view(),name="accountList"),
    path('Home/accountList/accountInfo/<int:pk>/',accountInfoView.as_view(),name="accountInfo"),
    path('Home/accountList/accountAssignment/<int:pk>/',accountAssignment.as_view(),name="accountAssignment"),
    path('Home/createCourse/',createCourse.as_view(), name="createCourse"),
    path('login/', login_view.as_view(), name='login'),
    path('Home/accountCreation/',accountCreation.as_view(), name='accountCreation'),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('Home/courseList/deleteCourse/<int:course_id>/', deleteCourse.as_view(), name='deleteCourse'),
    path('Home/courseList/editCourse/<int:course_pk>/', editCourse.as_view(), name='editCourse'),
    path('Home/accountList/deleteAccount/<int:pk>/', deleteAccount.as_view(), name='deleteAccount'),
    path('Home/courseList/courseSections/deleteSection/<int:pk>/', deleteSection.as_view(), name='deleteSection'),
    path('Home/courseList/courseSection/<int:course_pk>/', courseSections.as_view(), name='courseSections'),
    path('Home/courseList/accountAssignments/<int:user_id>/removeSection/<int:section_id>/', removeSection.as_view(), name='removeSection'),
    path('Home/editSection/<int:pk>/', EditSectionView.as_view(), name='editSection'),
    path('Home/courseList/courseSection/removeCourseAssignment/<int:user_pk>/<int:course_pk>/', removeCourseAssignment.as_view(), name='removeCourseAssignment')

]

