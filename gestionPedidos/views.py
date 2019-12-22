import csv

from django.contrib.auth.models import User
from django.forms import forms
from django.http import HttpResponse
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

def prueba(request):
    return render(request,"pruebaBo.html")

def register(request):

    obj = Tratamiento.objects.all()
    tipo_diabetes = Paciente.TYPES
    if request.method == 'POST':

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        birth_date = request.POST['birth_date']
        start_date = request.POST['start_date']

        format_str = '%d/%m/%Y'
        birth_date = datetime.strptime(birth_date, format_str)
        start_date = datetime.strptime(start_date, format_str)
        diabetes_type = request.POST['diabetes_type']
        treatment_id = request.POST['treatment_id']
        treatment_id = Tratamiento.objects.get(code = treatment_id)
        treatment_id = treatment_id.id

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")


        paciente = Paciente(
            password = make_password(password1),
            username = email,
            birth_date = birth_date,
            start_date = start_date,
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

def download(request):
    if request.method == 'POST':
        first_date = request.POST['first_date']
        final_date = request.POST['final_date']

        format_str = '%d/%m/%Y'
        first_date = datetime.strptime(first_date, format_str)
        final_date = datetime.strptime(final_date, format_str)
    else:
        return render(request,'download.html')

    items = Paciente.objects.filter(birth_date = first_date)
    #items = Paciente.objects.filter(birth_date = [first_date,final_date]) esta es la puta mierda que da el error

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="paciente.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(['user_prt_id','birth_date', 'diabetes_type', 'start_date', 'doctor_id_id', 'treatment_id'])

    for obj in items:
        writer.writerow([obj.user_ptr_id, obj.birth_date, obj.diabetes_type, obj.start_date, obj.doctor_id_id, obj.treatment_id])
    return response