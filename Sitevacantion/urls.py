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
    Company_view, Vacancy_view, Send_Request, CompanyStart, CompanyCreate, MyCompany, \
    MyVacanciesList, VacancyEdit, VacancyCreate, AplicationSend, Search, ResumeStart, \
    ResumeCreate
from JobforJunes.views import c_handler404, c_handler500

from users_app.views import MySignupView, MyLoginView, LogoutView

handler400 = c_handler404
handler500 = c_handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main_page.as_view(), name='main'),
    path('vacancies/', AllVacantions.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty_pk>/', Vacantions_by_speciality.as_view(), name='vacancion_by_specialty'),
    path('companies/<int:pk_com>/', Company_view.as_view(), name='company'),
    path('vacancies/<int:pk_vac>/', Vacancy_view.as_view(), name='vacancy'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', MySignupView.as_view(), name='Signup'),
    path('mycompany/letsstart/', CompanyStart.as_view(), name='company_start'),
    path('mycompany/create/', CompanyCreate.as_view(), name='create_new_company'),
    path('mycompany/', MyCompany.as_view(), name='my_company'),
    path('mycompany/vacancies/', MyVacanciesList.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/<int:pk_vac>/', VacancyEdit.as_view(), name='vacancy_edit'),
    path('mycompany/vacancies/create/', VacancyCreate.as_view(), name='vacancy_create'),
    path('vacancies/<int:pk_vac>/send/', AplicationSend.as_view(), name='sent'),
    path('search/', Search.as_view(), name='search',),
    path('myresume/letsstart/', ResumeStart.as_view(), name='resume_start'),
    path('myresume/create/', ResumeCreate.as_view(), name='resume_create')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)