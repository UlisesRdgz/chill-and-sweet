from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def menu(request):
    return render(request, 'menu.html')

