from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group, Permission
from django.db import models
from django.utils import timezone
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo de correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    imagen = models.ImageField(upload_to='path/to/upload', null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    ru = models.CharField(max_length=20, null=True, blank=True, unique=True )  # Registro Universitario
    ci = models.CharField(max_length=20, null=True, blank=True, unique=True)  # Cédula de Identidad
    fecha_nac = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    anio_ingreso = models.IntegerField(null=True, blank=True)
    gestion_ingreso = models.CharField(max_length=10, null=True, blank=True)
    estado = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
 
    # Añade los campos para las relaciones de grupos y permisos
    groups = models.ManyToManyField(Group, blank=True, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_permissions')
    
    # Campos para la fecha de creación y modificación
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.email} - {self.nombre} {self.apellido}'
