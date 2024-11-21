from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegisterForm, LoginForm
from .models import Usuario
from .models import *

from django.contrib.auth.decorators import login_required

# Vista de inicio
def index(request):
    if 'user_id' in request.session:
        return redirect('home')
    
    return render(request, 'index.html')

# Vista de ayuda
def help_view(request):
    return render(request, 'help.html')

# Vista de registro
def register_view(request):
    # Si el usuario ya está autenticado, redirigir a la página de inicio
    if 'user_id' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 

        # Verificación de validez del formulario
        if form.is_valid(): 
            user = form.save(commit=False) 
            user.contrasena = make_password(form.cleaned_data['contrasena']) 
            user.save() 
            # messages.success(request, 'Te has registrado correctamente.')
            return redirect('index')
        
        # Si el formulario no es válido, muestra los errores
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


# Vista de inicio de sesión
def login_view(request):
    # Si el usuario ya está autenticado, redirigir a la página de inicio
    if 'user_id' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

            try:
                # Buscar el usuario por correo
                user = Usuario.objects.get(correo=correo)

                # Verificar la contraseña
                if check_password(contrasena, user.contrasena):
                    # Inicio de sesión exitoso, guardar ID de usuario en la sesión
                    request.session['user_id'] = user.id
                    # messages.success(request, 'Has iniciado sesión correctamente.')
                    return redirect('home')
                else:
                    messages.error(request, 'La contraseña es incorrecta.')

            except Usuario.DoesNotExist:
                messages.error(request, 'Este correo no está registrado.')

    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

# Vista de cierre de sesión
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id'] 
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('index')

# Vista de inicio después de loguearse (Home)
def home_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        # Obtener el usuario de la base de datos
        user = Usuario.objects.get(id=user_id)
        return render(request, 'home.html', {'user': user})
    else:
        return redirect('login')


# Vista de menu de categorias de postres para crear un postre personalizado
def create(request):
    user_id = request.session.get('user_id')
    if user_id:
        categorias = Categoria.objects.all()

        return render(request, 'custom/create.html', {"categorias":categorias})
    else:
        return redirect('login')

# Vista de menu para personaizar un postre 
def customDessert(request, categoria_id):
    user_id = request.session.get('user_id')
    if user_id:
        # Filtrar los ingredientes de la categoría específica usando categoria_id
        ingredientes = Ingrediente.objects.filter(categoriaingrediente__categoria__id=categoria_id)

        # Agrupar ingredientes por tipo (ej. Tipo de café, Tamaño)
        ingredientes_por_tipo = {}
        for ingrediente in ingredientes:
            if ingrediente.tipo not in ingredientes_por_tipo:
                ingredientes_por_tipo[ingrediente.tipo] = []
            ingredientes_por_tipo[ingrediente.tipo].append(ingrediente)

        return render(request,'custom/personalize.html',{'ingredientes_por_tipo': ingredientes_por_tipo})
    else:
        return redirect('login')


def orden(request):
    if request.method == "POST":
        # Capturar los datos del formulario
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        forma = request.POST.get("forma")
        
        # Guardar en la sesión
        request.session["fecha"] = fecha
        request.session["hora"] = hora
        request.session["forma"] = forma

        # Redirigir a la página de pago
        return redirect("../pago")  # Usa el nombre correcto de la URL para la página de pago
    
    usuario = request.user  # Obtiene el usuario autenticado
    try:
        datos_usuario = Usuario.objects.get(pk=usuario.pk)  # Obtén la información del usuario
        puntos = datos_usuario.puntos_acumulados
    except Usuario.DoesNotExist:
        puntos = 0  # Si el usuario no existe, asigna 0 puntos

    context = {
        'puntos': puntos,
    }
    return render(request, 'orden/paginaorden.html', context)

# Vista de la pagina pago
def pago(request):
    return render(request,'pago/pagopagina.html')

# pago
def mostrar_pago(request):
    # Obtener los datos de la sesión
    fecha = request.session.get("fecha", "No especificado")
    hora = request.session.get("hora", "No especificado")
    forma = request.session.get("forma", "No especificado")

    contexto = {
        "fecha": fecha,
        "hora": hora,
        "forma": forma,
    }
    return render(request, "pagopagina.html", contexto)