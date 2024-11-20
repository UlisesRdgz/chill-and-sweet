from django.shortcuts import render,redirect
from django.http import HttpResponse


# Vista de la pagina orden
def orden(request):
    return render(request, 'orden/paginaorden.html')

def guardar_orden(request):
    if request.method == 'POST':
        # Obtiene los datos del formulario
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        forma = request.POST.get('forma')
        
        # Guarda los datos en la sesión
        request.session['fecha'] = fecha
        request.session['hora'] = hora
        request.session['forma'] = forma

        print(fecha)
        
        # Redirige a la página de pago
        #return redirect('../../pago')  # Asegúrate de que el nombre de la URL sea correcto
        return redirect('pago:mostrar_pago')

    return redirect('orden:paginaorden')

    #return render(request, 'pagopagina.html')  # Ajusta el nombre del archivo HTML según sea necesario
