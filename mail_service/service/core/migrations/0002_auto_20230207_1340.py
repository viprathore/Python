# Generated by Django 2.2.7 on 2023-02-07 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AlterModelTable(
            name="user",
            table="user",
        ),
    ]
