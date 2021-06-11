from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from django.shortcuts import render, redirect

from django.views import View

from django.db.models import Count

from JobforJunes.forms import VacancyEditForm

from JobforJunes.models import Vacancy







class MyVacanciesList(LoginRequiredMixin, View):
    def get(self, request):
        my_vacancies = Vacancy.objects.filter(company=request.user.company).annotate(appl_number=Count('applications'))
        if len(my_vacancies)>0:
            return render(request, 'vacancy_list.html', {'my_vacancies':my_vacancies})
        else:
            return render(request, 'vacancy_start.html')

class VacancyCreate(LoginRequiredMixin, View):
    def get(self, request):
        form=VacancyEditForm
        return render(request, 'vacancy_edit.html', {'form':form})

    def post(self, request):
        form=VacancyEditForm(request.POST)
        if form.is_valid():
            vacancy=form.save(commit=False)
            vacancy.company=request.user.company
            vacancy.save()
            return redirect('my_vacancies')

class VacancyEdit(LoginRequiredMixin, View):

    def get(self, request, pk_vac):
        my_vacancies=Vacancy.objects.get(id=pk_vac)
        form=VacancyEditForm(instance=my_vacancies)
        return render(request, 'vacancy_edit.html', {'form':form, 'vacancy':my_vacancies})

    def post(self, request,  pk_vac):
        my_vacancies = Vacancy.objects.get(id=pk_vac)
        form = VacancyEditForm(request.POST, instance=my_vacancies)
        if form.is_valid():
            form.save()
            messages.success(request, "Вакансия обновлена")
            print(messages.success)
            return redirect('vacancy_edit', pk_vac)
        messages.error(request, "Вакансия не обновлена, проверьте правильность данных")

