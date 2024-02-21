from django.urls import path

from .views import *

app_name = "LFTplatform"
urlpatterns = [
    path("",
         index,
         name="index"
         ),
    ##############################_RECRUIT___##################################
    path(
        "characters/create/",
        CharacterCreate.as_view(),
        name="character-create"
    ),
    # Crud
    path(
        "characters/",
        CharacterListView.as_view(),
        name="character-list"),  # cRud
    path(  # cRud
        "characters/<int:pk>/",
        CharacterDetailView.as_view(),
        name="character-detail"
    ),
    path(  # crUd
        "characters/<int:pk>/update/",
        CharacterUpdate.as_view(),
        name="character-update"
    ),
    path(  # cruD
        "characters/<int:pk>/delete/",
        CharacterDelete.as_view(),
        name="character-delete"
    ),
    ##############################_CHARACTER_##################################
    ##############################_GUILD_____##################################
    ##############################_TEAM______##################################
]
