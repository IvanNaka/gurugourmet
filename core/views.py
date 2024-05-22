import datetime
import json

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django import forms
from django.views.generic import TemplateView

from core.models import Usuario, Receita, Ingrediente, IngredienteReceita


class HomeView(View):
    def get(self, request, **kwargs):
        user = self.request.session.get('username')
        lista_receitas = Receita.objects.filter(status=True).all()[:6]
        lista_ingredientes = Ingrediente.objects.order_by('nome').all()
        context = {}
        context['lista_receitas'] = lista_receitas
        context['lista_ingredientes'] = lista_ingredientes
        context['username'] = user

        return render(self.request, "index.html", context)


class GetIngredientesView(View):
    def get(self, request, **kwargs):
        lista_ingredientes = list(Ingrediente.objects.order_by('nome').values())
        return JsonResponse({'sucess': True, 'lista_ingredientes': lista_ingredientes})

class GetReceitasView(View):
    def post(self, request, **kwargs):
        lista_objs = []
        lista_ingredientes = json.loads(self.request.body).get('lista_ingredientes')
        lista_receitas = list(IngredienteReceita.objects.filter(ingrediente_id__in=lista_ingredientes).distinct('receita_id').values_list('receita_id', flat=True))
        lista_objs = list(Receita.objects.filter(id__in=lista_receitas).values())
        return JsonResponse({'sucess': True, 'lista_receitas': lista_objs})

class LoginView(View):
    def get(self, request, **kwargs):
        return render(self.request, "login.html")
    def post(self, request, **kwargs):
        email = self.request.POST.get('email')
        senha = self.request.POST.get('password')
        usuario = Usuario.objects.filter(email=email, senha=senha).first()
        user = authenticate(request, username=usuario.username, password=senha)
        if usuario and user:
            login(request, user)
            request.session['username'] = usuario.username
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Usuario ou senha invalido!'}, status=500)

class CadastroView(View):
    def get(self, request, **kwargs):
        return render(self.request, "register.html")
    def post(self, request, **kwargs):
        email = self.request.POST.get('email')
        senha = self.request.POST.get('password')
        username = self.request.POST.get('username')
        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Usuario ou senha invalido!'}, status=500)
        userDjango = User.objects.create_user(username, email, senha)
        login(request, userDjango)
        usuarioNovo = Usuario()
        usuarioNovo.username = username
        usuarioNovo.senha = senha
        usuarioNovo.email = email
        usuarioNovo.userDjango = userDjango
        request.session['username'] = username
        usuarioNovo.save()
        if not userDjango and not usuarioNovo:
            return JsonResponse({'error': 'Erro ao cadastrar usuário!'})
        login(request, userDjango)
        return JsonResponse({'success': True})


class ReceitaView(View):
    def get(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        receita = Receita.objects.filter(id=receita_id).first()
        listaIngredientes = list(IngredienteReceita.objects.filter(receita_id=receita_id))
        username_usuario = self.request.user.username
        username_receita = receita.usuario.username
        is_criador = username_usuario == username_receita
        context = {"receita": receita, "listaIngredientes": listaIngredientes, "is_criador": is_criador}
        return render(self.request, "receitas.html", context)

class UpdateReceitaView(View):
    def get(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        receita = Receita.objects.filter(id=receita_id).first()
        listaIngredientes = list(IngredienteReceita.objects.filter(receita_id=receita_id))
        context = {"receita": receita, "listaIngredientes": listaIngredientes}
        return render(self.request, "editar_receitas.html", context)
    def post(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        texto_novo = self.request.POST.get("texto")
        tempo_preparo_novo = self.request.POST.get("tempo_preparo")
        titulo_novo = self.request.POST.get("titulo")
        lista_ingredientes = self.request.POST.getlist("ingredientes")
        receita = Receita.objects.filter(id=receita_id).first()
        receita.texto = texto_novo
        receita.tempo_preparo = tempo_preparo_novo
        receita.titulo = titulo_novo
        receita.save()
        IngredienteReceita.objects.filter(receita_id=receita_id).delete()
        lista_obj = []
        for ingrediente_lista in lista_ingredientes:
            ingrediente = IngredienteReceita()
            ingrediente_lista = json.loads(ingrediente_lista)
            ingrediente.ingrediente_id = ingrediente_lista.get("ingrediente_id")
            ingrediente.receita_id = receita_id
            ingrediente.quantidade = ingrediente_lista.get("quantidade")
            ingrediente.unidadeMedida = ingrediente_lista.get("unidadeMedida")
            lista_obj.append(ingrediente)
        IngredienteReceita.objects.bulk_create(lista_obj)
        return redirect('/')
    def delete(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        IngredienteReceita.objects.filter(receita_id=receita_id).delete()
        Receita.objects.filter(id=receita_id).delete()
        return JsonResponse({'success': True})

class CreateReceitaView(View):
    def get(self, request, **kwargs):
        return render(self.request, "criar_receita.html")

    def post(self, request, **kwargs):
        texto_novo = self.request.POST.get("texto")
        tempo_preparo_novo = self.request.POST.get("tempo_preparo")
        titulo_novo = self.request.POST.get("titulo")
        lista_ingredientes = self.request.POST.getlist("ingredientes")
        receita = Receita()
        if 'image' in self.request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_path = fs.url(filename)
            receita.imagem_principal = image_path
        else:
            receita.imagem_principal = ''
        receita.texto = texto_novo
        receita.tempo_preparo = tempo_preparo_novo
        receita.titulo = titulo_novo
        receita.usuario_id = titulo_novo
        receita.status = True
        receita.data_criacao = datetime.datetime.now()
        receita.usuario_id = Usuario.objects.filter(email=self.request.user.email).first().id
        receita.save()
        lista_obj = []
        for ingrediente_lista in lista_ingredientes:
            ingrediente = IngredienteReceita()
            ingrediente_lista = json.loads(ingrediente_lista)
            ingrediente.ingrediente_id = ingrediente_lista.get("ingrediente_id")
            ingrediente.receita_id = receita.id
            ingrediente.quantidade = ingrediente_lista.get("quantidade")
            ingrediente.unidadeMedida = ingrediente_lista.get("unidadeMedida")
            lista_obj.append(ingrediente)
        IngredienteReceita.objects.bulk_create(lista_obj)
        return redirect('/')

class LogoutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('/')