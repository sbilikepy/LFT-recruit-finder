from django.contrib.auth.models import AbstractUser
from django.db import models


class Recruiter(AbstractUser):
    """
    Custom user model representing a recruiter in the system
    """

    class Meta:
        verbose_name_plural = "recruiters"
        verbose_name = "recruiter"
        ordering = ["username"]


class Recruit(models.Model):
    """
    Represents a recruit, who looking for team
    """

    name = models.CharField(max_length=16)
    note = models.CharField(max_length=512)
    DAY_CHOICES = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]
    activity_days_recruit = models.CharField(
        max_length=3,
        choices=DAY_CHOICES,
        unique=True,
        null=True,
        blank=True,
    )
    activity_time_start = models.TimeField()
    activity_time_end = models.TimeField()

    class Meta:
        pass

    def __str__(self):
        return f"{self.name}"


class Character(models.Model):
    """
    Represents a character owned by a recruit
    """

    owner = models.ForeignKey(Recruit, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=12)

    class_name = models.CharField(max_length=16)
    spec_name = models.CharField(max_length=16)
    item_lvl = models.IntegerField()

    wcl_show = models.BooleanField()
    wcl = models.URLField()

    class Meta:
        verbose_name_plural = "characters"
        ordering = ["spec_name"]

    def __str__(self):
        return f"{self.spec_name} {self.class_name}"


class Guild(models.Model):
    """
    Represents a gaming guild with associated recruiter
    """

    name = models.CharField(
        max_length=24,
        blank=False,
        null=False,
        unique=True
    )
    FACTION_CHOICES = [
        ("alliance", "Alliance"),
        ("horde", "Horde"),
    ]
    faction = models.CharField(
        choices=FACTION_CHOICES,
        max_length=8,
        blank=False,
        null=False,
    )

    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, related_name="recruiter"
    )
    highest_progress = models.IntegerField(default=0)
    apply_link = models.URLField()
    wcl_link = models.URLField()
    guild_note = models.CharField(max_length=4096)

    class Meta:
        verbose_name_plural = "guilds"
        ordering = ["?"]

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    """
    Represents a team as part of guild with activity schedule
    """

    guild = models.ForeignKey(
        "Guild",
        on_delete=models.CASCADE,
        related_name="guild",
    )
    name = models.CharField(
        max_length=24,
        unique=False,
    )
    loot_system = models.CharField(
        max_length=16,
        default="Undefined",
    )
    team_size = models.IntegerField()
    team_progress = models.IntegerField(default=0)

    DAY_CHOICES = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]

    activity_days_team = models.CharField(
        max_length=3,
        choices=DAY_CHOICES,
        unique=True,
        null=True,
        blank=True,
    )
    activity_time_start = models.TimeField()
    activity_time_end = models.TimeField()

    class Meta:
        verbose_name_plural = "teams"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "guild"],
                name="unique_team_name_for_each_guild"
            ),
        ]

    def clean(self):
        if not self.name:
            self.name = (
                f"{self.guild.name} team"
                f"№ {Team.objects.filter(guild=self.guild).count() + 1}"
            )

        if self.team_progress > self.guild.highest_progress:
            self.guild.highest_progress = self.team_progress

        self.guild.save()

    def __str__(self):
        return f"{self.name}"
