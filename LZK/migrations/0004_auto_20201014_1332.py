# Generated by Django 2.2.16 on 2020-10-14 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LZK", "0003_auto_20201013_1415"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ability",
            name="levels",
            field=models.ManyToManyField(blank=True, to="LZK.Level"),
        ),
    ]
