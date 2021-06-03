from django.db.models import Count

from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponseRedirect

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect

from django.views import View

from django.core.exceptions import ObjectDoesNotExist

from JobforJunes.models import Company, Vacancy, Specialty

from JobforJunes.forms import Register_User_Form




class My_Login(LoginView):

    template_name = 'login.html'


class Register_User(View):

    def get(self, request):
        return render(request, 'register.html', context={'form':Register_User_Form})

    def post(self, request):
        form=Register_User_Form(request.POST)
        print(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.cleaned_data.save()
            return redirect('login')
        return render(request, 'register.html', context={'form':form})





class Main_page(View):
    def get(self, request):
        specialties = Specialty.objects.annotate(number_vacantion=Count('vacancies'))
        companies = Company.objects.annotate(number_companies=Count('companies'))
        return render(request, 'index.html', context={'all': {'specialties': specialties, 'companies': companies}})


class AllVacantions(View):
    def get(self, request):
        vacancies_t = Vacancy.objects.all()
        return render(request, 'vacancies.html', context={'vacancies_t': vacancies_t})


class Vacantions_by_speciality(View):
    def get(self, request, specialty_pk):
        vacancies = Vacancy.objects.filter(specialty__code=specialty_pk)
        return render(request, 'vacancies.html', context={'vacancies_t': vacancies})


class Company_view(View):
    def get(self, request, pk_com):
        try:
            company = Company.objects.get(id=pk_com)
            vacancy = Vacancy.objects.filter(company=company)
        except ObjectDoesNotExist:
            raise Http404('Такой компании нет')

        return render(request, 'company.html', context={'companies': company, 'vacancy': vacancy})


class Vacancy_view(View):
    def get(self, request, pk_vac):
        try:
            vacancy = Vacancy.objects.get(id=pk_vac)
        except ObjectDoesNotExist:
            raise Http404('Такой вакансии нет')

        return render(request, 'vacancy.html', context={'vacancy': vacancy})


def c_handler404(request, exception):
    return HttpResponseNotFound('Информация отсутствует')


def c_handler500(request):
    return HttpResponseServerError('Ошибка сервера')

class Send_Request(View):
    def get(self, request, pk_vac):
        try:
            vacancy = Vacancy.objects.get(id=pk_vac)
        except ObjectDoesNotExist:
            raise Http404('Такой вакансии нет')

        return render(request, 'sent.html', context={'vacancy': vacancy})
