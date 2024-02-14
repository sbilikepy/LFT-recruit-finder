from django.urls import path

from .views import *

app_name = "LFTplatform"
urlpatterns = [
    path("", index, name="index"),

    path("recruits/", RecruitListView.as_view(), name="recruit-list"),
    path("recruits/<int:pk>/", RecruitDetailView.as_view(),
         name="recruit-detail"),
]
