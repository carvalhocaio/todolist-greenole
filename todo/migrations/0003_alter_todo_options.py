# Generated by Django 4.2.7 on 2023-11-10 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todo_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['id'], 'verbose_name': 'ToDo', 'verbose_name_plural': 'ToDos'},
        ),
    ]
