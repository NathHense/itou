# Generated by Django 2.2.3 on 2019-08-01 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_prescriber',
            field=models.BooleanField(default=False, verbose_name='Prescripteur'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_siae_staff',
            field=models.BooleanField(default=False, verbose_name='Employeur (SIAE)'),
        ),
    ]