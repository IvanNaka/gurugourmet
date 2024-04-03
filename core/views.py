from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

class HomeView(View):
    def get(self, request, **kwargs):
        return render(self.request, "index.html")


class LoginView(View):
    def get(self, request, **kwargs):
        return render(self.request, "login.html")