# Generated by Django 3.0.8 on 2020-07-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("siaes", "0023_auto_20200625_1134")]

    operations = [
        migrations.AlterField(
            model_name="siae",
            name="job_applications_blocked_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Date du dernier blocage de candidatures"),
        )
    ]
