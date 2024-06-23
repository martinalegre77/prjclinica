# Generated by Django 5.0.4 on 2024-06-22 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_usuario_tipo_matricula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_matricula',
            field=models.CharField(blank=True, choices=[('1', 'M.N.'), ('2', 'M.P.')], max_length=4, null=True, verbose_name='Matrícula'),
        ),
    ]