# from django.http import HttpResponse

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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


##############################_RECRUIT___##################################
class RecruitCreate(LoginRequiredMixin, generic.CreateView):
    model = Recruit
    fields = "__all__"
    success_url = reverse_lazy("LFTplatform:recruit-list")
    # form_class = ...


class RecruitListView(LoginRequiredMixin, generic.ListView):
    model = Recruit
    context_object_name = "recruit_list"
    template_name = "LFTplatform/recruit_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(RecruitListView, self).get_context_data(**kwargs)
        context["search_form"] = RecruitSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super(RecruitListView, self).get_queryset()
        form = RecruitSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class RecruitDetailView(LoginRequiredMixin, generic.DetailView):
    model = Recruit
    # queryset = Driver.objects.all().prefetch_related()


class RecruitUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Recruit
    fields = "__all__"
    success_url = reverse_lazy("LFTplatform:recruit-list")
    # form_class = ...


class RecruitDelete(LoginRequiredMixin, generic.DeleteView):
    model = Recruit
    success_url = reverse_lazy("LFTplatform:recruit-list")
##############################_CHARACTER_##################################
##############################_GUILD_____##################################
##############################_TEAM______##################################
