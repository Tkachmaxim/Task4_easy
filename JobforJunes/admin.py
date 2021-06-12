from django.contrib import admin
from .models import Specialty, Vacancy, Company


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
