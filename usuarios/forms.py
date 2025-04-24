# usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Carrera, Perfil

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    
    ROL_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('administrativo', 'Administrativo'),
    ]
    
    rol = forms.ChoiceField(choices=ROL_CHOICES, required=True, label='Rol en la universidad')
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.filter(activo=True), required=False, label='Carrera')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rol', 'carrera')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de Bootstrap a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        
        # Script para ocultar/mostrar campo carrera según el rol
        self.fields['carrera'].widget.attrs['id'] = 'id_carrera_field'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@uab.edu.bo'):
            raise forms.ValidationError('Solo se permiten correos con dominio @uab.edu.bo')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        carrera = cleaned_data.get('carrera')
        
        if rol == 'estudiante' and not carrera:
            self.add_error('carrera', 'Este campo es obligatorio para estudiantes')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super(FormularioRegistro, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Crear el perfil asociado
            Perfil.objects.create(
                usuario=user,
                rol=self.cleaned_data['rol'],
                carrera=self.cleaned_data['carrera'] if self.cleaned_data['rol'] == 'estudiante' else None,
                estado_verificacion='pendiente' if self.cleaned_data['rol'] == 'administrativo' else 'aprobado'
            )
        
        return user

class FormularioLogin(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': ' '  # Placeholder vacío para form-floating
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'floatingPassword',
            'placeholder': ' '  # Placeholder vacío para form-floating
        })
    )