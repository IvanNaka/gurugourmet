from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    instagram = models.CharField(max_length=128, null=True)
    userDjango = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    is_admin = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    senha = models.CharField(max_length=128)

class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    numero = models.IntegerField()
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    cep = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)


class Receita(models.Model):
    texto = models.TextField()
    titulo = models.CharField(max_length=255, default='')
    data_criacao = models.DateTimeField()
    status = models.BooleanField()
    tempo_preparo = models.CharField(max_length=255, null=True)
    imagem_principal = models.FileField(max_length=255, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

class Ingrediente(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)

class IngredienteReceita(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.DO_NOTHING)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.DO_NOTHING)
    quantidade = models.DecimalField(max_digits=20, decimal_places=2)
    unidadeMedida = models.CharField(max_length=10)

class Imagem(models.Model):
    status = models.BooleanField()
    receita = models.ForeignKey(Receita, on_delete=models.DO_NOTHING)
    path = models.FileField()

class Comentario(models.Model):
    status = models.BooleanField()
    receita = models.ForeignKey(Receita, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    texto = models.TextField()

class BanReceita(models.Model):
    status = models.BooleanField()
    receita = models.ForeignKey(Receita, on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    justificativa = models.TextField()

class BanComentario(models.Model):
    status = models.BooleanField()
    comentario = models.ForeignKey(Comentario, on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    justificativa = models.TextField()

class BanImagem(models.Model):
    status = models.BooleanField()
    imagem = models.ForeignKey(Imagem, on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    justificativa = models.TextField()

class BanUsuario(models.Model):
    status = models.BooleanField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    justificativa = models.TextField()

class DenunciaComentario(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Denuncia feita por {self.usuario.username} no comentário {self.comentario.id}'