# Generated by Django 5.0.3 on 2024-05-22 23:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_equipamentoreceita_equipamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancomentario',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.usuario'),
        ),
        migrations.RemoveField(
            model_name='banusuario',
            name='admin',
        ),
        migrations.AlterField(
            model_name='banreceita',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.usuario'),
        ),
        migrations.AlterField(
            model_name='banimagem',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.usuario'),
        ),
        migrations.DeleteModel(
            name='Administrador',
        ),
    ]