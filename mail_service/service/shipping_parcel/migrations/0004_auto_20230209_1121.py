# Generated by Django 2.2.7 on 2023-02-09 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shipping_parcel", "0003_auto_20230209_1059"),
    ]

    operations = [
        migrations.RenameField(
            model_name="parcel",
            old_name="is_withdraw",
            new_name="withdraw_bids",
        ),
    ]