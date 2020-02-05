# Generated by Django 2.2.9 on 2020-01-30 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("approvals", "0005_auto_20200130_1535")]

    operations = [
        migrations.AlterField(
            model_name="approval",
            name="job_application",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tmp_approvals",
                to="job_applications.JobApplication",
                verbose_name="Candidature d'origine",
            ),
        )
    ]