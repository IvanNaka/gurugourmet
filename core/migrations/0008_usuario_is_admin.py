# Generated by Django 5.0.3 on 2024-05-22 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_equipamentoreceita_equipamento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]