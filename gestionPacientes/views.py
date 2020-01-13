import csv
import io
import numpy as np
import pandas as pd
from djqscsv import write_csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from gestionPacientes.models import Paciente,Tratamiento, Pesos, Calorias, Ritmo_cardiaco, Pasos, Suenio, Siesta, Siesta_resumen, Suenio_resumen
from gestionPacientes.models import  Bg_reading, Basal_rate, Bolus_type, Bolus_volume_delivered, Bwz_carb_input, Bwz_carb_ratio, Sensor_calibration, Sensor_glucose
from gestionPacientes.models import Cetonas, Insulina_lenta, Insulina_rapida, Glucosa_sangre, Peso, Hito_roche
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
import matplotlib.pyplot as plt
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def enviar_correo(usuario, contrasenia):
    body = "Has sido registrado en Glucmodel\n USUARIO: " + usuario + "\n CONTRASEÑA: " + contrasenia
    email = EmailMessage('Registro Glucmodel', body, to=[usuario])
    email.send()


def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "index.html")
    # En otro caso redireccionamos al login
    return redirect('/login')

def new_password(request):
    template = 'new_password.html'
    if request.method == "POST":
        # Recuperamos las credenciales validadas
        old_pas = request.POST['old_pas']
        new_pas = request.POST['new_pas']
        new_pas2 = request.POST['new_pas2']
        user = authenticate(username=request.user.username, password=old_pas)
        if user is None: #si no existe este usuario
            return render(request,template,{'msg': "La contraseña es erronea"})
        elif new_pas != new_pas2:
            return render(request, template,{'msg': "La nueva contraseña debe coincidir"})
        elif new_pas == old_pas:
            return render(request, template,{'msg': "La contraseña nueva no puede ser la misma que la anterior"})

        else:
            p = Paciente.objects.get(id = request.user.id)
            p.password = make_password(new_pas)
            p.save()
            do_login(request, user)
            return render(request,template,{'msg': "Contraseña cambiada con éxito"})

    else:
        return render(request, template)

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

        if Paciente.objects.filter(username = email).count():
            return render(request,"register.html",{'obj': obj, 'tipo_diabetes': tipo_diabetes,'msg': "El paciente " + email + " ya existe"})

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

            peso = Peso(
                peso = weight,
                id_user_id= paciente_peso,
                time = datetime.now()
            )
            peso.save()
        except Exception as e:
            print("no peso")
        enviar_correo(email,password1)
        return render(request, 'register.html',
                      {'obj': obj, 'tipo_diabetes': tipo_diabetes, 'msg': "Usuario subido con éxito"})

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
            else: #si el nom de usuario o contraseña es incorrecto
                msg = "Error en el usuario o contraseña"
                return render(request, "login.html",{'msg':msg})

    # Si llegamos al final renderizamos el formulario

    return render(request, "login.html")

def logout(request):
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')


