# Generated by Django 5.0.4 on 2024-05-22 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=15, unique=True, verbose_name='Usuario')),
                ('user_temp', models.BooleanField(default=True)),
                ('user_active', models.BooleanField(default=True)),
                ('user_admin', models.BooleanField(default=False)),
                ('apellido', models.CharField(blank=True, max_length=20, null=True, verbose_name='Apellido')),
                ('nombres', models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombre')),
                ('medico', models.BooleanField(default=False)),
                ('dni', models.IntegerField(blank=True, null=True, verbose_name='DNI')),
                ('tipo_matricula', models.CharField(blank=True, choices=[(1, 'M.N.'), (2, 'M.P.')], max_length=2, null=True, verbose_name='Matrícula')),
                ('matricula', models.CharField(blank=True, max_length=10, null=True, verbose_name='Número')),
                ('especialidad', models.CharField(blank=True, max_length=20, null=True, verbose_name='Especialidad')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('mail', models.EmailField(blank=True, max_length=25, null=True, verbose_name='Correo Electrónico')),
                ('foto', models.ImageField(null=True, upload_to='perfiles/', verbose_name='Foto de perfil')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
