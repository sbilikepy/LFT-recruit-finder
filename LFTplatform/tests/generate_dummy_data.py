import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LFTdjangoProject.settings')
django.setup()

from django.contrib.auth import get_user_model
from faker import Faker
from LFTplatform.models import Guild, Team, ActivitySession, \
    CharacterCharacteristics, ActivityDay

User = get_user_model()
fake = Faker()


def create_fake_users(num_users):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        discord_id = fake.random_number(digits=9)
        avatar = fake.lexify(text='?' * 15)
        public_server_name = fake.word().capitalize()
        recruiter_role = fake.boolean()
        user = User.objects.create_user(username=username, email=email)
        user.discord_id = discord_id
        user.avatar = avatar
        user.public_server_name = public_server_name
        user.recruiter_role = recruiter_role
        user.save()


def create_fake_guilds(num_guilds):
    for _ in range(num_guilds):
        guild_name = str(
            fake.word()[:24]).capitalize() + " " + fake.word()[:24]  # Take
        # first 24 characters
        faction = fake.random_element(elements=("Alliance", "Horde"))
        recruiter = User.objects.order_by('?').first()  # Random recruiter
        highest_progress = fake.random_int(0, 12)
        discord_link = fake.url() if fake.boolean(
            chance_of_getting_true=50) else None
        apply_link = fake.url() if fake.boolean(
            chance_of_getting_true=50) else None
        wcl_link = fake.url() if fake.boolean(
            chance_of_getting_true=50) else None
        guild_note = fake.text(max_nb_chars=4096)

        Guild.objects.create(
            guild_name=guild_name,
            faction=faction,
            recruiter=recruiter,
            highest_progress=highest_progress,
            discord_link=discord_link,
            apply_link=apply_link,
            wcl_link=wcl_link,
            guild_note=guild_note
        )


def create_fake_teams(num_teams):
    for _ in range(num_teams):
        guild = Guild.objects.order_by('?').first()
        team_name = fake.word()[:24].capitalize()
        loot_system = fake.random_element(
            elements=("EPGP", "LC", "SR", "DKP", "GDKP", "Other"))
        team_size = fake.random_element(elements=(25, 10))
        team_progress = fake.random_int(min=0, max=12)

        activity_sessions = ActivitySession.objects.order_by('?')[
                            :fake.random_int(min=1, max=3)]

        looking_for = CharacterCharacteristics.objects.order_by('?')[
                      :fake.random_int(min=2, max=5)]
        print(looking_for)
        Team.objects.create(
            guild=guild,
            team_name=team_name,
            loot_system=loot_system,
            team_size=team_size,
            team_progress=team_progress
        )
        team.looking_for.set(looking_for)


        team.activity_sessions.add(*activity_sessions)


def create_fake_activity_sessions(num_sessions):
    days_of_week = ActivityDay.objects.all()

    for _ in range(num_sessions):
        day = random.choice(days_of_week)
        time_start = f"{random.randint(0, 23):02d}:{random.choice([0, 15, 30, 45]):02d}"
        time_end = f"{random.randint(0, 23):02d}:{random.choice([0, 15, 30, 45]):02d}"

        ActivitySession.objects.create(
            day=day,
            time_start=time_start,
            time_end=time_end
        )
        print(f"{day},{time_start},{time_end}")


def create_fake_recruits(num_recruits):
    days_of_week = ActivityDay.objects.all()

        for session in activity_sessions:
            Team.objects.get(team_name=team_name).activity_sessions.add(
                session)


if __name__ == "__main__":
    create_fake_users(1)
    create_fake_guilds(1)
    create_fake_teams(1)