def download(request):
    try:
        if request.user.id == request.user.paciente.user_ptr_id:# si es un paciente solo se puede descargar a si mismo
            pacientes = Paciente.objects.filter(id=request.user.id)
            #aqui busco su fecha
            menor = request.user.paciente.first_date
            mayor = request.user.paciente.last_date
            fecha = "Existen registros de la fecha " + str(menor) + " a la fecha " + str(mayor)


    except:
        pacientes = Paciente.objects.all()#puede descargar todos los pacientes
        fecha = None
    if request.method == 'POST':
        first_date = request.POST['first_date'] #esto es solo para ver si se ha completado el formulario, si no se ha completado significa que solo has puesto el nombre de usuario, y va a calcular sus registros

        if 'usuario' in request.POST and first_date == "": #si has seleccionado un usuario
            msg = None
            usuario = request.POST['usuario']
            fecha_min = Paciente.objects.get(username=usuario).first_date
            fecha_max = Paciente.objects.get(username=usuario).last_date

            if(fecha_min == None):
                fecha = None
                msg = "No existen datos de este usuario"
                return render(request, 'download.html', {'pacientes': pacientes, 'msg': msg, 'fecha':fecha,'usuario':usuario})

            else:
                fecha_min = fecha_min.strftime("%d-%m-%Y") #lo paso a string con el formato que queremos
                fecha_max = fecha_max.strftime("%d-%m-%Y")
                fecha = "Existen registros de la fecha " + fecha_min + " a la fecha " + fecha_max
                return render(request, 'download.html', {'pacientes': pacientes, 'msg': msg, 'fecha':fecha,'usuario':usuario})

        #first_date = request.POST['first_date']
        final_date = request.POST['final_date']
        campos = request.POST.getlist("casillas[]")
        if(len(campos) == 0):
            msg = "Selecciona algún dato"
            return render(request, 'download.html', {'pacientes': pacientes, 'msg': msg, 'fecha':fecha})
        try:
            usuario = request.POST['usuario']
        except:
            usuario = Paciente.objects.get(id=request.user.id).username

        format_str = '%d/%m/%Y'
        first_date = datetime.strptime(first_date, format_str)
        final_date = datetime.strptime(final_date, format_str)
    else:
        return render(request,'download.html',{'pacientes':pacientes, 'fecha':fecha})

    id_usuario = Paciente.objects.get(username = usuario).id
    df = pd.DataFrame(columns=['time', "id_user_id"])
    for tabla in campos:
        items = eval(tabla).objects.filter(id_user_id = id_usuario,time__gte=first_date, time__lte= final_date)
        with open('items.csv', 'wb') as csv_file:
            write_csv(items, csv_file)
        df_aux = pd.read_csv("items.csv")
        df_aux = df_aux.drop(columns = ["ID"])
        df = df.merge(df_aux, on = ['time','id_user_id'], how = 'outer')
        csv_file.close()  # cierra el archivo calorias para poder eliminarlo
        os.remove('items.csv')
    df = df.set_index("time", drop=True)
    df = df.sort_index()
    if 'ver' in request.POST:
        disenio = '{% extends "base.html" %}\n'
        disenio += "{% load staticfiles i18n %}\n"
        disenio += '{% block css %}\n'
        disenio += '<link href="{% static "gestionPacientes/static/css/freelancer.css" %}" rel="stylesheet" type="text/css">\n'
        disenio += '{% endblock css %}\n'
        disenio += "{% block title %}Ver Datos{% endblock title %}\n"
        disenio += "{% block content %}\n"
        tabla = df.to_html(classes='table table-striped table-hover')
        disenio += tabla
        disenio += "\n"
        disenio += "{% endblock content %}"
        with open("gestionPacientes/plantillas/table.html", "w") as file:
            file.write(disenio)
        return render(request,"table.html")
    elif 'descarga' in request.POST: #si es descargar
        df.to_csv("final.csv")
        with open('final.csv') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename ='+ str(id_usuario) +'_'+ usuario + '.csv'
            os.remove("final.csv")
            return response
    elif 'grafico' in request.POST:
        try:
            df.pop('id_user_id')#no quiero mostrar el id en el grafico
            df.plot()
            plt.savefig(BASE_DIR + "/gestionPacientes/static/img/grafico.png")
            html = '{% extends "base.html" %}\n'
            html += "{% load staticfiles i18n %}\n"
            html += "{% block content %}\n"
            html += '<img class="plot" src="{{ figure }}"/>\n'
            html += "{% endblock content %}"

            with open('gestionPacientes/plantillas/grafico.html', 'w') as f:
                f.write(html)
            return render(request, 'grafico.html',{'figure': "../static/img/grafico.png"})
        except:
            return render(request,'download.html',{'pacientes':pacientes,'fecha':fecha,'msg': "La tabla está vacía"})
    return render(request,'download.html',{'pacientes':pacientes, 'fecha':fecha})


