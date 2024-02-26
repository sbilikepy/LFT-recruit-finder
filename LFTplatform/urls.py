from django.urls import path

from .views import *

app_name = "LFTplatform"
urlpatterns = [
    path("", index, name="index"),
    ##############################_CHARACTER___###############################
    path(  # Crud
        "characters/create/", CharacterCreate.as_view(), name="character-create"
    ),
    path(  # cRud
        "characters/", CharacterListView.as_view(), name="character-list"
    ),  # cRud
    path(  # cRud
        "characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"
    ),
    path(  # crUd
        "characters/<int:pk>/update/",
        CharacterUpdate.as_view(),
        name="character-update",
    ),
    path(  # cruD
        "characters/<int:pk>/delete/",
        CharacterDelete.as_view(),
        name="character-delete",
    ),
    ##############################_RECRUIT___##################################
    ##############################_GUILD_____##################################
    path("guilds/create/", GuildCreateView.as_view(), name="guild-create"),  # Crud
    path("guilds/", GuildListView.as_view(), name="guild-list"),  # cRud
    path("guilds/<int:pk>/", GuildDetailView.as_view(), name="guild-detail"),  # cRud
    # path(  # CRUD
    #         "/",
    #         .as_view(),
    #         name=""
    #     ),
    ##############################_TEAM______##################################
]
