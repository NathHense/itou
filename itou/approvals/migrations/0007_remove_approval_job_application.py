# Generated by Django 2.2.9 on 2020-01-30 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("approvals", "0006_auto_20200130_1948"),
        ("job_applications", "0018_move_approvals"),
    ]

    operations = [
        migrations.RemoveField(model_name="approval", name="job_application"),
        migrations.RemoveField(model_name="approval", name="number_sent_by_email"),
    ]