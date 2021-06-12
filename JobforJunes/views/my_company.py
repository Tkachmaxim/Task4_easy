from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from JobforJunes.forms import MyCompanyForm


class CompanyStart(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            request.user.company
            print(request.user.company)
            return redirect('my_company')
        except ObjectDoesNotExist:
            return render(request, r'my_company\company_start.html')


class MyCompany(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            company = request.user.company
            form = MyCompanyForm(instance=company)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, r'my_company\my_company.html', {'form': form})

    def post(self, request):
        form = MyCompanyForm(request.POST, request.FILES, instance=request.user.company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect(request.path)
        messages.error(request, 'Что-то пошло не так!')
        return render(request, r'my_company\my_company.html', {'form': form})


class CompanyCreate(View):
    def get(self, request):
        try:
            request.user.company
        except ObjectDoesNotExist:
            form = MyCompanyForm
            return render(request, r'my_company\company_create.html', {'form': form})
        return redirect('my_company')

    def post(self, request):
        form = MyCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            new_company = form.save()
            new_company.owner = request.user
            new_company.save()
            messages.success(request, 'Поздравляем, Вы успешно создали компнию')
            return redirect('my_company')
        messages.error(request, 'Компания не создана, проверьте правильность введенных данных')
