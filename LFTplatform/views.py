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
class CharacterCreate(LoginRequiredMixin, generic.CreateView):
    model = Character
    fields = "__all__"
    success_url = reverse_lazy("LFTplatform:character-list")
    # form_class = ...


class CharacterListView(LoginRequiredMixin, generic.ListView):
    model = Character
    context_object_name = "character_list"
    template_name = "LFTplatform/recruit_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CharacterListView, self).get_context_data(**kwargs)
        context["search_form"] = CharacterSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super(CharacterListView, self).get_queryset()
        form = CharacterSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(nickname__icontains=form.cleaned_data["name"])
        return queryset


class CharacterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Character
    # queryset = Driver.objects.all().prefetch_related()


class CharacterUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Character
    fields = "__all__"
    success_url = reverse_lazy("LFTplatform:character-list")
    # form_class = ...


class CharacterDelete(LoginRequiredMixin, generic.DeleteView):
    model = Recruit
    success_url = reverse_lazy("LFTplatform:character-list")
##############################_CHARACTER_##################################
##############################_GUILD_____##################################
##############################_TEAM______##################################
