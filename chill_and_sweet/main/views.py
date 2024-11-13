from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm
from .models import Usuario

# Vista de inicio
def index(request):
    return render(request, 'index.html')

# # Vista de inicio de sesión
# def login(request):
#     return render(request, 'auth/login.html')

# Vista de registro
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) 

        # Verificación de validez del formulario
        if form.is_valid(): 
            data_form = form.cleaned_data
            correo = data_form.get('correo')
            
            # Crear nuevo usuario
            user = form.save(commit=False)
            user.contrasena = make_password(data_form['contrasena'])
            user.save()

            messages.success(request, 'Te has registrado correctamente.')
            login(request, user)  
            return redirect('index')
        
        # Si el formulario no es válido, muestra los errores
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})