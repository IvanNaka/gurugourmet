# Generated by Django 5.0.3 on 2024-06-02 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_usuario_senha'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='senha',
            field=models.CharField(max_length=255, null=True),
        ),
    ]