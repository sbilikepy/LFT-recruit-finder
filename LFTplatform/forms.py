from django import forms
from .models import *


class CharacterSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search for a rookie"}),
    )


# class GuildSearchForm(forms.Form):
#     guild_name = forms.CharField(
#         max_length=255,
#         required=False,
#         label="",
#         widget=forms.TextInput(attrs={"placeholder": "Search for a guild"}),
#     )


class GuildFilterForm(forms.Form):
    FACTION_CHOICES = [
        ("Alliance", "Alliance"),
        ("Horde", "Horde"),
    ]
    faction = forms.CheckboxSelectMultiple(choices=FACTION_CHOICES)
    activity_time_start = forms.TimeField(required=False)
    activity_time_end = forms.TimeField(required=False)
    # activity_days = forms.CheckboxSelectMultiple()
    # loot_distribution_rules = forms.CheckboxSelectMultiple()
    # classes_and_specs = forms.CheckboxSelectMultiple()
