# Generated by Django 3.2 on 2023-01-25 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
