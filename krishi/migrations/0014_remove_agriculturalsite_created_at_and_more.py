# Generated by Django 4.2.1 on 2024-02-11 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("krishi", "0013_agriculturalsite_siteimage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agriculturalsite",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="agriculturalsite",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="agriculturalsite",
            name="website",
        ),
    ]
