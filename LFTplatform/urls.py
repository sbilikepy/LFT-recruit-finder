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
        "recruits/create/",
        RecruitCreate.as_view(),
        name="recruit-create"
    ),
    # Crud
    path(
        "recruits/",
        RecruitListView.as_view(),
        name="recruit-list"),  # cRud
    path(  # cRud
        "recruits/<int:pk>/",
        RecruitDetailView.as_view(),
        name="recruit-detail"
    ),
    path(  # crUd
        "recruits/<int:pk>/update/",
        RecruitUpdate.as_view(),
        name="recruit-update"
    ),
    path(  # cruD
        "recruits/<int:pk>/delete/",
        RecruitDelete.as_view(),
        name="recruit-delete"
    ),
    ##############################_CHARACTER_##################################
    ##############################_GUILD_____##################################
    ##############################_TEAM______##################################
]
