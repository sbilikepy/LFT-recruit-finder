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
    faction = forms.ChoiceField(
        label="Faction",
        widget=forms.RadioSelect,
        choices=Guild.FACTION_CHOICES,
        required=False,
        initial="Alliance",  # TODO: read more docs about it
    )

    activity_time_start_hour = forms.ChoiceField(
        label="From",
        choices=ActivitySession.MINUTE_CHOICES,
        required=False,
    )
    activity_time_end_hour = forms.ChoiceField(
        label="To",
        choices=ActivitySession.MINUTE_CHOICES,
        required=False
    )

    day_choices = ActivityDay.DAY_CHOICES
    days_of_week = [day[0] for day in day_choices]
    for day_code, day_name in day_choices:
        locals()[day_code] = forms.BooleanField(
            label=day_name,
            required=False,
            initial=True
        )