def upload(request):
    template = "upload.html"
    try: #si es paceinte
        if request.user.id == request.user.paciente.user_ptr_id:
            pacientes = "nada"

    except: # si es un medicco o investigador o admin
        pacientes = Paciente.objects.all()

    if request.method == 'GET':
        return render(request, template,{'pacientes' : pacientes})

    csv_file = request.FILES['file']
    tipo_archivo = request.POST['tipo_archivo'] #nombre del usuario
    nom = csv_file.name.split('_')
    extension = csv_file.name.split('.')
    if extension[1] != 'csv':
        return render(request, template, {'pacientes': pacientes, 'msg': "El archivo debe tener la extensión .csv"})

    try:
        usuario = request.user.paciente.user_ptr_id # si es u paciente, saco su id
    except:# si es un  medico, el id lo saco del usuario seleccionado
        usuario = request.POST['usuario'] #nombre del usuario
        usuario = Paciente.objects.get(username=usuario).id
    try:
        if tipo_archivo == "FITBIT CALORÍAS" or tipo_archivo == "FITBIT RITMO CARDÍACO" or tipo_archivo == "FITBIT PASOS" :
            msg, fecha_min, fecha_max = fitbit(request,csv_file,usuario,tipo_archivo)
        elif tipo_archivo == "FITBIT RESUMEN SUEÑO" or tipo_archivo == "FITBIT RESUMEN SIESTA":
            msg = sleep_nap_resumen(request,csv_file,usuario,tipo_archivo)
        elif tipo_archivo == "FITBIT SIESTA" or tipo_archivo == "FITBIT SUEÑO":
            msg, fecha_min, fecha_max = sleep_nap(request,csv_file,usuario,tipo_archivo)
        elif(tipo_archivo == "MEDTRONIC"):
            msg, fecha_min, fecha_max = medtronic(request,csv_file,usuario)
        elif (tipo_archivo == "FREE STYLE SENSOR"):
            msg, fecha_min, fecha_max = free_style_sensor(request, csv_file, usuario)
        elif (tipo_archivo == "ROCHE"):
            msg, fecha_min, fecha_max = roche(request, csv_file, usuario)

        #Guarda las fechas maximas y minimas de cada paciente al insertas datos en la BD
        paciente = Paciente.objects.get(user_ptr_id=usuario)
        paciente_fecha_min = paciente.first_date
        paciente_fecha_max = paciente.last_date
        if (paciente_fecha_min is None) or (fecha_min < paciente_fecha_min):
            paciente.first_date = fecha_min
            paciente.save()
        if (paciente_fecha_max is None) or (fecha_max > paciente_fecha_max):
            paciente.last_date = fecha_max
            paciente.save()

    except:
        msg = "Los datos no corresponden con el nombre seleccionado"
    return render(request, template,{'msg': msg,'pacientes': pacientes})

def roche(request, csv_file,usuario):
    try:
        roche = pd.read_csv(csv_file, sep=";", encoding="ISO-8859-1", usecols=["Fecha", "Hora", "Hito", "Glucemia",
                                                                        "Tipo de Bolo", "Unidades", "Dosis Basal (UI/H)",
                                                                        "Eventos S.I."],
                            parse_dates={'Time': ['Fecha', 'Hora']}, dayfirst=True)

        roche['Time'] = roche['Time'].dt.round('5min')

        roche.set_index('Time', inplace=True)

        roche.sort_index(inplace=True)

        roche.drop_duplicates(inplace=True)

        roche["Dosis Basal (UI/H)"].loc[roche["Eventos S.I."] == "Parada"] = 0

        roche_str = roche[["Hito", "Tipo de Bolo", "Eventos S.I."]]
        roche_int = roche[["Glucemia", "Unidades", "Dosis Basal (UI/H)"]]
        # Cuando el valor de "Eventos S.I." es Parada dosis basal a 0
        roche_int = roche.resample('5T').mean()

        roche = roche_int.merge(roche_str, left_index=True, right_index=True, how="outer")

        roche['Dosis Basal (UI/H)'] = roche['Dosis Basal (UI/H)'] / 12
        aux_br = roche['Dosis Basal (UI/H)'][0]
        for i in range(1, roche.shape[0]):
            if np.isnan(roche['Dosis Basal (UI/H)'][i]):
                roche.iloc[i, roche.columns.get_loc('Dosis Basal (UI/H)')] = aux_br
            else:
                aux_br = roche.iloc[i, roche.columns.get_loc('Dosis Basal (UI/H)')]
        roche.pop("Eventos S.I.")

        fecha_min = roche.index.min()
        fecha_max = roche.index.max()

        roche.to_csv('roche.csv')  # crea csv con los resultados del script
        csv_file = open('roche.csv', 'rb')  # importa datos del csv
        data_set = csv_file.read().decode('UTF-8')  # lee los datos
        csv_file.close()  # cierra el archivo para poder eliminarlo
        os.remove('roche.csv')  # elimina el archivo
        io_string = io.StringIO(data_set)
        next(io_string)
        try:
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                if column[1] != "":
                    _, created = Glucosa_sangre.objects.update_or_create(
                        time=column[0],
                        id_user_id=usuario,
                        defaults={"glucosa_sangre_mg_dL": column[1], }
                    )
                if column[2] != "":
                    _, created = Bwz_carb_input.objects.update_or_create(
                        time=column[0],
                        id_user_id=usuario,
                        defaults={"bwz_carb_input_EX": column[2], }
                    )
                if column[3] != "":
                    _, created = Basal_rate.objects.update_or_create(
                        time=column[0],
                        id_user_id=usuario,
                        defaults={"basal_rate_U_h": column[3], }
                    )
                if column[4] != "":
                    _, created = Hito_roche.objects.update_or_create(
                        time=column[0],
                        id_user_id=usuario,
                        defaults={"hito_roche": column[4], }
                    )
                if column[5] != "":
                    _, created = Bolus_type.objects.update_or_create(
                        time=column[0],
                        id_user_id=usuario,
                        defaults={"bolus_type": column[5], }
                    )
            msg = "Datos de la bomba de Roche subidos con exito"
        except:
            msg = "Error en la subida de datos de la bomba de Roche"
    except:
        msg = "Error en el tratamiento de datos de la bomba de Roche"
    return msg, fecha_min, fecha_max

