# Generated by Django 4.1.4 on 2023-01-04 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_rename_starting_bid_listing_bid_alter_bid_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="open",
            field=models.BooleanField(default=True),
        ),
    ]
