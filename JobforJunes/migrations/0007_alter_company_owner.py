# Generated by Django 3.2.3 on 2021-06-03 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('JobforJunes', '0006_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='company', to=settings.AUTH_USER_MODEL),
        ),
    ]
