import os

import django

from django.db.models import Count

os.environ["DJANGO_SETTINGS_MODULE"] = 'Sitevacantion.settings'
django.setup()

from JobforJunes import data

from JobforJunes.models import Specialty, Company, Vacancy

'''
for specialty in data.specialties:
    object_spec=Specialty(code=specialty['code'], title=specialty['title'])
    object_spec.save()


for company in data.companies:
    new_company=Company(name=company['title'], location=company['location'], description=company['description'], employee_count=company['employee_count'])
    new_company.save()


for vacantion in data.jobs:
    new_vacantion=Vacancy(title=vacantion['title'], specialty=Specialty.objects.filter(code=vacantion['specialty'])[0], company=Company.objects.filter(id=vacantion['company'])[0],
                          skills=vacantion['skills'], description=vacantion['description'], salary_min=vacantion['salary_from'], salary_max=vacantion['salary_to'],
                          published_at=vacantion['posted'])
    new_vacantion.save()

'''

p=Specialty.objects.annotate(num_vacancies=Count('vacancies'))

for z in p:
    print(z.num_vacancies)





