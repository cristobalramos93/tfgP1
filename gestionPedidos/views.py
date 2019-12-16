from django.contrib.auth.models import User
from django.forms import forms
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth.models import User
from gestionPedidos.models import Paciente,Tratamiento, Pesos
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
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        birth_date = request.POST['birth_date']
        #bir = birth_date.isoformat()
        diabetes_type = request.POST['diabetes_type']
        treatment_id = request.POST['treatment_id']
        treatment_id = Tratamiento.objects.get(code = treatment_id)
        treatment_id = treatment_id.id

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        paciente = Paciente(
            password = make_password(password1),
            username = email,
           # birth_date = birth_date,
            diabetes_type = diabetes_type,
            treatment_id = treatment_id,
            doctor_id_id = request.user.medico.user_ptr_id
        )
        paciente.save()


        weight = request.POST['weight']
        paciente_peso = Paciente.objects.get(username=email)
        paciente_peso = paciente_peso.user_ptr_id

        peso = Pesos(
            peso = weight,
            iduser= paciente_peso,
            date = datetime.now()
        )
        peso.save()
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