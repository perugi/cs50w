# Generated by Django 4.1.4 on 2023-01-04 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0011_listing_open"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="open",
            new_name="active",
        ),
    ]
