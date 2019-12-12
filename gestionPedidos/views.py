from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth.models import User



def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "index.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username,first_name=first_name,password=password,email = email)
        user.save()
        return redirect("/")
    else:
        return render(request,'register.html')

def login(request):
    # Creamos el formulario de autenticación vacío
    if request.method == "POST":

            # Recuperamos las credenciales validadas
            username = request.POST['username']
            password = request.POST['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html")

def logout(request):
    do_logout(request)

    # Redireccionamos a la portada
    return redirect('/')