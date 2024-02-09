from django.http import HttpResponse


# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django.views import generic
# from models import *
# from .forms import *

def index(request):
    """View function for the home page of the site."""
    return HttpResponse(":)")
