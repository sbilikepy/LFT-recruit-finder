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


class ActivityDay(models.Model):
    """
    Represents a day of the week for specifying activity schedule
    """

    DAY_CHOICES = [
        ("Mon", "Mon"),
        ("Tue", "Tue"),
        ("Wed", "Wed"),
        ("Thu", "Thu"),
        ("Fri", "Fri"),
        ("Sat", "Sat"),
        ("Sun", "Sun"),
    ]
    day_of_week = models.CharField(
        max_length=3,
        choices=DAY_CHOICES,
        unique=True)

    def __str__(self):
        return self.day_of_week


class ActivitySession(models.Model):  # for teams

    MINUTE_CHOICES = [(f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}")
                      for hour in range(0, 24)
                      for minute in range(0, 60, 15)]

    day = models.ForeignKey(
        ActivityDay, on_delete=models.CASCADE,
        verbose_name="day_of_week",
        null=True,
        blank=True
    )
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return (f"{self.day}:( {str(self.time_start)[:-3:]} - "
                f"{str(self.time_end)[:-3:]} )")


class Recruit(models.Model):
    """
    Represents a recruit, who looking for team
    """

    name = models.CharField(max_length=16)
    discord = models.CharField(max_length=512, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    note = models.CharField(max_length=512, null=True, blank=True)

    activity_days_recruit = models.ManyToManyField(
        ActivityDay, related_name="recruits", blank=True
    )
    activity_time_start = models.TimeField(null=True, blank=True)
    activity_time_end = models.TimeField(null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return self.name


class CharacterCharacteristics(models.Model):
    CLASS_CHOICES = [
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

    ]
    SPEC_CHOICES = [
        ("blood", "Blood"),
        ("frost", "Frost"),
        ("unholy", "Unholy"),
        ("balance", "Balance"),
        ("feral_dps", "Feral dps"),
        ("feral_tank", "Feral tank"),
        ("restoration", "Restoration"),
        ("beast_mastery", "Beast mastery"),
        ("marksmanship", "Marksmanship"),
        ("survival", "Survival"),
        ("arcane", "Arcane"),
        ("fire", "Fire"),
        ("holy", "Holy"),
        ("protection", "Protection"),
        ("retribution", "Retribution"),
        ("discipline", "Discipline"),
        ("shadow", "Shadow"),
        ("assassination", "Assassination"),
        ("combat", "Combat"),
        ("subtlety", "Subtlety"),
        ("elemental", "Elemental"),
        ("enhancement", "Enhancement"),
        ("affliction", "Affliction"),
        ("demonology", "Demonology"),
        ("destruction", "Destruction"),
        ("arms", "Arms"),
        ("fury", "Fury"),
    ]
    class_name = models.CharField(
        choices=CLASS_CHOICES,
        max_length=16, blank=True, null=True,
        default="class_name"
    )

    spec_name = models.CharField(
        choices=SPEC_CHOICES,
        max_length=16,
        blank=True,
        null=True,
        default="spec_name"
    )

    class Meta:
        verbose_name_plural = "Class-spec combinations"
        ordering = ["class_name", "spec_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["class_name", "spec_name"],
                name="unique_class_spec_combination"
            ),
        ]

    def __str__(self):
        return f"{self.spec_name} {self.class_name}"


class Character(models.Model):
    """
    Represents a character owned by a recruit
    """

    owner = models.ForeignKey(
        Recruit, on_delete=models.CASCADE, related_name="character"
    )

    nickname = models.CharField(max_length=12)
    class_spec_combination = models.ForeignKey(
        CharacterCharacteristics,
        on_delete=models.CASCADE,
        related_name="characters",
        null=True,
        blank=True,
    )
    item_lvl = models.IntegerField()

    wcl_show = models.BooleanField()
    wcl = models.URLField(blank=True)

    # listing_started = models.DateField(
    #     auto_now=True)

    class Meta:
        verbose_name_plural = "characters"
        # ordering = ["listing_started"]

    def __str__(self):
        return f"{self.spec_name} {self.class_name}"


class Guild(models.Model):
    """
    Represents a gaming guild with associated recruiter
    """

    guild_name = models.CharField(max_length=24, blank=False, null=False,
                                  unique=True)
    FACTION_CHOICES = [
        ("Alliance", "Alliance"),
        ("Horde", "Horde"),
    ]
    faction = models.CharField(
        choices=FACTION_CHOICES,
        max_length=8,
        blank=False,
        null=False,
    )

    recruiter = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        related_name="recruiter"
    )
    highest_progress = models.IntegerField(default=0)
    discord_link = models.URLField(blank=True, null=True)
    apply_link = models.URLField(blank=True, null=True)
    wcl_link = models.URLField(blank=True, null=True)
    guild_note = models.CharField(max_length=4096)

    class Meta:
        verbose_name_plural = "guilds"
        ordering = ["guild_name"]  # TODO: random ordering in ListView

    def __str__(self):
        return f"{self.guild_name}"


class Team(models.Model):
    """
    Represents a team as part of guild with activity schedule
    """
    TEAM_SIZE_CHOICES = [
        ("25", "25"),
        ("10", "10"),
    ]

    LOOT_SYSTEM_CHOICES = [

        ("EPGP", "EPGP"),
        ("LC", "LC"),
        ("SR", "SR"),
        ("DKP", "DKP"),
        ("GDKP", "GDKP"),
        ("Other", "Other"),

    ]

    guild = models.ForeignKey(
        "Guild",
        on_delete=models.CASCADE,
        related_name="teams",
        null=True,
        blank=True,
    )
    team_name = models.CharField(
        max_length=24,
        unique=False,
        null=True,
        blank=True,
    )

    loot_system = models.CharField(  # TODO: choices / form validation
        choices=LOOT_SYSTEM_CHOICES,
        max_length=16,
        default="Undefined",
        null=True,
        blank=True
    )
    team_size = models.IntegerField(
        choices=TEAM_SIZE_CHOICES,
        null=True,
        blank=True,
    )  # TODO: validator max
    team_progress = models.IntegerField(null=True, blank=True, default=0)  #
    # TODO: validator min

    looking_for = models.ManyToManyField(
        CharacterCharacteristics,
        related_name="teams_looking_for",
        blank=True,
    )
    activity_sessions = models.ManyToManyField(
        ActivitySession,
        related_name="sessions"

    )

    class Meta:
        verbose_name_plural = "teams"
        constraints = [
            models.UniqueConstraint(
                fields=["team_name", "guild"],
                name="unique_team_name_for_each_guild"
            ),
        ]

    def clean(self):
        if not self.team_name:
            self.team_name = (
                f"{self.guild.guild_name} team"
                f"№ {Team.objects.filter(guild=self.guild).count() + 1}"
            )
        if self.team_progress:
            if self.team_progress > self.guild.highest_progress:
                self.guild.highest_progress = self.team_progress

        self.guild.save()

    def __str__(self):
        return f"{self.team_name}"