def medtronic(request, csv_file,usuario):
    # Obtain the row of data division if exists
    medtron_data = pd.read_csv(csv_file, skiprows=6, sep=';')
    medtron_data.to_csv('medtron.csv')#creo para poder leer mas abajo
    medtron_data.drop('Index', axis=1, inplace=True)
    str_index = medtron_data['Date'].str.find('Date').idxmax()

    if len(medtron_data) != (str_index + 1):
        # Load first data set
        medtron_data_1 = pd.read_csv('medtron.csv', engine='python',
                                     skipfooter=medtron_data.shape[0] - str_index + 3,
                                     usecols=['Date', 'Time', 'BG Reading (mg/dL)', 'Basal Rate (U/h)',
                                              'Bolus Volume Delivered (U)', 'BWZ Carb Ratio (U/Ex)',
                                              'BWZ Carb Input (exchanges)', 'Sensor Calibration BG (mg/dL)'],
                                     parse_dates={'Hora': ['Date', 'Time']}, dayfirst=True)
        # Round data to the closest five minutes
        medtron_data_1['Hora'] = medtron_data_1['Hora'].dt.round('5min')
        # Convert time to time series and order DataFrame
        medtron_data_1.set_index('Hora', inplace=True)
        medtron_data_1.sort_index(inplace=True)
        # Join equal data time only on a row
        medtron_data_1 = medtron_data_1.groupby(level=0).sum(min_count=1)
        # Delete repeated data
        medtron_data_1.drop_duplicates(inplace=True)
        # 5 minutes resampling
        medtron_data_1 = medtron_data_1.resample('5T').mean()
        # Add data to basal rate
        medtron_data_1['Basal Rate (U/h)'] = medtron_data_1['Basal Rate (U/h)']/12
        aux_br = medtron_data_1['Basal Rate (U/h)'][0]
        for i in range(1, medtron_data_1.shape[0]):
            if np.isnan(medtron_data_1['Basal Rate (U/h)'][i]):
                medtron_data_1.iloc[i, medtron_data_1.columns.get_loc('Basal Rate (U/h)')] = aux_br
            else:
                aux_br = medtron_data_1.iloc[i, medtron_data_1.columns.get_loc('Basal Rate (U/h)')]
        # Add Bolys Type row (string values)
        bolus = pd.read_csv('medtron.csv', engine='python',
                            skipfooter=medtron_data.shape[0] - str_index + 3,
                            usecols=['Date', 'Time', 'Bolus Type'],
                            parse_dates={'Hora': ['Date', 'Time']}, dayfirst=True)
        # Convert time to time series and order DataFrame
        bolus['Hora'] = bolus['Hora'].dt.round('5T')
        bolus.drop_duplicates(inplace=True)
        mapping = {'Normal': 1, np.nan: 0}
        bolus = bolus.replace({'Bolus Type': mapping})
        bolus.set_index('Hora', inplace=True)
        bolus.sort_index(inplace=True)
        bolus = bolus.resample('5T').sum()
        mapping = {0: np.nan, 1: 'Normal', 2: 'Normal', 3: 'Normal', 4: 'Normal', 5: 'Normal'}
        bolus = bolus.replace({'Bolus Type': mapping})
        # Merge bolus type and Medtronic data
        medtron_data_1 = pd.merge(medtron_data_1, bolus, left_index=True, right_index=True, how='outer')
        col = medtron_data_1['Bolus Type']
        medtron_data_1.pop('Bolus Type')
        medtron_data_1.insert(2, col.name, col)

        medtron_data_2 = pd.read_csv('medtron.csv', engine='python', skiprows=str_index + 1,
                                     usecols=['Date', 'Time', 'Sensor Glucose (mg/dL)'],
                                     parse_dates={'Hora': ['Date', 'Time']}, dayfirst=True)
        medtron_data_2.set_index('Hora', inplace=True)
        medtron_data_2.sort_index(inplace=True)
        # 5 minutes resampling
        medtron_data_2 = medtron_data_2.resample('5T').mean()
    else:
        # Load first data set
        medtron_data_1 = pd.read_csv('medtron.csv', engine='python',
                                     skipfooter=medtron_data.shape[0] - str_index + 3,
                                     usecols=['Date', 'Time', 'BG Reading (mg/dL)', 'Basal Rate (U/h)',
                                              'Bolus Volume Delivered (U)', 'BWZ Carb Ratio (U/Ex)',
                                              'BWZ Carb Input (exchanges)', 'Sensor Calibration BG (mg/dL)'],
                                     parse_dates={'Hora': ['Date', 'Time']}, dayfirst=True)
        # Round data to the closest five minutes
        medtron_data_1['Hora'] = medtron_data_1['Hora'].dt.round('5min')
        # Convert time to time series and order DataFrame
        medtron_data_1.set_index('Hora', inplace=True)
        medtron_data_1.sort_index(inplace=True)
        # Join equal data time only on a row
        medtron_data_1 = medtron_data_1.groupby(level=0).sum(min_count=1)
        # Delete repeated data
        medtron_data_1.drop_duplicates(inplace=True)
        # 5 minutes resampling
        medtron_data_1 = medtron_data_1.resample('5T').mean()
        # Add data to basal rate
        medtron_data_1['Basal Rate (U/h)'] = medtron_data_1['Basal Rate (U/h)'] / 12
        aux_br = medtron_data_1['Basal Rate (U/h)'][0]
        for i in range(1, medtron_data_1.shape[0]):
            if np.isnan(medtron_data_1['Basal Rate (U/h)'][i]):
                medtron_data_1.iloc[i, medtron_data_1.columns.get_loc('Basal Rate (U/h)')] = aux_br
            else:
                aux_br = medtron_data_1.iloc[i, medtron_data_1.columns.get_loc('Basal Rate (U/h)')]
        medtron_data_2 = None

    fecha_min = medtron_data_1.index.min()
    fecha_max = medtron_data_1.index.max()

    for col in medtron_data_1.columns:
        col_csv = medtron_data_1[col].dropna()
        col_csv.to_csv('medtron.csv')  # crea csv con los resultados del script
        csv_file = open('medtron.csv', 'rb')  # importa datos del csv
        data_set = csv_file.read().decode('UTF-8')  # lee los datos
        csv_file.close()  # cierra el archivo para poder eliminarlo
        os.remove('medtron.csv')  # elimina el archivo
        io_string = io.StringIO(data_set)
        next(io_string)
        if col == "BG Reading (mg/dL)":
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                _, created = Bg_reading.objects.update_or_create(
                    time=column[0],
                    id_user_id=usuario,
                    defaults={"bg_reading_mg_dL": column[1], }
                )
        elif col == "Basal Rate (U/h)":
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                _, created = Basal_rate.objects.update_or_create(
                    time=column[0],
                    id_user_id=usuario,
                    defaults={"basal_rate_U_h": column[1], }
                )
        elif col == "Bolus Type":
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                _, created = Bolus_type.objects.update_or_create(
                    time=column[0],
                    id_user_id=usuario,
                    defaults={"bolus_type": column[1], }
                )
        elif col == "Bolus Volume Delivered (U)":
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                _, created = Bolus_volume_delivered.objects.update_or_create(
                    time=column[0],
                    id_user_id=usuario,
                    defaults={"bolus_volume_delivered_U": column[1], }
                )
        elif col == "BWZ Carb Ratio (U/Ex)":
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                _, created = Bwz_carb_ratio.objects.update_or_create(
                    time=column[0],
                    id_user_id=usuario,
                    defaults={"bwz_carb_ratio_U_EX": column[1], }
                )
        elif col == "BWZ Carb Input (exchanges)":
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                _, created = Bwz_carb_input.objects.update_or_create(
                    time=column[0],
                    id_user_id=usuario,
                    defaults={"bwz_carb_input_EX": column[1], }
                )
        elif col == "Sensor Calibration BG (mg/dL)":
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                _, created = Sensor_calibration.objects.update_or_create(
                    time=column[0],
                    id_user_id=usuario,
                    defaults={"sensor_calibration_mg_dL": column[1], }
                )
    if medtron_data_2 is not None:
        medtron_data_2 = medtron_data_2.dropna()
        medtron_data_2.to_csv('medtron.csv')  # crea csv con los resultados del script
        csv_file = open('medtron.csv', 'rb')  # importa datos del csv
        data_set = csv_file.read().decode('UTF-8')  # lee los datos
        csv_file.close()  # cierra el archivo para poder eliminarlo
        os.remove('medtron.csv')  # elimina el archivo
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
            _, created = Sensor_glucose.objects.update_or_create(
                time=column[0],
                id_user_id=usuario,
                defaults={"sensor_glucose_mg_dL": column[1], }
            )
        msg = "Datos del sensor y la bomba de medtronic subidos con exito"
    else:
        msg = "Datos de la bomba de medtronic subidos con exito"

    return msg, fecha_min, fecha_max

