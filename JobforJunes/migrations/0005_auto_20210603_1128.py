# Generated by Django 3.2.3 on 2021-06-03 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JobforJunes', '0004_auto_20210603_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='applications', to='JobforJunes.user'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='company', to='JobforJunes.user'),
        ),
    ]
