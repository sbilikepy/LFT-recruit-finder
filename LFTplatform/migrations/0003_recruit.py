# Generated by Django 5.0.2 on 2024-02-08 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LFTplatform", "0002_activityday"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recruit",
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
                ("name", models.CharField(max_length=16)),
                ("note", models.CharField(max_length=512)),
                ("activity_time_start", models.TimeField()),
                ("activity_time_end", models.TimeField()),
                ("activity_days", models.ManyToManyField(to="LFTplatform.activityday")),
            ],
        ),
    ]