# Generated by Django 5.0.2 on 2024-02-14 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LFTplatform", "0002_alter_activityday_day_of_week_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="guild",
            options={"verbose_name_plural": "guilds"},
        ),
        migrations.AlterField(
            model_name="character",
            name="wcl",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="recruit",
            name="activity_days_recruit",
            field=models.ManyToManyField(
                blank=True,
                related_name="recruit_activity_days",
                to="LFTplatform.activityday",
            ),
        ),
    ]