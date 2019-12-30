import csv
import io
import os
import pandas as pd
from django.forms import forms
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from Glucmodel.settings import DATABASES

from gestionPacientes.models import Paciente,Tratamiento, Pesos, Calorias
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

    items = Paciente.objects.filter(username = usuario,birth_date__gte=first_date, birth_date__lte= final_date)#saca los datos del usuario seleccionado con las fechas selecionadas
    usuario_seleccionado = Paciente.objects.get(username=usuario) #saca al usuario seleccionado
    itemPeso = Pesos.objects.filter(iduser = usuario_seleccionado.id) ##lo busca en la tabla pesos por el id del usuario seleccionado
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="paciente.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(campos) #aqui poner loas campos que salen en la cabecera

    for obj in items: #tabla de pacientes
        for on in itemPeso: #tabla de pesos
            #aqui poner los resultados del objeto(la lista es campos)
            writer.writerow([obj.user_ptr_id, obj.birth_date, obj.diabetes_type, obj.start_date, obj.doctor_id_id, obj.treatment_id]
           + [ on.peso])
    return response



def upload(request):
    template = "upload.html"

    if request.method == 'GET':
        return render(request, template)

    csv_file = request.FILES['file']
    #si la cabecera es calorias
    calorias(request,csv_file)


    return render(request, template)

def calorias(request,csv_file):
    cal_data = pd.read_csv(csv_file, skiprows=1, sep=',', names=['time', 'calories'])
    # Convert time to time series
    cal_data['time'] = pd.to_datetime("2018-06-13" + ' ' + cal_data['time'])#HAY QUE CAMBIAR FECHA POR TITULO DEL DOC
    cal_data.set_index('time', inplace=True)
    # 5 minutes resampling
    cal_data = cal_data.resample('5T').sum()
    cal_data = cal_data.assign(id_user_id = request.user.paciente.user_ptr_id)

    cal_data.to_csv('calorias.csv')#crea csv de calorias
    csv_file = open('calorias.csv', 'rb')#importa datos del csv de calorias
    data_set = csv_file.read().decode('UTF-8')#lee los datos
    csv_file.close()#cierra el archivo calorias para poder eliminarlo
    os.remove('calorias.csv')#elimina el archivo
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Calorias.objects.update_or_create(
            time=column[0],
            calories=column[1],
            id_user_id=column[2],

        )