def sleep_nap_resumen(request, csv_file,usuario,tipo_archivo):
    data_set = csv_file.read().decode('UTF-8')  # lee los datos
    io_string = io.StringIO(data_set)
    next(io_string)
    if tipo_archivo == "FITBIT RESUMEN SUEÑO":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
            _, created = Suenio_resumen.objects.update_or_create(
                time=column[2],
                id_user_id=usuario,
                defaults={
                    "sleep_main_sleep": column[3],
                    "sleep_efficiency": column[4],
                    "sleep_duration": column[5],
                    "sleep_minutes_asleep": column[6],
                    "sleep_minutes_light": column[7],
                    "sleep_minutes_deep": column[8],
                    "sleep_minutes_rem": column[9],
                    "sleep_minutes_awake": column[10],
                    "sleep_minutes_in_bed": column[11],
                }
            )
        msg = "Resumen de sueño subido con éxito"

    elif tipo_archivo == "FITBIT RESUMEN SIESTA":

        for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
            tamanio = len(column)
            if tamanio == 12:
                _, created = Siesta_resumen.objects.update_or_create(
                    time=column[2],
                    id_user_id=usuario,
                    defaults= {
                        "nap_main_sleep":column[3],
                        "nap_efficiency":column[4],
                        "nap_duration":column[5],
                        "nap_minutes_asleep":column[6],
                        "nap_minutes_light":column[7],
                        "nap_minutes_deep":column[8],
                        "nap_minutes_rem":column[9],
                        "nap_minutes_awake":column[10],
                        "nap_minutes_in_bed":column[11],
                        "nap_minutes_restless": -1,

                    }
                )
            elif tamanio == 10:
                _, created = Siesta_resumen.objects.update_or_create(
                    time=column[2],
                    id_user_id=usuario,
                    defaults= {
                        "nap_main_sleep":column[3],
                        "nap_efficiency":column[4],
                        "nap_duration":column[5],
                        "nap_minutes_asleep":column[6],
                        "nap_minutes_awake": column[7],
                        "nap_minutes_restless": column[8],
                        "nap_minutes_in_bed":column[9],
                        "nap_minutes_light": -1,
                        "nap_minutes_deep": -1,
                        "nap_minutes_rem": -1,
                    }
                )

        msg = "Resumen de siesta subido con éxito"
    else:
        msg = "Error en el archivo"
    return msg


