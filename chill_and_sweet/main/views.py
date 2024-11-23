from django.shortcuts import render, redirect, HttpResponse
from django.utils.timezone import now  # Para obtener la fecha y hora actuales
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegisterForm, LoginForm
from .models import Usuario
from .models import *
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# Vista de inicio
def index(request):
    if 'user_id' in request.session:
        return redirect('home')
    
    # Obtener los postres más vendidos o recomendados
    best_sellers = Postre.objects.filter(es_recomendado=True)[:4] 
    
    return render(request, 'index.html', {'best_sellers': best_sellers})

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

#vista de menú
def menu(request):
    return render(request, 'menu.html')


#vista de favoritos
def favoritos(request):
    return render(request, 'favoritos.html')

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
        # Si es una solicitud POST, procesar el formulario
        if request.method == 'POST':
            total = request.POST.get('total', 0.00)  # Obtener el total del formulario
            try:
                usuario = Usuario.objects.get(id=user_id)  # Obtener el usuario actual
                
                # Crear un nuevo pedido
                pedido = Pedido.objects.create(
                    usuario=usuario,
                    fecha=now().date(),  # Fecha actual
                    hora=now().time(),  # Hora actual
                    total=total,
                    puntos_utilizados=0,  # Valor predeterminado
                    estado_pago='pendiente'  # Estado inicial
                )
                
                # Redirigir a una página de confirmación o carrito
                return redirect('order_summary', pedido_id=pedido.id)
            except Usuario.DoesNotExist:
                return redirect('login')  # Si el usuario no existe, redirigir a login

        # Si es una solicitud GET, mostrar la personalización
        ingredientes = Ingrediente.objects.filter(categoriaingrediente__categoria__id=categoria_id)

        # Agrupar ingredientes por tipo (ej. Tipo de café, Tamaño)
        ingredientes_por_tipo = {}
        for ingrediente in ingredientes:
            if ingrediente.tipo not in ingredientes_por_tipo:
                ingredientes_por_tipo[ingrediente.tipo] = []
            ingredientes_por_tipo[ingrediente.tipo].append(ingrediente)

        return render(request, 'custom/personalize.html', {'ingredientes_por_tipo': ingredientes_por_tipo})

    else:
        return redirect('login')  # Si no hay sesión, redirigir al login


# Vista de cuenta del usuario 
def account(request):

    user_id = request.session.get('user_id')
    info_user = None  # Define un valor predeterminado
    equivalenete = 0.00

    if user_id:
        try:
            info_user = Usuario.objects.get(id=user_id)
            equivalenete = info_user.puntos_acumulados / 100
        except Usuario.DoesNotExist:
            info_user = None  # Manejamos el caso donde el usuario no exista
    else:
        return redirect('login')
        
    # Guardamos los cambios de la información del usuario        
    if request.method == "POST":
        form_type = request.POST.get("form_type") #Obtenemos el innput que se llama así
        if(form_type == "info_edit_form"):
            nombre_usuario = request.POST.get("name")
            apellidos_usuario = request.POST.get("lastname")
            correo_usuario = request.POST.get("email")

            info_user.nombre = nombre_usuario
            info_user.apellido = apellidos_usuario
            info_user.correo = correo_usuario

            info_user.save()

            return redirect('account')

        elif(form_type == "pass_edit_form"):
            actual_password = request.POST.get("actualpass", "")
            new_password = request.POST.get("newpass", "")
            confirm_password = request.POST.get("confpass", "")

            # Inicializamos las variables de error
            error_act_pass = 0
            error_new_pass = 0

            # Verificar que la contraseña actual sea correcta
            if not check_password(actual_password, info_user.contrasena):
                messages.error(request, 'La contraseña actual es incorrecta.')
                error_act_pass = 1

            # Verificar que las contraseñas nuevas coincidan
            if new_password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
                error_new_pass = 1

            # Si hay errores, no continuar
            if error_act_pass or error_new_pass:
                request.session['error_act_pass'] = error_act_pass
                request.session['error_new_pass'] = error_new_pass
                return redirect('account')  # Redirigir al mismo formulario para corregir errores

            # Si no hay errores, actualizar la contraseña
            info_user.contrasena = make_password(new_password)
            info_user.save()

            # Limpiar las variables de error en la sesión
            request.session['error_act_pass'] = 0
            request.session['error_new_pass'] = 0

            messages.success(request, '¡Tu contraseña ha sido cambiada exitosamente!')
            return redirect('account')           

    return render(request, 'account/account.html', {"info_user": info_user,
                                                    "equivalente": equivalenete,
                                                    "error_act_pass": request.session.get('error_act_pass'),
                                                    "error_new_pass": request.session.get('error_new_pass')})


def orden(request):
    if request.method == "POST":
        return redirect('pago') 
    user = request.session.get('user_id')
    puntos = Usuario.objects.get(pk=user).puntos_acumulados if user else 0
    return render(request, 'orden/paginaorden.html', {'puntos': puntos})


# Vista de la pagina pago
def pago(request):
    return render(request,'pago/pagopagina.html')