# Generated by Django 5.0.3 on 2024-06-12 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_usuario_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='custo_medio',
            field=models.CharField(max_length=255, null=True),
        ),
    ]