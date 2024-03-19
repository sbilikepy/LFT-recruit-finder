# Generated by Django 4.1 on 2024-03-19 06:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("LFTplatform", "0011_remove_team_activity_days_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="charactercharacteristics",
            name="class_name",
            field=models.CharField(
                blank=True,
                choices=[
                    ("dk", "Death Knight"),
                    ("druid", "Druid"),
                    ("hunter", "Hunter"),
                    ("mage", "Mage"),
                    ("paladin", "Paladin"),
                    ("priest", "Priest"),
                    ("rogue", "Rogue"),
                    ("shaman", "Shaman"),
                    ("warlock", "Warlock"),
                    ("warrior", "Warrior"),
                ],
                default="class_name",
                max_length=16,
                null=True,
            ),
        ),
    ]
