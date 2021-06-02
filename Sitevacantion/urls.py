"""Sitevacantion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from JobforJunes.views import Main_page, AllVacantions, Vacantions_by_speciality, \
    Company_view, Vacancy_view, My_Login, Register_User
from JobforJunes.views import c_handler404, c_handler500

handler400 = c_handler404
handler500 = c_handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main_page.as_view(), name='main'),
    path('vacancies/', AllVacantions.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty_pk>/', Vacantions_by_speciality.as_view(), name='vacancion_by_specialty'),
    path('companies/<int:pk_com>/', Company_view.as_view(), name='company'),
    path('vacancies/<int:pk_vac>/', Vacancy_view.as_view(), name='vacancy'),
    path('login/', My_Login.as_view(), name='login'),
    path('register/', Register_User.as_view(), name='register')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)