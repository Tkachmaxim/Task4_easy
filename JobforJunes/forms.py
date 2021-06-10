from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from JobforJunes.models import Company, Vacancy, Application, Resume


class MyCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('owner',)
        labels = {
            'name': 'Название компании',
            'logo': 'Логотип',
            'location': 'География',
            'description': 'Информация о компании',
            'employee_count': 'Количество человек в компании',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', ),
                Column('logo', ),
            ),
            Row(
                Column('employee_count', ),
                Column('location', ),
            ),
            Row(
                Column('description', ),
            ),
            Row(
                Column(Submit('submit', 'Сохранить')),
            ),
        )


class VacancyEditForm(forms.ModelForm):
    class Meta:
        model=Vacancy
        exclude=('published_at','company')
        labels={'title':'Название вакансии',
                'specialty':'Специализация',
                'salary_min':'Зарплата от:',
                'salary_max': 'Зарплата до:',
                'skills':'Требуемые навыки',
                'description':'Описание вакансии'
                }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper=FormHelper()
            self.helper.layout=Layout(
                Row(
                    Column('title',),
                    Column('specialty',),
                    ),
                Row(
                    Column('salary_min',),
                    Column('salary_max',),
                ),
                Row(
                    Column('skills',),
                ),
                Row(
                    Column('description',),
                ),
                Row(
                    Column(Submit('submit', 'Сохранить')),
                ),
            )


class AplicationForm(forms.ModelForm):
    class Meta:
        model=Application
        exclude=('vacancy', 'user')
        labels={'written_username':'Вас зовут',
                'written_phone':'Ваш телефон',
                'written_cover_letter':'Сопроводительное письмо'
                }


class ResumeForm (forms.ModelForm):
    class Meta:
        model=Resume
        exclude=('user',)
        labels={'name':'Имя',
                'surname':'Фамилия',
                'status':'Готовность к работе',
                'salary':'Ожидаемое вознаграждение',
                'specialty':'Специализация',
                'grade':'Квалификация',
                'education':'Образование',
                'experience':'Опыт работы',
                'portfolio':'Ссылка на портфолио'
                }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper=FormHelper()
            self.helper.layout=Layout(
                Row(
                    Column('name',),
                    Column(),
                    Column('surname',),
                ),
                Row(
                    Column('status',),
                    Column('salary',),
                ),
                Row(
                    Column('specialty',),
                    Column('grade',),
                ),
                Row(
                    Column('education',),
                ),
                Row(
                    Column('experience',),
                ),
                Row(
                    Column('portfolio',)
                ),
                Row(
                    Column(Submit('submit', 'Сохранить')),
            ),
            )
