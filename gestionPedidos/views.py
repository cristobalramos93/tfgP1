from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth.models import User
from gestionPedidos.models import Paciente,Tratamiento
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "index.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def register(request):
    obj = Tratamiento.objects.all()
    tipo_diabetes = Paciente.TYPES
    if request.method == 'POST':

        """"user = {{request.user.id}}
        obj = Paciente.objects.get(user)
        id_doctor = obj.doctor_id
        doctor_id_id = id_doctor
        buscar el id del medico que da de alta(sin comprobar)
        """""
        password = request.POST['password']
        email = request.POST['email']
        birth_date = request.POST['birth_date']
        #bir = birth_date.isoformat()
        diabetes_type = request.POST['diabetes_type']
        doctor_id_id = request.POST['doctor_id_id']
        treatment_id = request.POST['treatment_id']
        id_treatment = Tratamiento.objects.get(code = treatment_id)
        id_treatment2 = id_treatment.id
        p = Paciente(
            password = make_password(password),
            username = email,
           # birth_date = birth_date,
            diabetes_type = diabetes_type,
            treatment_id = treatment_id,
            doctor_id_id = 12
        )
        p.save()
        return redirect("/")
    else:
        return render(request,'register.html',{'obj': obj, 'tipo_diabetes' : tipo_diabetes})


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