# Generated by Django 4.1 on 2024-02-26 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("LFTplatform", "0002_team_in_search_for_a"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="guild",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="LFTplatform.guild",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="loot_system",
            field=models.CharField(
                blank=True, default="Undefined", max_length=16, null=True
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="team_name",
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name="team",
            name="team_size",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]