from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GroupForm
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# Página Principal
def home(request):
    return render(request, 'home.html')

# Iniciar Sesion
def iniciar_sesion(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            # Verificar si los campos están vacíos
            if form.cleaned_data.get('email') or form.cleaned_data.get('password'):
                form.first_attempt = False
            else:
                form.first_attempt = True
    else:
        form = CustomLoginForm()
    return render(request, 'IniciarSesion.html', {'form': form})

# Registrar
def registrar(request):
    errors = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciar_sesion')
        else:
            errors = form.errors  # Captura los errores
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'Registrar.html', {'form': form, 'errors': errors})

# Cerrar Sesión
def signout(request):
    logout(request)
    return redirect('home')

# DashBoard
def dashboard(request):
    return render(request, "dashboard.html")

# Listar Usuarios
def listar_usuarios(request):
    query = request.GET.get('q')
    if query:
        usuarios = User.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        usuarios = User.objects.filter(is_active=True)

    paginator = Paginator(usuarios, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('Gestion_Usuarios/usuarios_list.html', {'page_obj': page_obj})
        return JsonResponse({'html': html})

    return render(request, 'Gestion_Usuarios/listar_usuarios.html', {'page_obj': page_obj, 'query': query})


# Crear Usuario
@login_required
def crear_usuario(request):
    errors = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            
            # Registrar la acción de creación
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(usuario).pk,
                object_id=usuario.pk,
                object_repr=str(usuario),
                action_flag=ADDITION
            )
            
            return redirect('listar_usuarios')
        else:
            errors = form.errors  # Captura los errores
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'Gestion_Usuarios/crear_usuario.html', {'form': form, 'errors': errors})

# Actualizar Usuario
@login_required
def actualizar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            
            # Registrar la acción de actualización
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(usuario).pk,
                object_id=usuario.pk,
                object_repr=str(usuario),
                action_flag=CHANGE
            )
            
            messages.success(request, 'El usuario ha sido actualizado.')
            return redirect('listar_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)
    
    return render(request, 'Gestion_Usuarios/actualizar_usuario.html', {'form': form, 'usuario': usuario})

# Eliminar Usuario
@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = False
    usuario.save()
    
    # Registrar la acción de eliminación
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(usuario).pk,
        object_id=usuario.pk,
        object_repr=str(usuario),
        action_flag=DELETION
    )
    
    messages.success(request, 'El usuario ha sido eliminado.')
    return redirect('listar_usuarios')

@login_required
def listar_usuarios_inactivos(request):
    usuarios_inactivos = User.objects.filter(is_active=False)
    return render(request, 'Gestion_Usuarios/listar_usuarios_inactivos.html', {'usuarios_inactivos': usuarios_inactivos})

@login_required
def reactivar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = True
    usuario.save()
        # Registrar la acción de reactivación
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(usuario).pk,
        object_id=usuario.pk,
        object_repr=str(usuario),
        action_flag=ADDITION
    )
    messages.success(request, 'El usuario ha sido reactivado.')
    return redirect('listar_usuarios_inactivos')  
    
# Listar Grupos
@login_required
def listar_grupos(request):
    grupos = Group.objects.all()
    return render(request, 'Gestion_Usuarios/listar_grupos.html', {'grupos': grupos})

# Crear Grupos
@login_required
def crear_grupo(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            grupo = form.save()
            
            # Registrar la acción de creación
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(grupo).pk,
                object_id=grupo.pk,
                object_repr=str(grupo),
                action_flag=ADDITION
            )
            
            messages.success(request, f'Grupo {grupo.name} creado exitosamente.')
            return redirect('listar_grupos')
    else:
        form = GroupForm()
    return render(request, 'Gestion_Usuarios/crear_grupo.html', {'form': form})

#Actualizar Grupos
@login_required
def actualizar_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, 'El grupo ha sido actualizado con éxito.')
            return redirect('listar_grupos')
    else:
        form = GroupForm(instance=grupo)
    return render(request, 'Gestion_Usuarios/actualizar_grupo.html', {'form': form, 'grupo': grupo})

# Eliminar Grupos
@login_required
def eliminar_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'El grupo ha sido eliminado con éxito.')
        return redirect('listar_grupos')
    return render(request, 'Gestion_Usuarios/eliminar_grupo.html', {'grupo': grupo})