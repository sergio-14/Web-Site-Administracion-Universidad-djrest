from django import forms
from .models import PERIODO_CHOICES, Titulado
from Seg_Mod_Graduacion.models import ProyectoFinal

class TituladoForm(forms.ModelForm):
    class Meta:
        model = Titulado
        fields = '__all__'
        widgets = {
            'anio_ingreso': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'anio_egreso': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'periodo_ingreso': forms.Select(choices=PERIODO_CHOICES),
            'periodo_egreso': forms.Select(choices=PERIODO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.usuario:
            self.fields['proyecto_final'].queryset = ProyectoFinal.objects.filter(user=self.instance.usuario, estado='Aprobado')
