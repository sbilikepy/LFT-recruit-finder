# Generated by Django 4.1 on 2024-03-20 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("LFTplatform", "0015_alter_guild_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guild",
            name="faction",
            field=models.CharField(
                choices=[("Alliance", "Alliance"), ("Horde", "Horde")], max_length=8
            ),
        ),
    ]
