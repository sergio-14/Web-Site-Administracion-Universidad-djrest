from django import forms
from .models import T_Proyectos, IntSocSettings, T_Tipo_Proyecto, T_Fase_proyecto, T_Gestion, T_Semestre, T_Materia
from datetime import date

        
#proyectos de interaccion social 
class T_ProyectosForm(forms.ModelForm):
    class Meta:
        model = T_Proyectos
        fields = ['S_Titulo','Fecha_Inicio','Fecha_Finalizacion','S_Descripcion','S_Documentacion','S_Imagen','T_Fase_proyecto','T_Gestion','T_Tipo_Proyecto','T_Materia']
        widgets = {
            'Fecha_Inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'Fecha_Finalizacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(T_ProyectosForm, self).__init__(*args, **kwargs)
        settings = IntSocSettings.objects.first()
        if settings:
            hoy = date.today()
            if not (settings.fecha_inicio_habilitacion <= hoy <= settings.fecha_fin_habilitacion):
                for field in self.fields:
                    self.fields[field].disabled = True
                    
                

class IntSocSettingsForm(forms.ModelForm):
    class Meta:
        model = IntSocSettings
        fields = ['fecha_inicio_habilitacion', 'fecha_fin_habilitacion']
        widgets = {
            'fecha_inicio_habilitacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_fin_habilitacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(IntSocSettingsForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio_habilitacion'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_fin_habilitacion'].input_formats = ['%Y-%m-%d']
        

class TipoProyectoForm(forms.ModelForm):
    class Meta:
        model = T_Tipo_Proyecto
        fields = ['S_Tipo']

class FaseProyectoForm(forms.ModelForm):
    class Meta:
        model = T_Fase_proyecto
        fields = ['S_Fase']

class GestionForm(forms.ModelForm):
    class Meta:
        model = T_Gestion
        fields = ['S_Gestion']

class SemestreForm(forms.ModelForm):
    class Meta:
        model = T_Semestre
        fields = ['S_Semestre']

class MateriaForm(forms.ModelForm):
    class Meta:
        model = T_Materia
        fields = ['S_Materia', 'T_Semestre']