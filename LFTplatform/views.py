from datetime import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import *
from .models import *


def index(request):
    """View function for the home page of the site."""

    return render(
        request,
        template_name="LFTplatform/index.html",
        context={
            "guilds_count": Guild.objects.count(),
            "teams_count": Team.objects.count(),
            "recruits_count": Recruit.objects.count(),
        },
    )


##############################_CHARACTER_##################################
class CharacterCreate(LoginRequiredMixin, generic.CreateView):
    model = Character
    fields = "__all__"
    template_name = "LFTplatform/character/character_form.html"
    success_url = reverse_lazy("LFTplatform:character-detail")

    # form_class = ...
    def get_success_url(self):
        return reverse_lazy(
            "LFTplatform:character-detail", kwargs={"pk": self.object.pk}
        )


class CharacterListView(LoginRequiredMixin, generic.ListView):
    model = Character
    context_object_name = "character_list"
    template_name = "LFTplatform/character/character_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CharacterListView, self).get_context_data(**kwargs)
        context["search_form"] = CharacterSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super(CharacterListView, self).get_queryset()
        form = CharacterSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                nickname__icontains=form.cleaned_data["name"])
        return queryset


class CharacterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Character
    template_name = "LFTplatform/character/character_detail.html"
    # queryset = Driver.objects.all().prefetch_related()


class CharacterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Character
    fields = ["nickname", "class_spec_combination", "item_lvl", "wcl_show",
              "wcl"]
    template_name = "LFTplatform/character/character_form.html"

    # form_class = ...
    def get_success_url(self):
        return reverse_lazy(
            "LFTplatform:character-detail", kwargs={"pk": self.object.pk}
        )


class CharacterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Character
    template_name = "LFTplatform/character/character_confirm_delete.html"
    success_url = reverse_lazy("LFTplatform:character-list")


##############################_RECRUIT___##################################
# pass
##############################_GUILD_____##################################


class GuildCreateView(LoginRequiredMixin, generic.CreateView):
    model = Guild
    fields = "__all__"
    template_name = "LFTplatform/guild/guild_form.html"
    success_url = reverse_lazy("LFTplatform:guild-detail")

    def get_success_url(self):
        return reverse_lazy("LFTplatform:guild-detail",
                            kwargs={"pk": self.object.pk})


class GuildListView(LoginRequiredMixin, generic.ListView):
    model = Guild
    context_object_name = "guild_list"
    template_name = "LFTplatform/guild/guild_list.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_data = {
            "faction": "Any",
            "activity_time_start_hour": "00:00",
            "activity_time_end_hour": "00:00",
            "selected_days": [day[0] for day in ActivityDay.DAY_CHOICES],
            "raid_team_size": [team_size[0] for team_size in
                               Team.TEAM_SIZE_CHOICES],
            "loot_system": [loot_system[0] for loot_system in
                            Team.LOOT_SYSTEM_CHOICES],
        }
        form = GuildFilterForm(data=self.request.GET or None,
                               initial=initial_data)
        context["filter_form"] = form

        prefetch_teams = Prefetch(
            "teams",
            queryset=Team.objects.prefetch_related(
                "looking_for")
        )

        guilds = context["guild_list"].prefetch_related(prefetch_teams)

        required_specs = {}
        for guild in guilds:
            specs = set()
            for team in guild.teams.all():
                for spec in team.looking_for.all():
                    specs.add((spec.class_name, spec.spec_name))
            required_specs[guild.pk] = specs
        context["required_specs"] = required_specs

        context["selected_specs"] = self.request.GET.getlist("specific_specs")
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        faction_filter = self.request.GET.get("faction")
        activity_time_start_filter = self.request.GET.get(
            "activity_time_start_ho ur")
        activity_time_end_filter = self.request.GET.get(
            "activity_time_end_hour")
        selected_days_filter = self.request.GET.getlist("selected_days")
        selected_team_sizes = self.request.GET.getlist("raid_team_size")
        selected_loot_systems = self.request.GET.getlist("loot_system")
        selected_classes = self.request.GET.getlist(
            "class_spec_combinations"
        )
        selected_specs = self.request.GET.getlist("specific_specs")

        if activity_time_start_filter == activity_time_end_filter:
            activity_time_start_filter, activity_time_end_filter = None, None

        if faction_filter and faction_filter != "Any":
            queryset = queryset.filter(faction=faction_filter).distinct()

        if activity_time_start_filter is not None:
            time_hour, time_minute = map(int,
                                         activity_time_start_filter.split(":"))
            rt_start = time(hour=time_hour, minute=time_minute)

            time_hour, time_minute = map(int,
                                         activity_time_end_filter.split(":"))
            rt_end = time(hour=time_hour, minute=time_minute)

            if rt_end < rt_start:
                queryset = queryset.filter(
                    (
                            Q(teams__activity_sessions__time_start__lte=rt_end)
                            | Q(
                        teams__activity_sessions__time_start__gte=rt_start)
                    )
                    & (
                            Q(teams__activity_sessions__time_end__lte=rt_end)
                            | Q(
                        teams__activity_sessions__time_end__gte=rt_start)
                    )
                ).distinct()
            else:
                queryset = queryset.filter(
                    teams__activity_sessions__time_start__lte=rt_end,
                    teams__activity_sessions__time_end__gte=rt_start,
                ).distinct()

        if selected_days_filter and len(selected_days_filter) != 7:
            queryset = queryset.filter(
                teams__activity_sessions__day__day_of_week__in=selected_days_filter
            ).distinct()

        if selected_team_sizes:
            queryset = queryset.filter(
                teams__team_size__in=selected_team_sizes
            ).distinct()

        if selected_loot_systems:
            if len(selected_loot_systems) != len(Team.LOOT_SYSTEM_CHOICES):
                queryset = queryset.filter(
                    teams__loot_system__in=selected_loot_systems
                ).distinct()
                print(queryset)

        for key, value in self.request.GET.items():  # TODO: DELETE
            print(f"Parameter: {key}, Value: {value}")
        print(queryset)
        return queryset


class GuildDetailView(LoginRequiredMixin, generic.DetailView):
    model = Guild
    template_name = "LFTplatform/guild/guild_detail.html"
    queryset = Guild.objects.all().prefetch_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["required_specs"] = []
        for team in self.get_object().teams.all():
            for required_class_spec in team.looking_for.all():
                if str(required_class_spec) not in context["required_specs"]:
                    context["required_specs"].append(str(required_class_spec))
        return context


class GuildUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Guild
    fields = "__all__"
    template_name = "LFTplatform/guild/guild_form.html"
    success_url = reverse_lazy("LFTplatform:guild-detail")

    def get_success_url(self):
        return reverse_lazy("LFTplatform:guild-detail",
                            kwargs={"pk": self.object.pk})


class GuildDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Guild
    template_name = "LFTplatform/guild/guild_confirm_delete.html"
    success_url = reverse_lazy("LFTplatform:guild-list")


##############################_TEAM______##################################


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    template_name = "LFTplatform/team/team_form.html"

    # form_class = ...
    def get_success_url(self):
        return reverse_lazy("LFTplatform:team-detail",
                            kwargs={"pk": self.object.pk})


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "team_list"
    template_name = "LFTplatform/team/team_list.html"
    paginate_by = 10


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = "LFTplatform/team/team_detail.html"


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    template_name = "LFTplatform/team/team_form.html"

    def get_success_url(self):
        return reverse_lazy("LFTplatform:team-detail",
                            kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    template_name = "LFTplatform/team/team_confirm_delete.html"
    success_url = reverse_lazy("LFTplatform:team-list")
