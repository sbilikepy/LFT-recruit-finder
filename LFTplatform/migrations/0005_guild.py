# Generated by Django 5.0.2 on 2024-02-08 18:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LFTplatform", "0004_character"),
    ]

    operations = [
        migrations.CreateModel(
            name="Guild",
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
                ("name", models.CharField(max_length=24, unique=True)),
                ("faction", models.CharField(max_length=8)),
                ("highest_progress", models.IntegerField(default=0)),
                ("apply_link", models.URLField()),
                ("wcl_link", models.URLField()),
                ("guild_note", models.CharField(max_length=4096)),
                (
                    "recruiter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recruiter",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "guilds",
                "ordering": ["?"],
            },
        ),
    ]