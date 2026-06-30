from django.shortcuts import render
from apps.common.views import HomeView


def home(request):
    return render(request, "pages/index.html")