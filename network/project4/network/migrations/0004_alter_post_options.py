# Generated by Django 4.1.4 on 2023-01-22 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0003_user_following"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-timestamp"]},
        ),
    ]
