# Generated by Django 5.0.3 on 2024-05-30 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_usuario_senha_usuario_instagram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='instagram',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
