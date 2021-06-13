import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from JobforJunes.forms import VacancyEditForm
from JobforJunes.models import Vacancy, Application


class MyVacanciesList(LoginRequiredMixin, View):
    def get(self, request):
        my_vacancies = Vacancy.objects.filter(company=request.user.company).annotate(appl_number=Count('applications'))
        if len(my_vacancies) > 0:
            return render(request, r'my_vacancies/vacancy_list.html', {'my_vacancies': my_vacancies})
        else:
            return render(request, r'my_vacancies/vacancy_start.html')


class VacancyCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = VacancyEditForm
        return render(request, r'my_vacancies/vacancy_edit.html', {'form': form})

    def post(self, request):
        form = VacancyEditForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = request.user.company
            vacancy.published_at = datetime.datetime.today()
            # changing comma on dot
            change_comma = (vacancy.skills).replace(',', '•')
            vacancy.skills = change_comma
            vacancy.save()
            return redirect('my_vacancies')


class VacancyEdit(LoginRequiredMixin, View):

    def get(self, request, pk_vac):
        my_vacancies = get_object_or_404(Vacancy, id=pk_vac, company=request.user.company)
        apllacations = Application.objects.filter(vacancy=my_vacancies)
        form = VacancyEditForm(instance=my_vacancies)
        return render(request, r'my_vacancies/vacancy_edit.html',
                      {'form': form, 'vacancy': my_vacancies, 'applications': apllacations})

    def post(self, request, pk_vac):
        my_vacancies = get_object_or_404(Vacancy, id=pk_vac, company=request.user.company)
        form = VacancyEditForm(request.POST, instance=my_vacancies)
        apllacations = Application.objects.filter(vacancy=my_vacancies)
        if form.is_valid():
            form.save()
            messages.success(request, "Вакансия обновлена")
            return redirect('vacancy_edit', pk_vac)
        messages.error(request, "Вакансия не обновлена, проверьте правильность данных")
        return render(request, r'my_vacancies/vacancy_edit.html',
                      {'form': form, 'vacancy': my_vacancies, 'applications': apllacations})
