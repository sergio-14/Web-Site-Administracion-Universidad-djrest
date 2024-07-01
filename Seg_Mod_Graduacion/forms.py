from django import forms
from .models import InvCientifica, ComentarioInvCientifica, InvSettings, PerfilProyecto, ComentarioPerfil,ProyectoFinal

# área de investigación científica 
class InvCientificaForm(forms.ModelForm):
    class Meta:
        model = InvCientifica
        fields = ['invtitulo', 'invdescripcion', 'invdocumentacion', 'invmodalidad', 'invdestacado']
        widgets = {
            'invdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }

class InvComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioInvCientifica
        fields = ['invcomentario'] 
        widgets = {
            'invcomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = InvSettings
        fields = ['habilitarInv']

    def __init__(self, *args, **kwargs):
        super(GlobalSettingsForm, self).__init__(*args, **kwargs)
        
# área de perfil de proyecto 
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilProyecto
        fields = ['pertitulo', 'perdescripcion', 'perdocumentacion', 'permodalidad']
        widgets = {
            'perdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }
        
class PerComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioPerfil
        fields = ['percomentario'] 
        widgets = {
            'percomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }

class ProyectoFinalForm(forms.ModelForm):
    class Meta:
        model = ProyectoFinal
        fields = ['titulo', 'slug', 'resumen', 'modalidad', 'fecha', 'tribunales', 'tutor', 'tutor_externo', 'documentacion', 'estado']
