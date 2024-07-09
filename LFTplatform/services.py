from datetime import timedelta, datetime
from django.db.models import Q
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
              f"{round((end - start) * 100000)}")
        return result

    return wrapper


def faction_filter_queryset(queryset, faction_filter):
    queryset = queryset.filter(
        faction=faction_filter
    ).distinct()

    return queryset


def selected_days_filter_queryset(queryset, selected_days_filter):
    queryset = queryset.filter(
        teams__activity_sessions__day_session_start__day_of_week__in=selected_days_filter
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


def activity_time_filter_queryset(queryset,
                                  selected_days_filter,
                                  activity_time_start_filter,
                                  activity_time_end_filter):
    
    user_start_datetime_format_time_time_format = datetime.strptime(
        activity_time_start_filter, "%H:%M"
    ).time()
    user_end_time_time_format = datetime.strptime(
        activity_time_end_filter, "%H:%M"
    ).time()

    user_start_datetime_format = datetime(
        1900, 1, 1,
        user_start_datetime_format_time_time_format.hour,
        user_start_datetime_format_time_time_format.minute
    )
    user_end_datetime_format = datetime(
        1900, 1, 1,
        user_end_time_time_format.hour,
        user_end_time_time_format.minute
    )
    
    if user_end_datetime_format < user_start_datetime_format:
        user_end_datetime_format += timedelta(days=1)
    print(user_start_datetime_format, user_end_datetime_format)
    print(user_end_datetime_format - user_start_datetime_format)
    queryset = queryset.filter(
        teams__activity_sessions__day_session_start__day_of_week__in=selected_days_filter
    ).distinct()

    team_queryset = Team.objects.filter(guild__in=queryset)
    filtered_team_queryset = Team.objects.none()

    for team in team_queryset:
        # if len(filtered_team_queryset) == 10:
        #     break
        for session in team.activity_sessions.all():
            start_overlap = user_start_datetime_format <= session.time_start
            end_overlap = user_end_datetime_format >= session.time_end
            condition = True if (start_overlap and end_overlap) else False
            print(user_start_datetime_format, user_end_datetime_format,
                  "|||", session.time_start, session.time_end, "|||",
                  start_overlap, end_overlap, condition)

            if condition:
                print(f"{team.team_name}: id {team.id} HAS BEEN ADDED")
                filtered_team_queryset |= Team.objects.filter(id=team.id)

    queryset = queryset.filter(teams__in=filtered_team_queryset).distinct()

    print("____________________________________________________")

    return [queryset, filtered_team_queryset]

