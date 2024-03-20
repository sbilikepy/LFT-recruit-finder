# Generated by Django 4.1 on 2024-03-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("LFTplatform", "0008_activitysession_team_activity_sessions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="activity_time_end",
        ),
        migrations.RemoveField(
            model_name="team",
            name="activity_time_start",
        ),
        migrations.AlterField(
            model_name="activitysession",
            name="time_end",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="activitysession",
            name="time_start",
            field=models.TimeField(blank=True, null=True),
        ),
    ]