def sleep_nap(request, csv_file,usuario,tipo_archivo):

    # Data file name
    sl_data = pd.read_csv(csv_file, skiprows=1, sep=',', names=['Hora', 'Duracion (m)', 'Estado'])

    # Convert from seconds to minutes sleep time
    sl_data['Duracion (m)'] = sl_data['Duracion (m)'] / 60

    # Convert time to time series
    sl_data['Hora'] = pd.to_datetime(sl_data['Hora'])

    # Create new DataFrame to store treated data
    sl_treat_data = pd.DataFrame()

    # Create 1/2 minute frequency time series and fill with nan values
    sl_treat_data['Hora'] = pd.date_range(start=sl_data['Hora'].min(), end=sl_data['Hora'].max(), freq='0.5T')
    sl_treat_data['Estado'] = np.nan

    # Add to every row the sleep state. Then, the most repeated word is the one
    # set as the sleep state for those five minutes.
    j = 1

    for i in range(sl_treat_data.shape[0]):
        if sl_treat_data['Hora'][i] < sl_data['Hora'][j]:
            sl_treat_data.loc[i, 'Estado'] = sl_data.loc[j - 1, 'Estado']
        else:
            sl_treat_data.loc[i, 'Estado'] = sl_data.loc[j, 'Estado']
            j += 1

    sl_treat_data.set_index('Hora', inplace=True)
    sl_treat_data = sl_treat_data.resample('5T').sum()

    for i in range(sl_treat_data.shape[0]):
        w = sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')].count('w')
        l = sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')].count('l')
        r = sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')].count('r')
        d = sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')].count('d')

        if w >= l and w >= r and w >= d:
            sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')] = 'wake'
        if l >= w and l >= r and l >= d:
            sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')] = 'light'
        if r >= w and r >= l and r >= d:
            sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')] = 'rem'
        if d >= w and d >= l and d >= r:
            sl_treat_data.iloc[i, sl_treat_data.columns.get_loc('Estado')] = 'deep'
    #sl_treat_data = sl_treat_data.assign(id_user_id = request.user.paciente.user_ptr_id)

    fecha_min = sl_treat_data.index.min()
    fecha_max = sl_treat_data.index.max()

    sl_treat_data.to_csv('sleep.csv')  # crea csv de calorias con los resultados del script
    csv_file = open('sleep.csv', 'rb')  # importa datos del csv de calorias
    data_set = csv_file.read().decode('UTF-8')  # lee los datos
    csv_file.close()  # cierra el archivo calorias para poder eliminarlo
    os.remove('sleep.csv')  # elimina el archivo
    io_string = io.StringIO(data_set)
    next(io_string)
    if tipo_archivo == "FITBIT SUEÑO":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
            _, created = Suenio.objects.update_or_create(
                time=column[0],
                id_user_id=usuario,
                defaults={"sleep_state": column[1], }
            )
        msg = "Sueño subido con éxito"

    elif tipo_archivo == "FITBIT SIESTA":
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
            _, created = Siesta.objects.update_or_create(
                time=column[0],
                id_user_id=usuario,
                defaults={"nap_state": column[1], }

            )
        msg = "Siesta subida con éxito"
    else:
        msg = "Error en el archivo"
    return msg, fecha_min, fecha_max
