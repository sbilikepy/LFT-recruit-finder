# Generated by Django 4.1 on 2024-04-19 15:00

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
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
                            ("Mon", "Mon"),
                            ("Tue", "Tue"),
                            ("Wed", "Wed"),
                            ("Thu", "Thu"),
                            ("Fri", "Fri"),
                            ("Sat", "Sat"),
                            ("Sun", "Sun"),
                        ],
                        max_length=3,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ActivitySession",
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
                ("time_start", models.TimeField(blank=True, null=True)),
                ("time_end", models.TimeField(blank=True, null=True)),
            ],
        ),
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
                ("item_lvl", models.IntegerField()),
                ("wcl_show", models.BooleanField()),
                ("wcl", models.URLField(blank=True)),
            ],
            options={
                "verbose_name_plural": "characters",
            },
        ),
        migrations.CreateModel(
            name="CharacterCharacteristics",
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
                    "class_name",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Death Knight", "Death Knight"),
                            ("Druid", "Druid"),
                            ("Hunter", "Hunter"),
                            ("Mage", "Mage"),
                            ("Paladin", "Paladin"),
                            ("Priest", "Priest"),
                            ("Rogue", "Rogue"),
                            ("Shaman", "Shaman"),
                            ("Warlock", "Warlock"),
                            ("Warrior", "Warrior"),
                        ],
                        default="class_name",
                        max_length=16,
                        null=True,
                    ),
                ),
                (
                    "spec_name",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Blood", "Blood"),
                            ("Frost", "Frost"),
                            ("Unholy", "Unholy"),
                            ("Balance", "Balance"),
                            ("Feral dps", "Feral dps"),
                            ("Feral tank", "Feral tank"),
                            ("Restoration", "Restoration"),
                            ("Beast Mastery", "Beast Mastery"),
                            ("Marksmanship", "Marksmanship"),
                            ("Survival", "Survival"),
                            ("Arcane", "Arcane"),
                            ("Fire", "Fire"),
                            ("Frost", "Frost"),
                            ("Holy", "Holy"),
                            ("Protection", "Protection"),
                            ("Retribution", "Retribution"),
                            ("Discipline", "Discipline"),
                            ("Holy", "Holy"),
                            ("Shadow", "Shadow"),
                            ("Assassination", "Assassination"),
                            ("Combat", "Combat"),
                            ("Subtlety", "Subtlety"),
                            ("Elemental", "Elemental"),
                            ("Enhancement", "Enhancement"),
                            ("Restoration", "Restoration"),
                            ("Affliction", "Affliction"),
                            ("Demonology", "Demonology"),
                            ("Destruction", "Destruction"),
                            ("Arms", "Arms"),
                            ("Fury", "Fury"),
                            ("Protection", "Protection"),
                        ],
                        default="spec_name",
                        max_length=16,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Class-spec combinations",
                "ordering": ["class_name", "spec_name"],
            },
        ),
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
                ("guild_name", models.CharField(max_length=24, unique=True)),
                (
                    "faction",
                    models.CharField(
                        choices=[
                            ("Any", "Any"),
                            ("Alliance", "Alliance"),
                            ("Horde", "Horde"),
                        ],
                        max_length=8,
                    ),
                ),
                ("highest_progress", models.IntegerField(default=0)),
                ("discord_link", models.URLField(blank=True, null=True)),
                ("apply_link", models.URLField(blank=True, null=True)),
                ("wcl_link", models.URLField(blank=True, null=True)),
                ("guild_note", models.CharField(max_length=4096)),
            ],
            options={
                "verbose_name_plural": "guilds",
                "ordering": ["guild_name"],
            },
        ),
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "discord_id",
                    models.CharField(
                        default="ADMIN_DEFAULT_DISCORD_ID", max_length=512
                    ),
                ),
                ("avatar", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "global_name",
                    models.CharField(
                        default="ADMIN_DEFAULT_DISCORD_NAME", max_length=32, unique=True
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("Recruiter", "Recruiter"), ("Rookie", "Rookie")],
                        default="ADMIN_DEFAULT_SUPERUSER",
                        max_length=16,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "ordering": ["username"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                ("team_name", models.CharField(blank=True, max_length=24, null=True)),
                (
                    "loot_system",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("EPGP", "EPGP"),
                            ("LC", "LC"),
                            ("SR", "SR"),
                            ("DKP", "DKP"),
                            ("GDKP", "GDKP"),
                            ("Other", "Other"),
                        ],
                        default="Undefined",
                        max_length=16,
                        null=True,
                    ),
                ),
                (
                    "team_size",
                    models.IntegerField(
                        blank=True, choices=[(25, 25), (10, 10)], null=True
                    ),
                ),
                (
                    "team_progress",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                (
                    "activity_sessions",
                    models.ManyToManyField(
                        related_name="sessions", to="LFTplatform.activitysession"
                    ),
                ),
                (
                    "guild",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams",
                        to="LFTplatform.guild",
                    ),
                ),
                (
                    "looking_for",
                    models.ManyToManyField(
                        blank=True,
                        related_name="teams_looking_for",
                        to="LFTplatform.charactercharacteristics",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "teams",
            },
        ),
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
                ("discord", models.CharField(blank=True, max_length=512, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("note", models.CharField(blank=True, max_length=512, null=True)),
                ("activity_time_start", models.TimeField(blank=True, null=True)),
                ("activity_time_end", models.TimeField(blank=True, null=True)),
                (
                    "activity_days_recruit",
                    models.ManyToManyField(
                        blank=True,
                        related_name="recruits",
                        to="LFTplatform.activityday",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="guild",
            name="recruiter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recruiter",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="charactercharacteristics",
            constraint=models.UniqueConstraint(
                fields=("class_name", "spec_name"), name="unique_class_spec_combination"
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="class_spec_combination",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="characters",
                to="LFTplatform.charactercharacteristics",
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="character",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="activitysession",
            name="day",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="LFTplatform.activityday",
                verbose_name="day_of_week",
            ),
        ),
        migrations.AddConstraint(
            model_name="team",
            constraint=models.UniqueConstraint(
                fields=("team_name", "guild"), name="unique_team_name_for_each_guild"
            ),
        ),
    ]
