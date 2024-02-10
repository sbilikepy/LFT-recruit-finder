# Generated by Django 5.0.2 on 2024-02-08 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LFTplatform", "0003_recruit"),
    ]

    operations = [
        migrations.CreateModel(
            name="Character",
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
                ("nickname", models.CharField(max_length=12)),
                ("class_name", models.CharField(max_length=16)),
                ("spec_name", models.CharField(max_length=16)),
                ("item_lvl", models.IntegerField()),
                ("wcl_show", models.BooleanField()),
                ("wcl", models.URLField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="LFTplatform.recruit",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "characters",
                "ordering": ["spec_name"],
            },
        ),
    ]