def free_style_sensor(request,csv_file,usuario):
    try:
        gluc_data = pd.read_csv(csv_file, skiprows=1, sep=';', usecols=['Hora', 'Glucosa leída (mg/dL)', 'Histórico glucosa (mg/dL)', 'Insulina de acción rápida (unidades)',
                                                                        'Carbohidratos (raciones)','Insulina de acción lenta (unidades)',
                                                                        'Glucosa de la tira (mg/dL)', 'Cetonas (mmol/L)'])

        # Convert time to time series
        gluc_data['Hora'] = pd.to_datetime(gluc_data['Hora'])

        # Sort data by date
        gluc_data = gluc_data.sort_values(by=['Hora'])

        # Round data to the closest five minutes
        gluc_data['Hora'] = gluc_data['Hora'].dt.round('5min')
        gluc_data.set_index('Hora', inplace=True)

        # 5 minutes sampling
        gluc_data = gluc_data.resample('5min').mean()

        gluc_data_1 = gluc_data[["Glucosa leída (mg/dL)", "Histórico glucosa (mg/dL)"]].fillna(0)
        gluc_data_1 = gluc_data_1.assign(Glucosa_total=0).apply(juntar_glu, axis='columns')
        gluc_data["Glucosa_total"] = gluc_data_1["Glucosa_total"]
        gluc_data.pop("Glucosa leída (mg/dL)")
        gluc_data.pop("Histórico glucosa (mg/dL)")

        fecha_min = gluc_data.index.min()
        fecha_max = gluc_data.index.max()

        for col in gluc_data.columns:
            col_csv = gluc_data[col].dropna()
            col_csv.to_csv('free.csv')  # crea csv con los resultados del script
            csv_file = open('free.csv', 'rb')  # importa datos del csv
            data_set = csv_file.read().decode('UTF-8')  # lee los datos
            csv_file.close()  # cierra el archivo para poder eliminarlo
            os.remove('free.csv')  # elimina el archivo
            io_string = io.StringIO(data_set)
            try:
                next(io_string)
                if col == "Insulina de acción rápida (unidades)":
                    for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                        _, created = Insulina_rapida.objects.update_or_create(
                            time=column[0],
                            id_user_id=usuario,
                            defaults={"insulina_rapida_U": column[1], }
                        )
                elif col == "Carbohidratos (raciones)":
                    for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                        _, created = Bwz_carb_input.objects.update_or_create(
                            time=column[0],
                            id_user_id=usuario,
                            defaults={"bwz_carb_input_EX": column[1], }
                        )
                elif col == "Insulina de acción lenta (unidades)":
                    for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                        _, created = Insulina_lenta.objects.update_or_create(
                            time=column[0],
                            id_user_id=usuario,
                            defaults={"insulina_lenta_U": column[1], }
                        )
                elif col == "Glucosa de la tira (mg/dL)":
                    for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                        _, created = Glucosa_sangre.objects.update_or_create(
                            time=column[0],
                            id_user_id=usuario,
                            defaults={"glucosa_sangre_mg_dL": column[1], }
                        )
                elif col == "Cetonas (mmol/L)":
                    for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                        _, created = Cetonas.objects.update_or_create(
                            time=column[0],
                            id_user_id=usuario,
                            defaults={"cetonas_mmol_L": column[1], }
                        )
                elif col == "Glucosa_total":
                    for column in csv.reader(io_string, delimiter=',', quotechar="|"):  # inserta datos en la bd
                        _, created = Sensor_glucose.objects.update_or_create(
                            time=column[0],
                            id_user_id=usuario,
                            defaults={"sensor_glucose_mg_dL": column[1], }
                        )
                msg = "Datos de freestyle subidos con éxito"
            except:
                print("columna vacia")
    except:
        msg = "Error en el tipo de datos de freestyle"
    return msg, fecha_min, fecha_max

