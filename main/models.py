from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, username, dni, medico, password=None):
        usuario = self.model(
            username = username,
            dni = dni,
            medico = medico
            )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, username, dni, medico, password):
        usuario = self.create_user(
            username = username,
            dni = dni,
            medico = medico,
            password = password
            )
        usuario.user_admin = True
        usuario.save()
        return usuario


TIPO_APTO_CHOISE = (
    ('A', 'APTO sin restricciones'),
    ('B', 'AUTORIZADO con recomendación de evaluación y/o tratamiento médico'),
    ('C', 'NO AUTORIZADO hasta completar la evaluación, tratamiento y/o rehabilitación')
)

TIPO_MATRICULA_CHOISE = (
    ('1', 'M.N.'),
    ('2', 'M.P.')
)


class Usuario(AbstractBaseUser):
    """
    USUARIOS MÉDICOS 
    Y USUARIOS ADMINISTRATIVOS
    """
    # id se crea automaticamente
    username = models.CharField('Usuario', unique=True, max_length=15)
    user_temp = models.BooleanField(default=True)
    user_active = models.BooleanField(default=True)
    user_admin = models.BooleanField(default=False)
    apellido = models.CharField('Apellido', max_length=20, null=True, blank=True)
    nombres = models.CharField('Nombre', max_length=30, null=True, blank=True)
    medico = models.BooleanField(default=False)
    dni = models.IntegerField('DNI', null=True, blank=True)
    tipo_matricula = models.CharField('Matrícula', max_length=4, choices=TIPO_MATRICULA_CHOISE, null=True, blank=True)
    matricula = models.CharField('Número', max_length=10, null=True, blank=True)
    especialidad = models.CharField('Especialidad', max_length=20, null=True, blank=True)
    telefono = models.IntegerField('Teléfono', null=True, blank=True)
    mail = models.EmailField('Correo Electrónico', max_length=50, null=True, blank=True)
    image = models.ImageField('Foto de perfil', upload_to='images/', null=True, blank=True)
    objects = UsuarioManager()
    # Para alta de usuarios
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['dni', 'medico']

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'Usuario: {self.username}'
    
    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.user_admin


class Deporte(models.Model):
    """
    DEPORTES
    """
    nombre = models.CharField('Deporte', max_length=30)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Deporte'
        verbose_name_plural = 'Deportes'

    def __str__(self):
        return f'{self.nombre}'


class Institucion(models.Model):
    """
    INSTITUCIONES
    """
    nombre = models.CharField('Nombre', max_length=50)
    direccion = models.CharField('Dirección', max_length=30, null=True, blank=True)
    telefono = models.IntegerField('Teléfono', null=True, blank=True)
    mail = models.EmailField('E-mail', null=True, blank=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'

    # def __str__(self):
    #     return f'{self.nombre, self.direccion, self.telefono, self.mail}'


class Deportista(models.Model):
    """
    DATOS DE DEPORTISTAS
    """
    apellido = models.CharField('Apellido', max_length=20)
    nombres = models.CharField('Nombres', max_length=30)
    dni = models.IntegerField('DNI')
    fecha_nac = models.DateField('Fecha de nacimiento')
    edad = models.IntegerField('Edad')
    domicilio = models.CharField('Domicilio', max_length=30, null=True, blank=True)
    telefono = models.IntegerField('Teléfono', null=True, blank=True)
    obra_social = models.CharField('Obra Social', max_length=25, null=True, blank=True)
    id_deporte = models.ForeignKey(Deporte, on_delete=models.PROTECT)
    id_institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Deportista'
        verbose_name_plural = 'Deportistas'

    def __str__(self):
        return f'Deportista: {self.apellido}, {self.nombres}'


class AntFamiliares(models.Model):
    """
    ANTECEDENTES FAMILIARES PATOLÓGICOS
    """
    fam_cardiovasculares = models.BooleanField('Cardiovasculares', default=False)
    fam_cardiovasculares_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    fam_neurologicas = models.BooleanField('Neurológicas', default=False)
    fam_neurologicas_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    fam_tumorales = models.BooleanField('Tumorales', default=False)
    fam_tumorales_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    fam_respiratorias = models.BooleanField('Respiratorias', default=False)
    fam_respiratorias_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    fam_desangre = models.BooleanField('De la sangre', default=False)
    fam_desangre_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    fam_otras = models.BooleanField('Otras', default=False, null=True, blank=True)
    fam_otras_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    fam_obs = models.TextField(null=True, blank=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Antecedentes Familiares'
        verbose_name_plural = 'Antecedentes Familiares'


class AntPersonales(models.Model):
    """
    ANTECEDENTES PERSONALES PATOLÓGICOS
    """
    per_cardiologica = models.BooleanField('Cardiológicas', default=False)
    per_cardiologica_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    per_respiratoria = models.BooleanField('Respiratorias', default=False)
    per_respiratoria_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    per_neurologicas = models.BooleanField('Neurológicas', default=False)
    per_neurologicas_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    per_infecciosas = models.BooleanField('Infecciosas', default=False)
    per_infecciosas_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    per_cirugias = models.BooleanField('Cirugías', default=False)
    per_cirugias_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    per_alergias = models.BooleanField('Alergias', default=False)
    per_alergias_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    per_traumatologicas = models.BooleanField('Traumatológicas', default=False)
    per_traumatologicas_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    per_otras = models.BooleanField('Otras', default=False)
    per_otras_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    # MEDICACIÓN
    medicacion = models.BooleanField('Toma alguna medicación', default=False)
    medicacion_cual = models.CharField('Cual?', max_length=30, null=True, blank=True)
    medicacion_dosis = models.CharField('Qué dosis?', max_length=30, null=True, blank=True)
    fuma = models.BooleanField('Fuma?', default=False)
    alcohol = models.BooleanField('Toma alcohol?', default=False)
    sustancias = models.BooleanField('Abuso de sustancias?', default=False)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Antecedentes Personales'
        verbose_name_plural = 'Antecedentes Personales'


class ExamenFisico(models.Model):
    """
    EXAMEN FÍSICO
    """
    # id_examen / se crea automaticamente
    estado_general = models.CharField('Estado general', max_length=40)
    talla = models.DecimalField('Talla (mts)', decimal_places=2, max_digits=3)
    peso = models.DecimalField('Peso (kg)', decimal_places=3, max_digits=6)
    presion_arterial = models.CharField('TA', max_length=10)
    frecuencia_cardiaca = models.CharField('FC', max_length=10)
    oxigeno_sangre = models.IntegerField('SO2')

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Examen'
        verbose_name_plural = 'Exámenes'


class Apto(models.Model):
    """
    CERTIFICADO DE APTO FISICO
    """
    id_deportista = models.ForeignKey(Deportista, on_delete=models.PROTECT)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha = models.DateField(auto_now=True, auto_now_add=False)
    id_familiares = models.ForeignKey(AntFamiliares, on_delete=models.PROTECT)
    id_personales = models.ForeignKey(AntPersonales, on_delete=models.PROTECT)
    id_examen = models.ForeignKey(ExamenFisico, on_delete=models.PROTECT)
    tipo = models.CharField('Tipo de Apto', max_length=2, choices=TIPO_APTO_CHOISE)
    observaciones = models.CharField('Observaciones', max_length=80, null=True, blank=True)
#     apto_pdf = models.ImageField()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Apto'
        verbose_name_plural = 'Aptos'