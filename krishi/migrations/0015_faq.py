# Generated by Django 4.2.1 on 2024-02-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("krishi", "0014_remove_agriculturalsite_created_at_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FaQ",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.TextField(default="Not Available")),
                ("answer", models.TextField(default="Not Available")),
            ],
        ),
    ]