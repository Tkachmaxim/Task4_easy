from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View

from JobforJunes.forms import AplicationForm
from JobforJunes.models import Company, Vacancy, Specialty


class MainPage(View):

    def get(self, request):
        specialties = Specialty.objects.annotate(number_vacantion=Count('vacancies'))
        companies = Company.objects.annotate(number_companies=Count('companies'))
        return render(request, r'public\index.html', context={'specialties': specialties, 'companies': companies})


class Search(View):
    def get(self, request):
        query = request.GET.get('search')
        if query is None or query == '':
            messages.error(request, 'Ничего не найдено')
            return render(request, r'public\search.html')
        else:
            vacancies = Vacancy.objects.filter(Q(title__icontains=query) |
                                               Q(description__icontains=query) |
                                               Q(skills__icontains=query))
            if len(vacancies) == 0:
                messages.error(request, 'Ничего не найдено')
        return render(request, r'public\search.html', {'vacancies': vacancies})


class AllVacantions(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return render(request, r'public\vacancies.html', context={'vacancies': vacancies})


class VacantionsBySpeciality(View):
    def get(self, request, specialty_pk):
        get_object_or_404(Specialty, code=specialty_pk)
        vacancies = Vacancy.objects.filter(specialty__code=specialty_pk)
        return render(request, r'public\vacancies.html', context={'vacancies_t': vacancies})


class CompanyView(View):
    def get(self, request, pk_com):
        try:
            company = Company.objects.get(id=pk_com)
            vacancy = Vacancy.objects.filter(company=company)
        except ObjectDoesNotExist:
            raise Http404('Такой компании нет')

        return render(request, r'public\company.html', context={'companies': company, 'vacancy': vacancy})


class VacancyView(View):
    def get(self, request, pk_vac):
        try:
            vacancy = Vacancy.objects.get(id=pk_vac)
            form = AplicationForm()
        except ObjectDoesNotExist:
            raise Http404('Такой вакансии нет')

        return render(request, r'public\vacancy.html', context={'vacancy': vacancy, 'form': form})

    def post(self, request, pk_vac):
        form = AplicationForm(request.POST)
        vacancy = Vacancy.objects.get(id=pk_vac)
        if form.is_valid():
            aplication = form.save(commit=False)
            aplication.vacancy = vacancy
            aplication.user = User.objects.get(id=vacancy.company.owner_id)
            aplication.save()
            return redirect('sent', pk_vac)
        return render(request, r'public\vacancy', pk_vac)


class AplicationSend(View):

    def get(self, request, pk_vac):
        return render(request, r'public\sent.html', context={'pk_vac': pk_vac})


def c_handler404(request, exception):
    return HttpResponseNotFound('Информация отсутствует')


def c_handler500(request):
    return HttpResponseServerError('Ошибка сервера')
