# Generated by Django 5.0.3 on 2024-06-06 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_usuario_instagram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='instagram',
            field=models.CharField(max_length=128),
        ),
    ]