from django.http import HttpResponseNotFound, HttpResponseServerError

from django.db.models import Count

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

from django.views import View

from JobforJunes.models import Company, Vacancy, Specialty



class Main_page(View):
    def get(self, request):
        specialties=Specialty.objects.annotate(number_vacantion=Count('vacancies'))
        companies = Company.objects.annotate(number_companies=Count('companies'))
        return render(request, 'index.html', context={'all':{'specialties':specialties, 'companies':companies}})


class AllVacantions(View):
    def get(self,request):
        vacancies_t = Vacancy.objects.all()
        return render(request, 'vacancies.html', context={'vacancies_t':vacancies_t})


class Vacantions_by_speciality(View):
    def get(self, request, specialty_pk):
        try:
            vacancies = Vacancy.objects.filter(specialty__code=specialty_pk)
        except:
            return HttpResponseNotFound('Инофрмация не найдна')
        return render(request, 'vacancies.html', context={'vacancies_t':vacancies})


class Company_view(View):
    def get(self, request, pk_com):
        try:
            company=Company.objects.get(id=pk_com)
            vacancy=Vacancy.objects.filter(company=company)
        except:
           return HttpResponseNotFound('Инофрмация не найдна')

        return render(request, 'company.html', context={'companies':company, 'vacancy':vacancy})


class Vacancy_view(View):
    def get(self, request, pk_vac):
        try:
            vacancy = Vacancy.objects.get(id=pk_vac)
        except:
            return HttpResponseNotFound('Инофрмация не найдна')

        return render(request, 'vacancy.html', context={'vacancy':vacancy})

def c_handler404(request, exception):
    return HttpResponseNotFound('Информация отсутствует')

def c_handler500(request):
    return HttpResponseServerError('Ошибка сервера')