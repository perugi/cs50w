# Generated by Django 4.1.4 on 2023-01-04 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_alter_listing_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="bid",
            new_name="starting_bid",
        ),
        migrations.CreateModel(
            name="Bid",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bid", models.FloatField(max_length=100)),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "bidder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bids",
                        to="auctions.listing",
                    ),
                ),
            ],
        ),
    ]