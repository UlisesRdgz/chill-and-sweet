from django.shortcuts import render

# Vista de inicio
def index_view(request):
    return render(request, 'index.html')

# Vista de inicio de sesión
def login_view(request):
    return render(request, 'auth/login.html')

# Vista de registro
def register_view(request):
    return render(request, 'auth/register.html')