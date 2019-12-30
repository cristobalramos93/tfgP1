import csv
import io
import os
from wsgiref.util import FileWrapper

import pandas as pd
from djqscsv import write_csv
from django.forms import forms
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from Glucmodel.settings import DATABASES

from gestionPacientes.models import Paciente,Tratamiento, Pesos, Calorias, Ritmo_cardiaco, Pasos
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "index.html")
    # En otro caso redireccionamos al login
    return redirect('/login')

def prueba(request):
    return render(request,"home.html")


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
            return render(request, 'register.html', {'obj': obj, 'tipo_diabetes': tipo_diabetes,'msg': "Las contraseñas deben ser iguales"})

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

        try:
            weight = request.POST['weight']
            paciente_peso = Paciente.objects.get(username=email)
            paciente_peso = paciente_peso.user_ptr_id

            peso = Pesos(
                peso = weight,
                iduser= paciente_peso,
                date = datetime.now()
            )
            peso.save()
        except Exception as e:
            print("no peso")

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


def file(param):
    pass


def download(request):
    id_doctor = request.user.medico.user_ptr_id
    pacientes = Paciente.objects.filter(doctor_id_id=id_doctor)
    if request.method == 'POST':
        first_date = request.POST['first_date']
        final_date = request.POST['final_date']
        campos = request.POST.getlist("casillas[]")
        usuario = request.POST['usuario']
        format_str = '%d/%m/%Y'
        first_date = datetime.strptime(first_date, format_str)
        final_date = datetime.strptime(final_date, format_str)
    else:
        return render(request,'download.html',{'pacientes' : pacientes})

    id_usuario = Paciente.objects.get(username = usuario).id
    df = pd.DataFrame(columns=['time', "id_user_id"])
    for tabla in campos:
        if tabla == "Calorias":
            items = Calorias.objects.filter(id_user_id = id_usuario,time__gte=first_date, time__lte= final_date)
        elif tabla == "Pasos":
            items = Pasos.objects.filter(id_user_id=id_usuario, time__gte=first_date, time__lte=final_date)
        elif tabla == "Ritmo_cardiaco":
            items = Ritmo_cardiaco.objects.filter(id_user_id=id_usuario, time__gte=first_date, time__lte=final_date)

        with open('items.csv', 'wb') as csv_file:
            write_csv(items, csv_file)
        df_aux = pd.read_csv("items.csv")
        df_aux = df_aux.drop(columns = ["ID"])
        df = df.merge(df_aux, on = ['time','id_user_id'], how = 'outer')
        csv_file.close()  # cierra el archivo calorias para poder eliminarlo
        os.remove('items.csv')
    df.to_csv("final.csv")

    with open('final.csv') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = datos.csv'
        os.remove("final.csv")
        return response
    #para hacer un push en git



def upload(request):
    template = "upload.html"

    if request.method == 'GET':
        return render(request, template)

    csv_file = request.FILES['file']
    #si la cabecera es calorias
    nom = csv_file.name.split('_')
    if(nom[2] == "cals" or nom[2] == "heart" or nom[2] == "sleep" or nom[2] == "steps" ):
        msg = fitbit(request,csv_file)


    return render(request, template,{'msg': msg})

def fitbit(request,csv_file):
    nom = csv_file.name.split('_') #sacamos la fecha del nombre del archivo
    tipo = nom[2]
    nom = nom[3].split('.')
    nom = nom[0]
    cal_data = pd.read_csv(csv_file, skiprows=1, sep=',', names=['time', 'calories'])
    # Convert time to time series
    cal_data['time'] = pd.to_datetime(nom + ' ' + cal_data['time'])
    cal_data.set_index('time', inplace=True)
    # 5 minutes resampling
    cal_data = cal_data.resample('5T').sum()
    cal_data = cal_data.assign(id_user_id = request.user.paciente.user_ptr_id)

    cal_data.to_csv('calorias.csv')#crea csv de calorias con los resultados del script
    csv_file = open('calorias.csv', 'rb')#importa datos del csv de calorias
    data_set = csv_file.read().decode('UTF-8')#lee los datos
    csv_file.close()#cierra el archivo calorias para poder eliminarlo
    os.remove('calorias.csv')#elimina el archivo
    io_string = io.StringIO(data_set)
    next(io_string)
    if(tipo == "cals"):
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):#inserta datos en la bd
            _, created = Calorias.objects.update_or_create(
                time=column[0],
                calories=column[1],
                id_user_id=column[2],
            )
        msg = "Calorías subidas con éxito"

    elif(tipo == "heart"):
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):#inserta datos en la bd
            _, created = Ritmo_cardiaco.objects.update_or_create(
                time=column[0],
                heart_rate=column[1],
                id_user_id=column[2],
            )
        msg = "Ritmo cardiaco subido con éxito"

    elif(tipo == "steps"):
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):#inserta datos en la bd
            _, created = Pasos.objects.update_or_create(
                time=column[0],
                steps=column[1],
                id_user_id=column[2],
            )
        msg = "Pasos subidos con éxito"

    else:
        msg = "Error en el archivo"

    return msg



