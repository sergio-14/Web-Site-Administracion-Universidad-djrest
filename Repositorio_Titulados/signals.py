from django.db.models.signals import post_save
from django.dispatch import receiver
from Seg_Mod_Graduacion.models import ProyectoFinal
from .models import Titulado
from django.utils import timezone

@receiver(post_save, sender=ProyectoFinal)
def crear_titulado(sender, instance, created, **kwargs):
    if created and instance.estado == 'Aprobado':
        Titulado.objects.create(
            usuario=instance.usuario,
            proyecto_final=instance,
            anio_ingreso=instance.usuario.anio_ingreso,
            periodo_ingreso=instance.usuario.gestion_ingreso,
            anio_egreso=timezone.now().year,
            periodo_egreso='Periodo ejemplo',  # Ajusta esto según tu lógica
            nota=0  # Ajusta esto según tu lógica
        )

