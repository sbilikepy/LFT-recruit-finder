from datetime import timedelta

from LFTplatform.models import *

CLASS_SPEC_VALID_COMBINATIONS = {
    "Death Knight": {"Blood", "Frost", "Unholy"},
    "Druid": {"Balance", "Feral dps", "Feral tank", "Restoration"},  # !
    "Hunter": {"Beast mastery", "Marksmanship", "Survival"},
    "Mage": {"Arcane", "Fire", "Frost"},  # !
    "Paladin": {"Holy", "Protection", "Retribution"},  # !
    "Priest": {"Discipline", "Holy", "Shadow"},  # !  # !
    "Rogue": {"Assassination", "Combat", "Subtlety"},
    "Shaman": {"Elemental", "Enhancement", "Restoration"},  # !
    "Warlock": {"Affliction", "Demonology", "Destruction"},
    "Warrior": {"Arms", "Fury", "Protection"},  # !
}

CLASS_CHOICES = [
    (class_name, class_name) for class_name in
    CLASS_SPEC_VALID_COMBINATIONS.keys()
]

SPEC_CHOICES = [
    (spec, spec)
    for class_name, specs in CLASS_SPEC_VALID_COMBINATIONS.items()
    for spec in sorted(specs)
]


def time_decorator(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Start: {start}| End: {end} | Request processing takes:"
              f" {round(end - start, 2)} s. "
              f"Score: "
              f"{(end - start) * 100000}")
        return result

    return wrapper


def faction_filter_queryset(queryset, faction_filter):
    queryset = queryset.filter(
        faction=faction_filter
    ).distinct()
    return queryset


def selected_days_filter_queryset(queryset, selected_days_filter):
    queryset = queryset.filter(
        teams__activity_sessions__day__day_of_week__in=selected_days_filter
    ).distinct()
    return queryset


def selected_team_sizes_filter_queryset(queryset, selected_team_sizes):
    queryset = queryset.filter(
        teams__team_size__in=selected_team_sizes
    ).distinct()
    return queryset


def selected_loot_systems_filter_queryset(queryset, selected_loot_systems):
    queryset = queryset.filter(
        teams__loot_system__in=selected_loot_systems
    ).distinct()
    return queryset


def selected_classes_filter_queryset(queryset, selected_classes):
    queryset = queryset.filter(
        teams__looking_for__class_name__in=selected_classes
    ).distinct()
    return queryset


def selected_specs_filter_queryset(queryset, selected_specs):
    spec_combinations_ids = [
        combination.pk
        for combination in CharacterCharacteristics.objects.all()
        if combination.__str__() in selected_specs
    ]

    queryset = queryset.filter(
        teams__looking_for__id__in=spec_combinations_ids
    ).distinct()
    return queryset


import pytz


def activity_time_filter_queryset(queryset,
                                  selected_days_filter,
                                  activity_time_start_filter,
                                  activity_time_end_filter):
    user_start = datetime.strptime(activity_time_start_filter,
                                   '%H:%M').replace(tzinfo=pytz.utc)
    user_end = datetime.strptime(activity_time_end_filter, '%H:%M').replace(
        tzinfo=pytz.utc)

    if user_end < user_start:
        user_end += timedelta(days=1)
        print("delta change user: ", user_start, "-", user_end)

    queryset = queryset.filter(
        teams__activity_sessions__day__day_of_week__in=selected_days_filter
    ).distinct()

    team_queryset = Team.objects.filter(guild__in=queryset)
    filtered_team_queryset = Team.objects.none()

    for team in team_queryset:
        for session in team.activity_sessions.all():
            if session.time_end < session.time_start:
                session.time_end += timedelta(days=1)

            session_start = session.time_start.replace(tzinfo=pytz.utc)
            session_end = session.time_end.replace(tzinfo=pytz.utc)

            if session_start < user_start:
                if session_end < user_start:
                    session.time_start += timedelta(days=1)
                    session.time_end += timedelta(days=1)

            if user_start <= session_start <= session_end <= user_end:
                filtered_team_queryset |= Team.objects.filter(id=team.id)

    print(filtered_team_queryset)
    return queryset
