from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .forms import InvCientificaForm, InvComentarioForm, GlobalSettingsForm, PerfilForm, PerComentarioForm,ProyectoFinalForm
from .models import InvCientifica, ComentarioInvCientifica, InvSettings, PerfilProyecto, ComentarioPerfil,ProyectoFinal

##############  permisos decoradores  para funciones y clases   ################  

#modalidad de graduación permigroup 
def permiso_M_G(user, ADMMGS):
    try:
        grupo = Group.objects.get(name=ADMMGS)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{ADMMGS}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied
    
#permiso para docentes  
def permiso_Docentes(user, Docentes):
    try:
        grupo = Group.objects.get(name=Docentes)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{Docentes}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#permiso para estudiantes
def permiso_Estudiantes(user, Estudiantes):
    try:
        grupo = Group.objects.get(name=Estudiantes)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{Estudiantes}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#vista 403
def handle_permission_denied(request, exception):
    return render(request, '403.html', status=403)

################  vistas modalidad de graduación  ##########################

#vista agregar formulario alcance de proyecto 
@login_required
@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def vista_investigacion(request):
    proyectos_usuario = InvCientifica.objects.filter(user=request.user).order_by('-invfecha_creacion').prefetch_related('comentarioinvcientifica_set')

    paginator = Paginator(proyectos_usuario, 1)  
    page_number = request.GET.get('page')
    proyectos_paginados = paginator.get_page(page_number)

    return render(request, 'invcientifica/vista_investigacion.html', {'proyectos': proyectos_paginados})

@method_decorator(user_passes_test(lambda u: permiso_M_G(u, 'ADMMGS')), name='dispatch')
class ProyectosParaAprobar(View):
    def get(self, request):
        proyectos = InvCientifica.objects.filter(investado='Pendiente')
        proyectos_con_formulario = {proyecto: InvComentarioForm() for proyecto in proyectos}
        
        context = {
            'proyectos': proyectos_con_formulario,
        }
        return render(request, 'invcientifica/ProyectosParaAprobar.html', context)
    
    def post(self, request):
        proyecto_id = request.POST.get('proyecto_id')
        comentario_texto = request.POST.get('comentario_texto')
        if proyecto_id and comentario_texto:
            proyecto = get_object_or_404(InvCientifica, pk=proyecto_id)
            ComentarioInvCientifica.objects.create(invcomentario=comentario_texto, user=request.user, invproyecto_relacionado=proyecto)
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al agregar el comentario.')
        
        if 'aprobar' in request.POST:
            return AprobarProyecto().post(request, proyecto_id)
        elif 'rechazar' in request.POST:
            return RechazarProyecto().post(request, proyecto_id)
        else:
            messages.error(request, 'Hubo un error al procesar la solicitud.')
            return redirect('ProyectosParaAprobar')

