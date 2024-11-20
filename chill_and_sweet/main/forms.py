from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    # Campo para la contraseña
    contrasena = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )

    # Campo para confirmar la contraseña
    confirmar_contrasena = forms.CharField(
        label="Confirmar contraseña", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'})
    )

    class Meta:
        model = Usuario 
        fields = ['nombre', 'apellido', 'correo', 'contrasena'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        }
        error_messages = {
            'correo': {
                'invalid': "Por favor, ingresa un correo electrónico válido.",
                'unique': "Este correo ya está registrado. Por favor inicia sesión.",
            },
        }

    # Validación personalizada para nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            raise ValidationError("El nombre solo debe contener letras, espacios y caracteres acentuados.")
        return nombre

    # Validación personalizada para apellido
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', apellido):
            raise ValidationError("El apellido solo debe contener letras, espacios y caracteres acentuados.")
        return apellido

    # Validación personalizada para el campo de contraseña
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')

        # Verificación de longitud mínima
        if len(contrasena) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        # Verificación de que contenga al menos una letra mayúscula
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")

        # Verificación de que contenga al menos una letra minúscula
        if not re.search(r'[a-z]', contrasena):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")

        # Verificación de que contenga al menos un número
        if not re.search(r'\d', contrasena):
            raise ValidationError("La contraseña debe contener al menos un número.")

        # Verificación de que contenga al menos un carácter especial
        if not re.search(r'[!@#$%^&*()_\-+=\[\]{}|\\:;"\'<>,.?/~`]', contrasena):
            raise ValidationError("La contraseña debe contener al menos un carácter especial (ej: !@#$%).")

        return contrasena
    
    # Validación general del formulario para asegurar que ambas contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")

        # Verificación de que las contraseñas coinciden
        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

class LoginForm(forms.Form):
    correo = forms.EmailField(
        label="Correo electrónico", 
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'})
    )
    contrasena = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )