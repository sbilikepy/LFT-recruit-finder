from django.urls import path

from .views import *

app_name = "LFTplatform"
urlpatterns = [
    path("", index, name="index"),
    ##############################_CHARACTER___###############################
    path(  # Crud
        "characters/create/", CharacterCreate.as_view(),
        name="character-create"
    ),
    path(  # cRud
        "characters/", CharacterListView.as_view(), name="character-list"
    ),  # cRud
    path(  # cRud
        "characters/<int:pk>/", CharacterDetailView.as_view(),
        name="character-detail"
    ),
    path(  # crUd
        "characters/<int:pk>/update/",
        CharacterUpdateView.as_view(),
        name="character-update",
    ),
    path(  # cruD
        "characters/<int:pk>/delete/",
        CharacterDeleteView.as_view(),
        name="character-delete",
    ),
    ##############################_RECRUIT___##################################
    ##############################_GUILD_____##################################
    path("guilds/create/", GuildCreateView.as_view(), name="guild-create"),
    # Crud
    path("guilds/", GuildListView.as_view(), name="guild-list"),  # cRud
    path("guilds/<int:pk>/", GuildDetailView.as_view(), name="guild-detail"),
    # cRud
    path(  # crUd
        "guilds/<int:pk>/update/",
        GuildUpdateView.as_view(),
        name="guild-update",
    ),
    path(  # cruD
        "guilds/<int:pk>/delete/",
        GuildDeleteView.as_view(),
        name="guild-delete",
    ),
    ##############################_TEAM______##################################
    path(  # Crud
        "teams/create/",
        TeamCreateView.as_view(),
        name="team-create"
    ),
    path(  # cRud
        "teams/",
        TeamListView.as_view(),
        name="team-list"
    ),  # cRud
    path(  # cRud
        "teams/<int:pk>/",
        TeamDetailView.as_view(),
        name="team-detail"
    ),
    path(  # crUd
        "teams/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name="team-update",
    ),
    path(  # cruD
        "teams/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name="team-delete",
    ),
]
