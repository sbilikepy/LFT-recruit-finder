# from django.http import HttpResponse

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# from django.urls import reverse_lazy
from django.views import generic

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


class RecruitListView(LoginRequiredMixin, generic.ListView):
    model = Recruit
    context_object_name = "recruit_list"
    template_name = "LFTplatform/recruit_list.html"
    paginate_by = 5


class RecruitDetailView(LoginRequiredMixin, generic.ListView):
    model = Recruit
