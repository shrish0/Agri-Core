# Generated by Django 4.2.1 on 2024-02-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("krishi", "0015_faq"),
    ]

    operations = [
        migrations.AddField(
            model_name="agriculturalsite",
            name="price",
            field=models.IntegerField(default=1000),
        ),
    ]
