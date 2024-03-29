# Generated by Django 3.2 on 2023-01-25 12:16

import users.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[users.validator.username_value_not_me], verbose_name='Ник пользователя'),
        ),
    ]
