# Generated by Django 5.0.4 on 2024-06-24 02:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_usuario_tipo_matricula'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apto',
            name='id_familiares',
        ),
        migrations.RemoveField(
            model_name='apto',
            name='id_personales',
        ),
        migrations.RemoveField(
            model_name='apto',
            name='id_deportista',
        ),
        migrations.RemoveField(
            model_name='apto',
            name='id_examen',
        ),
        migrations.RemoveField(
            model_name='apto',
            name='id_usuario',
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fam_cardiovasculares', models.BooleanField(default=False, verbose_name='Cardiovasculares')),
                ('fam_cardiovasculares_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('fam_neurologicas', models.BooleanField(default=False, verbose_name='Neurológicas')),
                ('fam_neurologicas_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('fam_tumorales', models.BooleanField(default=False, verbose_name='Tumorales')),
                ('fam_tumorales_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('fam_respiratorias', models.BooleanField(default=False, verbose_name='Respiratorias')),
                ('fam_respiratorias_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('fam_desangre', models.BooleanField(default=False, verbose_name='De la sangre')),
                ('fam_desangre_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('fam_otras', models.BooleanField(blank=True, default=False, null=True, verbose_name='Otras')),
                ('fam_otras_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('fam_obs', models.TextField(blank=True, null=True)),
                ('per_cardiologica', models.BooleanField(default=False, verbose_name='Cardiológicas')),
                ('per_cardiologica_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('per_respiratoria', models.BooleanField(default=False, verbose_name='Respiratorias')),
                ('per_respiratoria_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('per_neurologicas', models.BooleanField(default=False, verbose_name='Neurológicas')),
                ('per_neurologicas_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('per_infecciosas', models.BooleanField(default=False, verbose_name='Infecciosas')),
                ('per_infecciosas_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('per_cirugias', models.BooleanField(default=False, verbose_name='Cirugías')),
                ('per_cirugias_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('per_alergias', models.BooleanField(default=False, verbose_name='Alergias')),
                ('per_alergias_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('per_traumatologicas', models.BooleanField(default=False, verbose_name='Traumatológicas')),
                ('per_traumatologicas_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('per_otras', models.BooleanField(default=False, verbose_name='Otras')),
                ('per_otras_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('medicacion', models.BooleanField(default=False, verbose_name='Toma alguna medicación')),
                ('medicacion_cual', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cual?')),
                ('medicacion_dosis', models.CharField(blank=True, max_length=30, null=True, verbose_name='Qué dosis?')),
                ('fuma', models.BooleanField(default=False, verbose_name='Fuma?')),
                ('alcohol', models.BooleanField(default=False, verbose_name='Toma alcohol?')),
                ('sustancias', models.BooleanField(default=False, verbose_name='Abuso de sustancias?')),
                ('estado_general', models.CharField(max_length=40, verbose_name='Estado general')),
                ('talla', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Talla (mts)')),
                ('peso', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Peso (kg)')),
                ('presion_arterial', models.CharField(max_length=10, verbose_name='TA')),
                ('frecuencia_cardiaca', models.CharField(max_length=10, verbose_name='FC')),
                ('oxigeno_sangre', models.IntegerField(verbose_name='SO2')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('tipo', models.CharField(choices=[('A', 'APTO sin restricciones'), ('B', 'AUTORIZADO con recomendación de evaluación y/o tratamiento médico'), ('C', 'NO AUTORIZADO hasta completar la evaluación, tratamiento y/o rehabilitación')], max_length=2, verbose_name='Tipo de Apto')),
                ('observaciones', models.CharField(blank=True, max_length=80, null=True, verbose_name='Observaciones')),
                ('evaluacion_file', models.ImageField(blank=True, null=True, upload_to='evaluaciones/')),
                ('certificado_file', models.ImageField(blank=True, null=True, upload_to='certificados/')),
                ('deportista', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.deportista')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Evaluación',
                'verbose_name_plural': 'Evaluaciones',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='AntFamiliares',
        ),
        migrations.DeleteModel(
            name='AntPersonales',
        ),
        migrations.DeleteModel(
            name='ExamenFisico',
        ),
        migrations.DeleteModel(
            name='Apto',
        ),
    ]