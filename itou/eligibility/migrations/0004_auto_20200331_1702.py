# Generated by Django 3.0.4 on 2020-03-31 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("eligibility", "0003_auto_20200324_0936")]

    operations = [
        migrations.AlterModelOptions(
            name="administrativecriteria",
            options={
                "ordering": ["level", "ui_rank"],
                "verbose_name": "Critère administratif",
                "verbose_name_plural": "Critères administratifs",
            },
        )
    ]
