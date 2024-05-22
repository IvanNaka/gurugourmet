from datetime import timezone

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django import forms
from django.views.generic import TemplateView
from django.contrib import messages
from pyexpat.errors import messages
from django.utils import timezone
from core.models import Usuario, Receita, Ingrediente, IngredienteReceita, Comentario


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
        user = self.request.session.get('username')
        lista_receitas = Receita.objects.filter(status=True).all()[:6]
        lista_ingredientes = Ingrediente.objects.order_by('nome').all()
        context = {}
        context['lista_receitas'] = lista_receitas
        context['lista_ingredientes'] = lista_ingredientes
        context['user'] = user

        return render(self.request, "index.html", context)

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
        context = {"receita": receita, "listaIngredientes": listaIngredientes}
        print(listaIngredientes)
        return render(self.request, "receitas.html", context)

    def get(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        receita = Receita.objects.filter(id=receita_id).first()
        listaIngredientes = list(IngredienteReceita.objects.filter(receita_id=receita_id))
        comentarios = Comentario.objects.filter(receita=receita, status=True)
        context = {
            "receita": receita,
            "listaIngredientes": listaIngredientes,
            "comentarios": comentarios
        }
        return render(request, "receitas.html", context)

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para comentar.')
            return redirect('login')

        receita_id = kwargs.get('receita_id')
        receita = get_object_or_404(Receita, id=receita_id)
        texto = request.POST.get('texto')

        if texto:
            usuario = Usuario.objects.get(id=request.user.id)

            Comentario.objects.create(
                status=True,  # ou False, dependendo da sua lógica de aprovação
                receita=receita,
                usuario=usuario,
                data=timezone.now(),
                texto=texto
            )
            messages.success(request, 'Seu comentário foi adicionado com sucesso.')
        else:
            messages.error(request, 'O texto do comentário não pode estar vazio.')

        return redirect('receitas', receita_id=receita.id)

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
        receita = Receita.objects.filter(id=receita_id)
        receita.texto = texto_novo
        receita.tempo_preparo = tempo_preparo_novo
        receita.titulo = titulo_novo
        receita.save()
        IngredienteReceita.objects.filter(receita_id=receita_id).delete()
        for ingrediente_lista in lista_ingredientes:
            ingrediente = IngredienteReceita()
            ingrediente.ingrediente_id = ingrediente_lista.get("ingrediente_id")
            ingrediente.receita_id = receita_id
            ingrediente.quantidade_id = ingrediente_lista.get("quantidade_id")
            ingrediente.unidade_medida = ingrediente_lista.get("unidade_medida_id")
            ingrediente.save()

        return JsonResponse({'success': True})
    def delete(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        IngredienteReceita.objects.filter(receita_id=receita_id).delete()
        Receita.objects.filter(receita_id=receita_id).delete()
        return JsonResponse({'success': True})

class CreateReceitaView(View):
    def get(self, request, **kwargs):
        context = {}
        return render(self.request, "register.html")