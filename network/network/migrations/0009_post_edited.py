# Generated by Django 4.1.4 on 2023-01-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0008_post_no_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="edited",
            field=models.BooleanField(default=False),
        ),
    ]