def juntar_glu(r):
    if (r["Glucosa leída (mg/dL)"] > 0) & (r["Histórico glucosa (mg/dL)"] > 0):
        r.Glucosa_total = (r["Glucosa leída (mg/dL)"] + r["Histórico glucosa (mg/dL)"])/2
    elif r["Glucosa leída (mg/dL)"] > 0:
        r.Glucosa_total = r["Glucosa leída (mg/dL)"]
    elif r["Histórico glucosa (mg/dL)"] > 0:
        r.Glucosa_total = r["Histórico glucosa (mg/dL)"]
    else:
        r.Glucosa_total = np.nan
    return r

def fitbit(request,csv_file,usuario,tipo_archivo):
    nom = csv_file.name.split('_')  # sacamos la fecha del nombre del archivo
    nom = nom[3].split('.')
    nom = nom[0]
    cal_data = pd.read_csv(csv_file, skiprows=1, sep=',', names=['time', 'calories'])
    cal_data['time'] = pd.to_datetime(nom + ' ' + cal_data['time'])
    # Convert time to time series
    cal_data.set_index('time', inplace=True)
    # 5 minutes resampling
    if(tipo_archivo == "FITBIT RITMO CARDÍACO"):
        cal_data = cal_data.resample('5T').mean()
    else:
        cal_data = cal_data.resample('5T').sum()

    #cal_data = cal_data.assign(id_user_id = request.user.paciente.user_ptr_id)

    fecha_min = cal_data.index.min()
    fecha_max = cal_data.index.max()

    cal_data.to_csv('calorias.csv')#crea csv de calorias con los resultados del script
    csv_file = open('calorias.csv', 'rb')#importa datos del csv de calorias
    data_set = csv_file.read().decode('UTF-8')#lee los datos
    csv_file.close()#cierra el archivo calorias para poder eliminarlo
    os.remove('calorias.csv')#elimina el archivo
    io_string = io.StringIO(data_set)
    next(io_string)
    if(tipo_archivo == "FITBIT CALORÍAS"):
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):#inserta datos en la bd
            _, created = Calorias.objects.update_or_create(
                time=column[0],
                id_user_id=usuario,
                defaults={
                    "calories" : column[1],
                }
            )
        msg = "Calorías subidas con éxito"

    elif(tipo_archivo == "FITBIT RITMO CARDÍACO"):
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):#inserta datos en la bd
            _, created = Ritmo_cardiaco.objects.update_or_create(
                time=column[0],
                id_user_id=usuario,
                defaults={
                    "heart_rate": column[1],
                }
            )
        msg = "Ritmo cardiaco subido con éxito"

    elif(tipo_archivo == "FITBIT PASOS"):
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):#inserta datos en la bd
            _, created = Pasos.objects.update_or_create(
                time=column[0],
                id_user_id=usuario,
                defaults={"steps": column[1], }

            )
        msg = "Pasos subidos con éxito"

    else:
        msg = "Error en el archivo"

    return msg, fecha_min, fecha_max



