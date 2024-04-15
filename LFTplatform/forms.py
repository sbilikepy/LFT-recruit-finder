from django import forms

from .models import *


class CharacterSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search for a rookie"}),
    )


class GuildFilterForm(forms.Form):
    Guild.FACTION_CHOICES.insert(0, ("Any", "Any"))

    faction = forms.ChoiceField(
        label="Faction",
        widget=forms.RadioSelect(),
        choices=Guild.FACTION_CHOICES,
        required=False,
    )

    activity_time_start_hour = forms.ChoiceField(
        label="RT start",
        choices=ActivitySession.MINUTE_CHOICES,
        required=False,
    )
    activity_time_end_hour = forms.ChoiceField(
        label="RT end", choices=ActivitySession.MINUTE_CHOICES, required=False
    )

    selected_days = forms.MultipleChoiceField(
        label="Activity days",
        choices=ActivityDay.DAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    raid_team_size = forms.MultipleChoiceField(
        label="Raid size",
        choices=Team.TEAM_SIZE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    loot_system = forms.MultipleChoiceField(
        label="Loot system",
        choices=Team.LOOT_SYSTEM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # in_game_class = forms.MultipleChoiceField(
    #     label="Classes",
    #     choices=CharacterCharacteristics.CLASS_CHOICES,
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )

    class_spec_combination = forms.MultipleChoiceField(
        label="Classes",
        choices=CharacterCharacteristics.CLASS_CHOICES,

    )
