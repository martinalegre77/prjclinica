# Generated by Django 5.0.4 on 2024-06-20 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_usuario_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='foto',
        ),
        migrations.AddField(
            model_name='usuario',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Foto de perfil'),
        ),
    ]