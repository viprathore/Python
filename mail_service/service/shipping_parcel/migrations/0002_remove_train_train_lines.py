# Generated by Django 2.2.7 on 2023-02-09 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shipping_parcel", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="train",
            name="train_lines",
        ),
    ]
