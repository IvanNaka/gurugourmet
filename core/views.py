import datetime
import json

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django import forms
from django.views.generic import TemplateView

from core.models import Usuario, Receita, Ingrediente, IngredienteReceita, Comentario, DenunciaComentario, BanImagem, \
    BanUsuario


class HomeView(View):
    def get(self, request, **kwargs):
        user = self.request.session.get('username')
        if user:
            is_admin = Usuario.objects.filter(username=user).first().is_admin
        else:
            is_admin = False
        lista_receitas = Receita.objects.filter(status=True).all()[:6]
        lista_ingredientes = Ingrediente.objects.order_by('nome').all()
        context = {
            'lista_receitas': lista_receitas,
            'lista_ingredientes': lista_ingredientes,
            'username': user,
            'is_admin': is_admin,
        }
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
        if usuario:
            user = authenticate(request, username=usuario.email, password=senha)
            is_admin = authenticate(request, is_admin=usuario.is_admin, null=True)
            if user:
                login(request, user)
                request.session['username'] = usuario.username
                return JsonResponse({'success': True, 'admin': is_admin})
            else:
                return JsonResponse({'error': 'Usuário ou senha inválido!'}, status=401)

        return JsonResponse({'error': 'Usuário não encontrado!'}, status=404)

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
        comentarios = Comentario.objects.filter(receita=receita, status=True)
        username_usuario = self.request.user.username
        username_receita = receita.usuario.username
        is_criador = username_usuario == username_receita
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        context = {
            "receita": receita,
            "listaIngredientes": listaIngredientes,
            "comentarios": comentarios,
            "is_criador": is_criador,
            "is_admin": is_admin
        }
        return render(self.request, "receitas.html", context)


    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para comentar.')
            return render(request, "login.html")
            #return redirect('login')

        receita_id = kwargs.get('receita_id')
        receita = get_object_or_404(Receita, id=receita_id)
        texto = request.POST.get('texto')
        listaIngredientes = list(IngredienteReceita.objects.filter(receita_id=receita_id))
        comentarios = Comentario.objects.filter(receita=receita, status=True)
        context = {
            "receita": receita,
            "listaIngredientes": listaIngredientes,
            "comentarios": comentarios,
        }

        if texto:
            usuario = Usuario.objects.get(userDjango=request.user)

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
        return render(self.request, "receitas.html", context)
        #return redirect('receita', receita_id=receita.id)

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
        receita = Receita.objects.filter(id=receita_id).first()
        username_usuario = self.request.user.username
        username_receita = receita.usuario.username
        is_criador = username_usuario == username_receita
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        receita_id = kwargs.get('receita_id')
        if is_criador or is_admin:
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
class DenunciarComentarioView(View):
    def get(self, request, **kwargs):
        return render(self.request, "denunciar.html")
    @method_decorator(login_required)
    def post(self, request, comentario_id):
        comentario = get_object_or_404(Comentario, id=comentario_id)
        usuario = request.user
        motivo = request.POST.get('motivo')
        denuncia = DenunciaComentario(comentario=comentario, usuario=usuario, motivo=motivo)
        denuncia.save()
        context = {
            'receita_id': comentario.receita.id,
        }
        response = render(request, 'denunciar.html', context)
        messages.success(request, 'Denúncia registrada com sucesso.')
        return response


class PaginaAdmView(View):
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        user = self.request.session.get('username')
        usuario = Usuario.objects.filter(username=user).first()
        is_admin = usuario.is_admin if usuario else False
        if is_admin:
            usuarios = Usuario.objects.all()
            denuncias = DenunciaComentario.objects.all()  # Busca todas as denúncias
            context = {
                'username': user,
                'is_admin': is_admin,
                'usuarios': usuarios,
                'denuncias': denuncias,  # Adiciona as denúncias ao contexto
            }
            return render(self.request, 'pagina_adm.html', context)
        else:
            return render(request, 'index.html')


class ConfirmarDeleteView(View):
    def get(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        receita = Receita.objects.filter(id=receita_id).first()
        username_usuario = self.request.user.username
        username_receita = receita.usuario.username
        is_criador = username_usuario == username_receita
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        context = {
            "receita": receita,
        }
        if not (is_criador or is_admin):
            return redirect('/')
        return render(self.request, "deletar_receita.html", context)

    def post(self, request, **kwargs):
        receita_id = kwargs.get('receita_id')
        receita = Receita.objects.filter(id=receita_id).first()
        username_usuario = self.request.user.username
        username_receita = receita.usuario.username
        is_criador = username_usuario == username_receita
        context = {
            "receita": receita,
        }
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        receita_id = kwargs.get('receita_id')
        if is_criador or is_admin:
            DenunciaComentario.objects.filter(comentario__receita=receita_id).delete()
            Comentario.objects.filter(receita_id=receita_id).delete()
            IngredienteReceita.objects.filter(receita_id=receita_id).delete()
            Receita.objects.filter(id=receita_id).delete()
        messages.success(request, 'Receita apagada com sucesso!')
        return render(request, 'deletar_receita.html', context)

class DeleteUsuarioView(View):
    def get(self, request, **kwargs):
        usuario_id = kwargs.get('usuario_id')
        usuario = Usuario.objects.filter(id=usuario_id).first()
        username_usuario = self.request.user.username
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        context = {
            "usuario": usuario,
        }
        if not is_admin:
            return redirect('/')
        return render(self.request, "deletar_usuario.html", context)

    def post(self, request, **kwargs):
        usuario_id = kwargs.get('usuario_id')
        usuario = Usuario.objects.filter(id=usuario_id).first()
        username_usuario = self.request.user.username
        context = {
            "usuario_id": usuario_id,
        }
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        if is_admin:
            usuario.delete()
        messages.success(request, 'Usuario apagado com sucesso!')
        return render(request, 'deletar_usuario.html', context)

class DeleteComentarioView(View):
    def get(self, request, **kwargs):
        comentario_id = kwargs.get('comentario_id')
        comentario = Comentario.objects.filter(id=comentario_id).first()
        username_usuario = self.request.user.username
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        context = {
            "comentario": comentario,
        }
        if not is_admin:
            return redirect('/')
        return render(self.request, "deletar_comentario.html", context)

    def post(self, request, **kwargs):
        comentario_id = kwargs.get('comentario_id')
        comentario = Comentario.objects.filter(id=comentario_id).first()
        username_usuario = self.request.user.username
        context = {
            "comentario_id": comentario_id,
        }
        if username_usuario:
            is_admin = Usuario.objects.filter(username=username_usuario).first().is_admin
        else:
            is_admin = False
        if is_admin:
            comentario.delete()
        messages.success(request, 'Comentário apagado com sucesso!')
        return render(request, 'deletar_comentario.html', context)

class LogoutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('/')