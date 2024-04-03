from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django import forms
from django.views.generic import TemplateView

from core.models import Usuario


class HomeView(View):
    def get(self, request, **kwargs):
        return render(self.request, "index.html")

class LoginForm(forms.Form):
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
class LoginView(View):
    def get(self, request, **kwargs):
        return render(self.request, "login.html")
    def post(self, request, **kwargs):
        email = self.request.POST.get('email')
        senha = self.request.POST.get('password')
        is_valido = Usuario.objects.filter(email=email, senha=senha).exists()
        if is_valido:
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Usuario ou senha invalido!'}, status=400)

class CadastroView(View):
    def get(self, request, **kwargs):
        return render(self.request, "register.html")
    def post(self, request, **kwargs):

        return render(self.request, "login.html")
