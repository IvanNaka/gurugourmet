# Generated by Django 5.0.3 on 2024-05-30 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='senha',
        ),
        migrations.AddField(
            model_name='usuario',
            name='instagram',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='usuario',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
