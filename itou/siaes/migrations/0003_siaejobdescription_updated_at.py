# Generated by Django 2.2.6 on 2019-10-17 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("siaes", "0002_auto_20190930_1527")]

    operations = [
        migrations.AddField(
            model_name="siaejobdescription",
            name="updated_at",
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name="Date de modification"),
        )
    ]
