# Generated by Django 3.2 on 2022-12-22 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='841732', max_length=255, null=True, verbose_name='Код подтверждения'),
        ),
    ]
