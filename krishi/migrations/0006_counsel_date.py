# Generated by Django 4.2.1 on 2023-11-12 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("krishi", "0005_counsel_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="counsel",
            name="date",
            field=models.DateField(default="2023-02-01"),
        ),
    ]
