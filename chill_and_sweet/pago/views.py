from django.shortcuts import render
from django.http import HttpResponse


# Vista de la pagina pago
def pago(request):
    return render(request,'pago/pagopagina.html')

# pago/views.py
def mostrar_pago(request):

    fecha = request.session.get('fecha', '')
    hora = request.session.get('hora', '')
    forma = request.session.get('forma', '')
   
    print(fecha)
    print(request.session)
    # Pasar los datos al template
    return render(request, 'pago/pagopagina.html', {
        'fecha': fecha,
        'hora': hora,
        'forma': forma
    })
