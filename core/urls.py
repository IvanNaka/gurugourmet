"""
URL configuration for GuruGourmet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from GuruGourmet import settings
from core import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('login/', csrf_exempt(views.LoginView.as_view())),
    path('cadastro/', csrf_exempt(views.CadastroView.as_view())),
    path('receita/<int:receita_id>', csrf_exempt(views.ReceitaView.as_view())),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
