from django.db.models import Count, Q

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponseRedirect

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect

from django.views import View

from django.core.exceptions import ObjectDoesNotExist

from JobforJunes.models import Company, Vacancy, Specialty, Resume

from JobforJunes.forms import MyCompanyForm, VacancyEditForm, AplicationForm, ResumeForm


class ResumeStart(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        try:
            resume=Resume.objects.get(user=request.user)
            form=ResumeForm(instance=resume)
        except ObjectDoesNotExist:
            return render(request, 'resume_create.html')
        return render(request, 'resume_edit.html', {'form':form})

    def post(self, request):
        resume = Resume.objects.get(user=request.user)
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше резюме обновлено!')
            return redirect(request.path)
        messages.error(request, 'Резюме не обновлено, что-то пошло не так')
        return render(request, 'resume_edit.html', {'form':form})


class ResumeCreate(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        form=ResumeForm
        return render(request, 'resume_edit.html', {'form':form})

    def post(self, request):
        resume=ResumeForm(request.POST)
        if resume.is_valid():
            result=resume.save(commit=False)
            result.user_id=request.user.id
            resume.save()
            messages.success(request, 'Поздравляем, Вы создали резюме!')
            return redirect('resume_start')
        messages.error(request, 'Резюме не создано, что-то пошло не так')
        return render(request, 'resume_edit.html', {'form':form})






class CompanyStart(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        try:
            if request.user.company:
                return redirect('my_company')
        except ObjectDoesNotExist:
            return render(request, 'company_start.html')


class MyCompany(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        company=request.user.company
        form=MyCompanyForm(instance=company)
        return render(request, 'my_company.html', {'form':form})

    def post(self, request):
        form=MyCompanyForm(request.POST, request.FILES, instance=request.user.company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect(request.path)
        messages.error(request, 'Что-то пошло не так!')
        return render(request,'my_company.html', {'form':form})

class CompanyCreate(View):
    def get(self, request):
        form=MyCompanyForm
        return render(request, 'company_create.html', {'form':form})

    def post(self, request):
        form=MyCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            new_company=form.save()
            new_company.owner=request.user
            new_company.save()
            messages.success(request,'Поздравляем, Вы успешно создали компнию')
            return redirect('my_company')
        messages.error(request, 'Компания не создана, проверьте правильность введенных данных')


class MyVacanciesList(View):
    def get(self, request):
        my_vacancies = Vacancy.objects.filter(company=request.user.company).annotate(appl_number=Count('applications'))
        if len(my_vacancies)>0:
            return render(request, 'vacancy_list.html', {'my_vacancies':my_vacancies})
        else:
            return render(request, 'vacancy_start.html')

class VacancyCreate(View):
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

class VacancyEdit(View):

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


class Main_page(View):

    def get(self, request):
        specialties = Specialty.objects.annotate(number_vacantion=Count('vacancies'))
        companies = Company.objects.annotate(number_companies=Count('companies'))
        return render(request, 'index.html', context={'all': {'specialties': specialties, 'companies': companies}})



class Search(View):
    def get(self, request):
        query = request.GET.get('search')
        if query==None or query=='':
            messages.error(request,'Ничего не найдено')
            return redirect('search')
        else:
            vacancies=Vacancy.objects.filter(Q(title__icontains=query)|
                                             Q(description__icontains=query)|
                                             Q(skills__icontains=query))
            if len(vacancies)==0:
                messages.error(request, 'Ничего не найдено')




        return render(request,'search.html', {'vacancies':vacancies})




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
            form=AplicationForm()
        except ObjectDoesNotExist:
            raise Http404('Такой вакансии нет')

        return render(request, 'vacancy.html', context={'vacancy': vacancy, 'form':form})

    def post(self, request, pk_vac):
        form=AplicationForm(request.POST)
        vacancy=Vacancy.objects.get(id=pk_vac)
        if form.is_valid():
            aplication=form.save(commit=False)
            aplication.vacancy=vacancy
            aplication.user=User.objects.get(id=vacancy.company.owner_id)
            aplication.save()
            return redirect('sent', pk_vac)
        return render(request, 'vacancy', pk_vac)

class AplicationSend(View):

    def get(self, request, pk_vac):
        return render(request, 'sent.html', context={'pk_vac':pk_vac})


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
