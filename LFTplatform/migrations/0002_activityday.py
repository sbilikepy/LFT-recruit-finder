# Generated by Django 5.0.2 on 2024-02-08 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LFTplatform", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActivityDay",
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
                (
                    "day_of_week",
                    models.CharField(
                        choices=[
                            ("mon", "Monday"),
                            ("tue", "Tuesday"),
                            ("wed", "Wednesday"),
                            ("thu", "Thursday"),
                            ("fri", "Friday"),
                            ("sat", "Saturday"),
                            ("sun", "Sunday"),
                        ],
                        max_length=3,
                    ),
                ),
            ],
        ),
    ]