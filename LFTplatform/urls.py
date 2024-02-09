from django.urls import path

from .views import *

app_name = "LFTplatform"
urlpatterns = [
    path("", index, name="index"),
]
