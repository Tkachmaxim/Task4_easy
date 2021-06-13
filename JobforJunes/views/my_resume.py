from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View

from JobforJunes.forms import ResumeForm
from JobforJunes.models import Resume


class ResumeStart(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            resume = Resume.objects.get(user=request.user)
            form = ResumeForm(instance=resume)
        except ObjectDoesNotExist:
            return render(request, r'my_resume/resume_create.html')
        return render(request, r'my_resume/resume_edit.html', {'form': form})

    def post(self, request):
        resume = Resume.objects.get(user=request.user)
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше резюме обновлено!')
            return redirect(request.path)
        messages.error(request, 'Резюме не обновлено, что-то пошло не так')
        return render(request, r'my_resume/resume_edit.html', {'form': form})


class ResumeCreate(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            request.user.resume
        except ObjectDoesNotExist:
            form = ResumeForm
            return render(request, r'my_resume/resume_edit.html', {'form': form})

        return redirect('resume_start')

    def post(self, request):
        resume = ResumeForm(request.POST)
        if resume.is_valid():
            result = resume.save(commit=False)
            result.user_id = request.user.id
            resume.save()
            messages.success(request, 'Поздравляем, Вы создали резюме!')
            return redirect('resume_start')
        messages.error(request, 'Резюме не создано, что-то пошло не так')
        form = ResumeForm
        return render(request, r'my_resume/resume_edit.html', {'form': form})
