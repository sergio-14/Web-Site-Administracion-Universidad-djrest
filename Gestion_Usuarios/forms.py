from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

# Validaciones para inicio de sesión
class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Correo Electrónico'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_attempt = True

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                self.first_attempt = False
                if not User.objects.filter(email=email).exists():
                    self.add_error('email', "El correo electrónico no existe.")
                else:
                    self.add_error('password', "La contraseña es incorrecta.")
            elif not user.is_active:
                self.first_attempt = False
                raise forms.ValidationError("Esta cuenta está inactiva.")
        return cleaned_data

# Validaciones para registrar nuevo usuario
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'ci', 'ru', 'is_active', 'is_staff','is_superuser', 'password1', 'password2', 'groups')
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'flexSwitchCheckActive'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'flexSwitchCheckStaff'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'flexSwitchCheckSuperuser'}),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise ValidationError(_("La contraseña debe tener al menos 8 caracteres."))

        if not any(char.isupper() for char in password1):
            raise ValidationError(_("La contraseña debe contener al menos una mayúscula."))

        if password1.isdigit():
            raise ValidationError(_("La contraseña no puede consistir solo en números."))

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Las contraseñas no coinciden."))

        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Ya existe un usuario con este correo electrónico."))

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            docentes_group, created = Group.objects.get_or_create(name='Docentes')
            user.groups.add(docentes_group)
        return user

# Formulario para actualizar usuario
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'imagen', 'ru', 'ci', 'fecha_nac', 'telefono', 'anio_ingreso', 'gestion_ingreso', 'is_active', 'is_staff','is_superuser', 'groups')
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'flexSwitchCheckActive'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'flexSwitchCheckStaff'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'flexSwitchCheckSuperuser'}),
        }

