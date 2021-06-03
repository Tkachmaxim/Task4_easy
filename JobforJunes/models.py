from django.db import models
from django.contrib.auth import get_user_model


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='speciality_images')


class Company(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='company_images')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner=models.OneToOneField(get_user_model(), null=True, on_delete=models.CASCADE, related_name='company')


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.CharField(max_length=20)


class Application(models.Model):
    written_username = models.CharField(max_length=50)
    written_phone = models.CharField(max_length=50)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, null=True, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, related_name='applications')


class User(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()