class AprobarProyecto(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(InvCientifica, pk=proyecto_id)
        proyecto.investado = 'Aprobado'
        proyecto.save()
        messages.success(request, '¡Proyecto aprobado exitosamente!')
        return redirect('ProyectosParaAprobar')

class RechazarProyecto(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(InvCientifica, pk=proyecto_id)
        proyecto.investado = 'Rechazado'
        proyecto.save()
        messages.error(request, '¡Proyecto rechazado!')
        return redirect('ProyectosParaAprobar')

@user_passes_test(lambda u: permiso_M_G(u, 'ADMMGS')) 
def global_settings_view(request):
    settings = InvSettings.objects.first()
    if not settings:
        settings = InvSettings()

    if request.method == 'POST':
        form = GlobalSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GlobalSettingsForm(instance=settings)
    
    return render(request, 'invcientifica/global_settings.html', {'form': form, 'settings': settings})

@login_required
@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def agregar_investigacion(request):
    settings = InvSettings.objects.first()
    
    if not settings:
        messages.error(request, 'No se encontró la configuración global. Por favor, contacta al administrador.')
        return redirect('global_settings')
    
    tiene_investigacion_aprobada = InvCientifica.objects.filter(user=request.user, investado='Aprobado').exists()
    
    form_disabled = not settings.habilitarInv or tiene_investigacion_aprobada
    
    if request.method == 'POST' and not form_disabled:
        form = InvCientificaForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            
            slug = slugify(proyecto.invtitulo)
            counter = 1
            while InvCientifica.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            proyecto.slug = slug
            
            proyecto.user = request.user
            proyecto.save()
            return redirect('dashboard')
    else:
        form = InvCientificaForm()
    
    if form_disabled:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'invcientifica/agregar_investigacion.html', {
        'form': form,
        'form_disabled': form_disabled,
    })

########  PERFIL DE PROYECTO M. G 2DA PARTE   #########
@login_required
@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def vista_perfil(request):
    proyectos_usuario = PerfilProyecto.objects.filter(user=request.user).order_by('-perfecha_creacion').prefetch_related('comentarios')
    
    paginator = Paginator(proyectos_usuario, 1) 
    page_number = request.GET.get('page')
    proyectos_paginados = paginator.get_page(page_number)

    return render(request, 'perfil/vista_perfil.html', {'proyectos': proyectos_paginados})

@method_decorator(user_passes_test(lambda u: permiso_M_G(u, 'ADMMGS')), name='dispatch')
class PerfilesParaAprobar(View):
    def get(self, request):
        proyectos = PerfilProyecto.objects.filter(perestado='Pendiente')
        proyectos_con_formulario = {proyecto: PerComentarioForm() for proyecto in proyectos}
        
        context = {
            'proyectos': proyectos_con_formulario,
        }
        return render(request, 'perfil/PerfilesParaAprobar.html', context)
    
    def post(self, request):
        proyecto_id = request.POST.get('proyecto_id')
        comentario_texto = request.POST.get('comentario_texto')
        if proyecto_id and comentario_texto:
            proyecto = get_object_or_404(PerfilProyecto, pk=proyecto_id)
            ComentarioPerfil.objects.create(percomentario=comentario_texto, user=request.user, perproyecto_relacionado=proyecto)
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al agregar el comentario.')
        
        if 'aprobar' in request.POST:
            return AprobarPerfil().post(request, proyecto_id)
        elif 'rechazar' in request.POST:
            return RechazarPerfil().post(request, proyecto_id)
        else:
            messages.error(request, 'Hubo un error al procesar la solicitud.')
            return redirect('PerfilesParaAprobar')
    
class AprobarPerfil(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(PerfilProyecto, pk=proyecto_id)
        proyecto.perestado = 'Aprobado'
        proyecto.save()
        messages.success(request, '¡Perfil aprobado exitosamente!')
        return redirect('PerfilesParaAprobar')

class RechazarPerfil(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(PerfilProyecto, pk=proyecto_id)
        proyecto.perestado = 'Rechazado'
        proyecto.save()
        messages.error(request, '¡Perfil rechazado!')
        return redirect('PerfilesParaAprobar')

@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes'))
def agregar_perfil(request):
    tiene_investigacion_aprobada = InvCientifica.objects.filter(user=request.user, investado='Aprobado').exists()
    form_disabled = not tiene_investigacion_aprobada

    if request.method == 'POST' and not form_disabled:
        formp = PerfilForm(request.POST, request.FILES)
        print("Formulario enviado. Método POST.")
        if formp.is_valid():
            print("Formulario es válido.")
            proyecto = formp.save(commit=False)
            
            slug = slugify(proyecto.pertitulo)
            counter = 1
            while PerfilProyecto.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            proyecto.slug = slug
            
            proyecto.user = request.user
            proyecto.save()
            return redirect('dashboard')
        else:
            print("Formulario no es válido:", formp.errors)
    else:
        formp = PerfilForm()

    if form_disabled:
        for field in formp.fields.values():
            field.widget.attrs['disabled'] = 'disabled'

    return render(request, 'perfil/agregar_perfil.html', {
        'formp': formp,
        'form_disabled': form_disabled,
    })
    
#### VISTA DE PROYECTO FINAL #####

### VISTA PARA EL ESTUDIANTE ###
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Estudiantes').exists())
def agregar_proyecto_final(request):
    if request.method == 'POST':
        form = ProyectoFinalForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.user = request.user
            proyecto.save()
            messages.success(request, 'Proyecto final agregado exitosamente.')
            return redirect('dashboard')
    else:
        form = ProyectoFinalForm()
    
    return render(request, 'proyectofinal/agregar_proyecto_final.html', {'form': form})

### VISTA PARA EL ADMINISTRADOR ###
@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Administrador').exists()), name='dispatch')
class RevisarProyectoFinal(View):
    def get(self, request):
        proyectos = ProyectoFinal.objects.filter(estado='Pendiente')
        return render(request, 'proyectofinal/revisar_proyecto_final.html', {'proyectos': proyectos})

    def post(self, request):
        proyecto_id = request.POST.get('proyecto_id')
        accion = request.POST.get('accion')
        proyecto = get_object_or_404(ProyectoFinal, id=proyecto_id)
        
        if accion == 'aprobar':
            proyecto.estado = 'Aprobado'
            proyecto.save()
            proyecto.user.estado = True
            proyecto.user.save()
            messages.success(request, 'Proyecto final aprobado exitosamente.')
        elif accion == 'rechazar':
            proyecto.estado = 'Rechazado'
            proyecto.save()
            messages.error(request, 'Proyecto final rechazado.')

        return redirect('revisar_proyecto_final')
