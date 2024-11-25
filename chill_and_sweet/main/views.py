from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.utils.timezone import now  # Para obtener la fecha y hora actuales
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegisterForm, LoginForm
from .models import Usuario
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime, timedelta, time
import json

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

# Vista del menú
def menu(request):
    user_id = request.session.get('user_id')
    if user_id:
        categorias = Categoria.objects.prefetch_related('postre_set').all()
        return render(request, 'menu.html', {'categorias': categorias})
    else:
        return redirect('login')
    
def add_to_cart(request):
    if request.method == 'POST':
        postre_id = request.POST.get('postre_id')
        cantidad = int(request.POST.get('cantidad', 1))

        postre = get_object_or_404(Postre, id=postre_id)
        usuario = Usuario.objects.get(id=request.session['user_id'])

        # Verificar si ya existe en el carrito
        carrito_item, created = Carrito.objects.get_or_create(usuario=usuario, postre=postre)
        if not created:
            carrito_item.cantidad += cantidad
        carrito_item.save()

        # Agregar mensaje de éxito
        messages.success(request, f'{postre.nombre} se agregó al carrito.')

        # Redirigir al menú
        return redirect('menu')

    # En caso de que no sea un método POST
    return redirect('menu')

@csrf_exempt
def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        postre_id = data.get("postre_id")
        nueva_cantidad = data.get("cantidad")

        if not postre_id or not nueva_cantidad:
            return JsonResponse({"success": False, "message": "Datos inválidos."})

        try:
            usuario = Usuario.objects.get(id=request.session["user_id"])
            carrito_item = Carrito.objects.get(usuario=usuario, postre_id=postre_id)
            carrito_item.cantidad = nueva_cantidad
            carrito_item.save()

            # Recalcular total
            carrito_items = Carrito.objects.filter(usuario=usuario)
            total = sum(item.postre.precio * item.cantidad for item in carrito_items)

            return JsonResponse({
                "success": True,
                "subtotal": carrito_item.postre.precio * carrito_item.cantidad,
                "total": total,
            })
        except Carrito.DoesNotExist:
            return JsonResponse({"success": False, "message": "Elemento no encontrado."})
        except Usuario.DoesNotExist:
            return JsonResponse({"success": False, "message": "Usuario no autenticado."})

    return JsonResponse({"success": False, "message": "Método no permitido."})

@csrf_exempt
def delete_from_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        postre_id = data.get("postre_id")

        if not postre_id:
            return JsonResponse({"success": False, "message": "ID del producto no proporcionado."})

        try:
            usuario = Usuario.objects.get(id=request.session["user_id"])
            carrito_item = Carrito.objects.get(usuario=usuario, postre_id=postre_id)
            carrito_item.delete()

            # Recalcular el total general
            carrito_items = Carrito.objects.filter(usuario=usuario)
            total = sum(item.postre.precio * item.cantidad for item in carrito_items)

            return JsonResponse({"success": True, "total": total})
        except Carrito.DoesNotExist:
            return JsonResponse({"success": False, "message": "Producto no encontrado en el carrito."})
        except Usuario.DoesNotExist:
            return JsonResponse({"success": False, "message": "Usuario no autenticado."})

    return JsonResponse({"success": False, "message": "Método no permitido."})

def confirm_order(request):
    if request.method == "POST":
        fecha_pedido = request.POST.get("fecha_pedido")
        hora_pedido = request.POST.get("hora_pedido")
        forma = request.POST.get("forma")

        try:
            fecha_hora_pedido = datetime.strptime(f"{fecha_pedido} {hora_pedido}", "%Y-%m-%d %H:%M")
            ahora = datetime.now()
            limite_dos_horas = ahora + timedelta(hours=2)

            # Verificar que la fecha y hora están dentro del rango permitido
            if fecha_hora_pedido < ahora or fecha_hora_pedido > limite_dos_horas:
                messages.error(request, "La fecha y hora deben estar entre ahora y dentro de dos horas.")
                return redirect("order")

            # Verificar que el horario esté dentro de las 9 AM y 9 PM
            if not (time(9, 0) <= fecha_hora_pedido.time() <= time(21, 0)):
                messages.error(request, "El horario debe estar entre las 9:00 AM y las 9:00 PM.")
                return redirect("order")

            # Guardar la orden o proceder con el flujo deseado
            # Ejemplo: Pedido.objects.create(...)
            messages.success(request, "Pedido confirmado exitosamente.")
            return redirect("home")
        except ValueError:
            messages.error(request, "Fecha u hora inválida.")
            return redirect("order")

    return redirect("order")

def order(request):
    user_id = request.session.get('user_id')  # Obtén el ID del usuario desde la sesión
    if not user_id:
        return redirect('login')  # Redirige al login si no hay usuario en la sesión

    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return redirect('login')  # Redirige al login si el usuario no existe

    # Obtén los elementos del carrito para este usuario
    carrito_items = Carrito.objects.filter(usuario=usuario).select_related('postre')

    # Calcula el total y el subtotal por elemento
    total = Decimal(0)
    for item in carrito_items:
        item.subtotal = item.postre.precio * item.cantidad
        total += item.subtotal

    # Calcula los puntos equivalentes como Decimal
    puntos_descuento = Decimal(usuario.puntos_acumulados) / Decimal(100)
    total_con_descuento = total - puntos_descuento if total > puntos_descuento else Decimal(0)

    return render(request, 'cart/order.html', {
        'carrito_items': carrito_items,
        'total': total,
        'puntos_descuento': puntos_descuento,
        'total_con_descuento': total_con_descuento,
        'usuario': usuario,
    })

# Vista de favoritos
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
                
                # Redirigir a una página de confirmación o carrito
                return redirect('home')
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

# Vista de la pagina pago
def pago(request):
    return render(request,'pago/pagopagina.html')

# Vista de la pagina de contacto
def contact(request):
    return render(request, 'contact.html')

def soon(request):
    return render(request, 'soon.html')
