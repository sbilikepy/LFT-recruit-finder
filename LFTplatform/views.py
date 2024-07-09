import os

import dotenv
import requests
from dotenv import load_dotenv

from datetime import time
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Prefetch
from django.db.models import Q

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import redirect

from .forms import *
from .models import *
from .services import *

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)


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
        form = CharacterSearchForm(self.request.GET)  # TODO: am i need s.form?
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


class GuildListView(generic.ListView):
    model = Guild
    context_object_name = "guild_list"
    template_name = "LFTplatform/guild/guild_list.html"
    paginate_by = 20

    filtered_teams = None

    # all guilds = 708
    #   r1a = 347
    #   r2h = 361
    # _____________________________

    # @time_decorator
    def get_context_data(self, **kwargs):
        # print("console get_context_data trigger")
        context = super().get_context_data(**kwargs)
        context['guild_count'] = self.get_queryset().count()
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
            "teams", queryset=Team.objects.prefetch_related("looking_for")
        )
        guilds = context["guild_list"]
        # guilds = context["guild_list"].prefetch_related(prefetch_teams)

        required_specs = {}
        for guild in guilds:
            specs = set()
            for team in guild.teams.all():
                for spec in team.looking_for.all():
                    specs.add((spec.class_name, spec.spec_name))
            required_specs[guild.pk] = specs
        context["required_specs"] = required_specs

        context["selected_specs"] = self.request.GET.getlist("specific_specs")
        context["filtered_teams_queryset"] = self.filtered_teams
        return context

    @time_decorator
    def get_queryset(self):
        # print("console get_queryset trigger")
        queryset = super().get_queryset()
        faction_filter = self.request.GET.get("faction")
        activity_time_start_filter = self.request.GET.get(
            "activity_time_start_hour")
        activity_time_end_filter = self.request.GET.get(
            "activity_time_end_hour")
        selected_days_filter = self.request.GET.getlist("selected_days")
        selected_team_sizes = self.request.GET.getlist("raid_team_size")
        selected_loot_systems = self.request.GET.getlist("loot_system")
        selected_classes = self.request.GET.getlist(
            "class_spec_combinations"
        )
        selected_specs = self.request.GET.getlist("specific_specs")

        # Root: faction -> days -> sizes ->  LS -> class ->spec -> time

        #############       FACTION           #######        +++++++++
        if faction_filter and faction_filter != "Any":
            queryset = faction_filter_queryset(
                queryset, faction_filter
            )

        #############       selected_days_filter           #######  +++++++
        if selected_days_filter and len(selected_days_filter) != 7:
            queryset = selected_days_filter_queryset(
                queryset, selected_days_filter
            )

        #############       selected_team_sizes           ###########  ++++
        if selected_team_sizes:
            queryset = selected_team_sizes_filter_queryset(
                queryset, selected_team_sizes
            )

        #############       selected_loot_systems           ######   ++++++
        if selected_loot_systems:
            if len(selected_loot_systems) != len(Team.LOOT_SYSTEM_CHOICES):
                queryset = selected_loot_systems_filter_queryset(
                    queryset, selected_loot_systems
                )
        #############       selected_classes           ##################

        if selected_classes:
            queryset = selected_classes_filter_queryset(
                queryset, selected_classes
            )

        #############       selected_specs           ##################
        if selected_specs:
            queryset = selected_specs_filter_queryset(
                queryset, selected_specs
            )

        ####   activity_time_start_filter 00:00 - 00:00  or 0m duration   ####
        if activity_time_start_filter != activity_time_end_filter:
            queryset, self.filtered_teams = activity_time_filter_queryset(
                queryset,
                selected_days_filter,
                activity_time_start_filter,
                activity_time_end_filter
            )


        ######################################################################
        ######################################################################
        ######################################################################
        # for key, value in self.request.GET.items():
        #     print(f"Parameter: {key}, Value: {value}")
        #     if key == "selected_days":
        #         print([i for i in value])
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


###################____________USER________________###########################

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "LFTplatform/user/user_detail.html"


####################__________DISCORD_LOGIN________############################


def discord_oauth2_authentication(request: HttpRequest):
    """
    https://discord.com/developers/docs/topics/oauth2
    OAuth2 link -> urls -> this view - > redirect to auth app
    :param request:
    :return:
    """
    generated_url = os.getenv("GENERATED_URL")
    return redirect(generated_url)


def discord_authorization(request: HttpRequest):
    """
    link -> discord_login view -> discord oauth2 -> this view ->
    :param request:
    :return:
    """
    code = request.GET.get("code")
    user_data = exchange_code(code)

    if user_data:
        discord_id = user_data['user_data_for_authorization']['id']
        print(discord_id)
        try:
            current_user = User.objects.get(discord_id=discord_id)
            current_user.username = user_data['user_data_for_authorization'][
                'username']
            current_user.email = user_data['user_data_for_authorization'].get(
                "email", None)
            current_user.avatar = user_data['user_data_for_authorization'][
                "avatar"]

            current_user.public_server_name = \
                user_data['user_data_for_authorization']["global_name"]

            current_user.recruiter_role = user_data["recruiter_role"]
            current_user.save()



        except User.DoesNotExist:

            current_user = User.objects.create(
                username=user_data['user_data_for_authorization']['username'],
                email=user_data['user_data_for_authorization'].get(
                    "email", None
                ),
                discord_id=discord_id,
                avatar=user_data['user_data_for_authorization']["avatar"],
                public_server_name=user_data['user_data_for_authorization'][
                    "global_name"],
                recruiter_role=user_data["recruiter_role"],
            )

        login(request, user=current_user)

        return redirect(
            reverse(
                'LFTplatform:user-detail', kwargs={'pk': current_user.pk}
            )
        )

    return JsonResponse({"error": "Failed to authenticate."}, status=400)
    # return JsonResponse(user)


def exchange_code(code: str):
    """
    Exchanges the OAuth2 code for user data.
    :param code:
    :return:
    """
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    pwv_server_id = os.getenv("PWV_SERVER_ID")

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": "identify guilds guilds.members.read"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers,
        auth=(client_id, client_secret)
    )

    if response.status_code == 200:
        credentials = response.json()
        access_token = credentials.get('access_token')

        # User
        user_response = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": 'Bearer %s' % access_token}
        )
        # all servers
        guilds_response = requests.get(
            "https://discord.com/api/v10/users/@me/guilds",
            headers={"Authorization": 'Bearer %s' % access_token}
        )
        # PWV server
        server_member_response = requests.get(
            f"https://discord.com/api/v10/users/@me/guilds/"
            f"{pwv_server_id}/member",
            headers={"Authorization": 'Bearer %s' % access_token}
        )
        if server_member_response.status_code == 200:
            recruiter_role = os.getenv(
                'RECRUITER_ROLE_ID') in server_member_response.json().get(
                "roles", [])
        else:
            recruiter_role = False

        response_data = {
            "user_data_for_authorization": user_response.json(),
            "recruiter_role": recruiter_role,
            "TEMP_DATA": [credentials, server_member_response.json()]
        }
        return response_data
    else:
        return None
