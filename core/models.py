from django.db import models

# Create your models here.

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    senha = models.CharField()
class Receita(models.Model):
    texto = models.TextField()
    data_criacao = models.DateTimeField()
    status = models.BooleanField()
    idUsuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

class Ingrediente(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)

class Equipamento(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)

class Administrador(models.Model):
    username = models.CharField(max_length=100)
    senha = models.CharField()