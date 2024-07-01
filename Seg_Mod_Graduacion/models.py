from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings

User = get_user_model()

ESTADO_CHOICES = [
    ('Aprobado', 'Aprobado'),
    ('Pendiente', 'Pendiente'),
    ('Rechazado', 'Rechazado'),
]

class TutorExterno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Materia(models.Model):
    sigla = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.sigla})"

class Modalidad(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre

class InvCientifica(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    invtitulo = models.CharField(max_length=150, verbose_name='Agregar Titulo')
    slug = models.SlugField(unique=True)
    invfecha_creacion = models.DateTimeField(auto_now_add=True)
    invdescripcion = models.TextField(verbose_name='Agregar una Descripcion', blank=True)
    invdocumentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True, blank=True)
    invmodalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    invdestacado = models.BooleanField(default=True, verbose_name='Destacar Formulario')
    investado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.invtitulo

class ComentarioInvCientifica(models.Model):
    invcomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    invfecha_post = models.DateTimeField(auto_now_add=True)
    invproyecto_relacionado = models.ForeignKey(InvCientifica, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-invfecha_post']

    def __str__(self):
        return self.invcomentario[:15] + '...' if len(self.invcomentario) > 15 else self.invcomentario

class InvSettings(models.Model):
    habilitarInv = models.BooleanField(default=True, verbose_name='Habilitar Formulario')

    def __str__(self):
        return "Configuración Global"

class PerfilProyecto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    pertitulo = models.CharField(max_length=150, verbose_name='Agregar Titulo Perfil')
    slug = models.SlugField(unique=True)
    perfecha_creacion = models.DateTimeField(auto_now_add=True)
    perdescripcion = models.TextField(verbose_name='Agregar una Descripcion', blank=True)
    perdocumentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True, blank=True)
    permodalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    perestado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.pertitulo

class ComentarioPerfil(models.Model):
    percomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    perfecha_post = models.DateTimeField(auto_now_add=True)
    perproyecto_relacionado = models.ForeignKey(PerfilProyecto, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        ordering = ['-perfecha_post']

    def __str__(self):
        return self.percomentario[:15] + '...' if len(self.percomentario) > 15 else self.percomentario

class ProyectoFinal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    resumen = models.TextField(max_length=500)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    tribunales = models.ManyToManyField(User, related_name='tribunales', limit_choices_to={'groups__name': 'Docentes'}, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_final', limit_choices_to={'groups__name': 'Docentes'})
    tutor_externo = models.ForeignKey(TutorExterno, on_delete=models.SET_NULL, null=True, blank=True)
    documentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.titulo
