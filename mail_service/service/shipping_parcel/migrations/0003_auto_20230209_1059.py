# Generated by Django 2.2.7 on 2023-02-09 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shipping_parcel", "0002_remove_train_train_lines"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="train",
            name="full_capacity",
        ),
        migrations.RemoveField(
            model_name="train",
            name="remaining_capacity",
        ),
        migrations.AddField(
            model_name="train",
            name="capacity",
            field=models.DecimalField(
                decimal_places=2,
                default=2.4,
                help_text="capacity of the train",
                max_digits=12,
            ),
            preserve_default=False,
        ),
    ]
