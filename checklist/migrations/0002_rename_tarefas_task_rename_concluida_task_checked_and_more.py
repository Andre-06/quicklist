# Generated by Django 4.1.7 on 2024-02-02 12:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tarefas',
            new_name='Task',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='concluida',
            new_name='checked',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='descricao',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='usuario_id',
            new_name='id_user',
        ),
    ]
