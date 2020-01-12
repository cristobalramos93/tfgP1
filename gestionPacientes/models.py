# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class CasosFormacion(models.Model):
    id = models.IntegerField(primary_key=True)
    alcohol = models.IntegerField(blank=True, null=True)
    blobrecs = models.TextField(db_column='blobRecs', blank=True, null=True)  # Field name made lowercase.
    cetoacidosis = models.IntegerField(db_column='Cetoacidosis', blank=True, null=True)  # Field name made lowercase.
    cetonicos = models.IntegerField(blank=True, null=True)
    conocimientos_infor = models.IntegerField(blank=True, null=True)
    control_alimentacion = models.IntegerField(blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    frecuencia_deporte = models.IntegerField(blank=True, null=True)
    glicosilada = models.IntegerField(blank=True, null=True)
    glucemia_postdeporte = models.IntegerField(blank=True, null=True)
    hiperglucemia = models.IntegerField(blank=True, null=True)
    hipoglucemia = models.IntegerField(blank=True, null=True)
    indice_glucemico = models.IntegerField(blank=True, null=True)
    intensidad_deporte = models.IntegerField(blank=True, null=True)
    moodle = models.IntegerField(blank=True, null=True)
    perfiles = models.IntegerField(blank=True, null=True)
    practica_deporte = models.IntegerField(blank=True, null=True)
    sense = models.IntegerField(blank=True, null=True)
    situaciones_tensas = models.IntegerField(blank=True, null=True)
    tomas_extras = models.IntegerField(blank=True, null=True)

    class Meta:

        db_table = 'casos_formacion'


class CasosSeguimiento(models.Model):
    caseid = models.AutoField(db_column='caseID', primary_key=True)  # Field name made lowercase.
    blobrecs = models.TextField(db_column='blobRecs', blank=True, null=True)  # Field name made lowercase.
    cetonicos = models.IntegerField(blank=True, null=True)
    ejercicio = models.IntegerField(blank=True, null=True)
    fondoojos = models.IntegerField(db_column='fondoOjos', blank=True, null=True)  # Field name made lowercase.
    hba1c = models.IntegerField(blank=True, null=True)
    imc = models.IntegerField(blank=True, null=True)
    h1 = models.IntegerField(blank=True, null=True)
    h2 = models.CharField(max_length=45, blank=True, null=True)
    h3 = models.CharField(max_length=45, blank=True, null=True)
    h4 = models.CharField(max_length=45, blank=True, null=True)
    h5 = models.CharField(max_length=45, blank=True, null=True)
    h6 = models.CharField(max_length=45, blank=True, null=True)
    h7 = models.CharField(max_length=45, blank=True, null=True)
    h8 = models.CharField(max_length=45, blank=True, null=True)
    h9 = models.CharField(max_length=45, blank=True, null=True)
    h10 = models.CharField(max_length=45, blank=True, null=True)
    h11 = models.CharField(max_length=45, blank=True, null=True)
    h12 = models.CharField(max_length=45, blank=True, null=True)
    h13 = models.CharField(max_length=45, blank=True, null=True)
    h14 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:

        db_table = 'casos_seguimiento'


class DestinoDoc(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45)  # Field name made lowercase.

    class Meta:

        db_table = 'destino_doc'


class Dietas(models.Model):
    clave = models.BigAutoField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.
    moment = models.IntegerField(db_column='MOMENT', blank=True, null=True)  # Field name made lowercase.
    observations = models.CharField(db_column='OBSERVATIONS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    raciones = models.FloatField(db_column='RACIONES', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'dietas'



class Documentaciones(models.Model):
    clave = models.BigAutoField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    fichero = models.TextField(db_column='FICHERO', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FILESIZE', blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.
    tipodestino = models.BigIntegerField(db_column='TIPODESTINO', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filetype = models.CharField(db_column='FILETYPE', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'documentaciones'


class Ejercicios(models.Model):
    clave = models.BigAutoField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='LEVEL', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'ejercicios'


class Ficherosexportados(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='FECHA', blank=True, null=True)  # Field name made lowercase.
    filepath = models.CharField(db_column='FILEPATH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'ficherosexportados'


class GestionpedidosArticulos(models.Model):
    nombre = models.CharField(max_length=30)
    seccion = models.CharField(max_length=30)
    precio = models.IntegerField()

    class Meta:

        db_table = 'gestionpedidos_articulos'


class GestionpedidosClientes(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    telefono = models.CharField(max_length=7)

    class Meta:

        db_table = 'gestionpedidos_clientes'


class GestionpedidosPedidos(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField()
    entregado = models.IntegerField()

    class Meta:

        db_table = 'gestionpedidos_pedidos'


class Glucemias(models.Model):
    clave = models.BigAutoField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.
    moment = models.IntegerField(db_column='MOMENT', blank=True, null=True)  # Field name made lowercase.
    observations = models.CharField(db_column='OBSERVATIONS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    value = models.FloatField(db_column='VALUE', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'glucemias'


class Insulinas(models.Model):
    clave = models.BigAutoField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.
    moment = models.IntegerField(db_column='MOMENT', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    value = models.FloatField(db_column='VALUE', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'insulinas'


class MensajesUsuario(models.Model):
    mensajeid = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nuevo = models.IntegerField(blank=True, null=True)
    recomendacionid = models.IntegerField(blank=True, null=True)
    userid = models.BigIntegerField(blank=True, null=True)

    class Meta:

        db_table = 'mensajes_usuario'


class Modelos(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modelo = models.CharField(db_column='MODELO', max_length=512)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='FECHA')  # Field name made lowercase.
    idpaciente = models.IntegerField(db_column='IDPACIENTE')  # Field name made lowercase.

    class Meta:

        db_table = 'modelos'


class Momentos(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45)  # Field name made lowercase.
    hourfrom = models.SmallIntegerField(db_column='HOURFROM', blank=True, null=True)  # Field name made lowercase.
    hourto = models.SmallIntegerField(db_column='HOURTO', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'momentos'


class NivelEje(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45)  # Field name made lowercase.

    class Meta:

        db_table = 'nivel_eje'


class Pesos(models.Model):
    clave = models.BigAutoField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.
    peso = models.FloatField(db_column='PESO', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'pesos'


class Pruebas(models.Model):
    clave = models.BigAutoField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    fichero = models.TextField(db_column='FICHERO', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FILESIZE', blank=True, null=True)  # Field name made lowercase.
    iduser = models.BigIntegerField(db_column='IDUSER', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='TYPE', blank=True, null=True)  # Field name made lowercase.
    filetype = models.CharField(db_column='FILETYPE', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'pruebas'


class Recomendaciones(models.Model):
    asunto = models.CharField(max_length=255, blank=True, null=True)
    seccion = models.CharField(max_length=255, blank=True, null=True)
    texto = models.TextField(blank=True, null=True)

    class Meta:

        db_table = 'recomendaciones'


class TipoEje(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45)  # Field name made lowercase.

    class Meta:

        db_table = 'tipo_eje'


class TipoIns(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45)  # Field name made lowercase.

    class Meta:

        db_table = 'tipo_ins'


class TipoPru(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45)  # Field name made lowercase.

    class Meta:

        db_table = 'tipo_pru'


class Usuarios(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    altacurso = models.IntegerField(db_column='ALTACURSO', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    dni = models.CharField(db_column='DNI', max_length=32, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    examen = models.BigIntegerField(db_column='EXAMEN', blank=True, null=True)  # Field name made lowercase.
    fechaevaluacion = models.DateTimeField(db_column='FECHAEVALUACION', blank=True, null=True)  # Field name made lowercase.
    firmacontrato = models.IntegerField(db_column='FIRMACONTRATO', blank=True, null=True)  # Field name made lowercase.
    height = models.FloatField(db_column='HEIGHT', blank=True, null=True)  # Field name made lowercase.
    iddoctor = models.BigIntegerField(db_column='IDDOCTOR', blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    login = models.BigIntegerField(db_column='LOGIN', blank=True, null=True)  # Field name made lowercase.
    moodleid = models.IntegerField(db_column='MOODLEID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nivel = models.IntegerField(db_column='NIVEL', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=32, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=32, blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='PHONE2', max_length=32, blank=True, null=True)  # Field name made lowercase.
    rolcurso = models.IntegerField(db_column='ROLCURSO', blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=6, blank=True, null=True)  # Field name made lowercase.
    surname1 = models.CharField(db_column='SURNAME1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    surname2 = models.CharField(db_column='SURNAME2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fechaconsen = models.DateTimeField(db_column='FECHACONSEN', blank=True, null=True)  # Field name made lowercase.
    hipergluc = models.IntegerField(db_column='HIPERGLUC', blank=True, null=True)  # Field name made lowercase.
    hipogluc = models.IntegerField(db_column='HIPOGLUC', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'usuarios'

class Centro_medico(models.Model):
    name = models.CharField(max_length=250)
    #postal = models.IntegerField(max_length=250, blank = True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'centro_medico'
        

class Medico(User):
    board_number = models.CharField(max_length=250)
    medical_center = models.ForeignKey(Centro_medico, on_delete=models.PROTECT)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'medico'

class Tratamiento(models.Model):
    code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.code 

    class Meta:
        db_table = 'tratamiento'

class Paciente(User):
    TYPES = (
        ('Tipo 1', 'Diabetes de tipo 1'),
        ('Tipo 2', 'Diabetes de tipo 2'),
        ('Otro', 'Diabetes de otro tipo')
    )
    birth_date = models.DateField()
    diabetes_type = models.CharField(max_length=10, choices=TYPES)
    treatment = models.ForeignKey(Tratamiento, on_delete=models.PROTECT,null = True)
    start_date = models.DateField(null = True, blank = True)
    doctor_id = models.ForeignKey(Medico, on_delete=models.PROTECT)
    first_date = models.DateTimeField(null = True, blank= True, help_text="Primera fecha con datos del paciente")
    last_date = models.DateTimeField(null=True, blank=True, help_text="Ultima fecha con datos del paciente")

    def __str__(self):
        return self.username 

    class Meta:
        db_table = 'paciente'


class Centro_investigacion(models.Model):
    name = models.CharField(max_length=250)
    #postal = models.IntegerField(max_length=250, blank = True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'centro_investigacion'


class Investigador(User):
    TYPES_INVEST = (
        ('Research', 'Investigador de busqueda'),
        ('Analisis', 'Investigador de analisis'),
        ('Otro', 'otro tipo de investigador')
    )
    Investigator_type = models.CharField(max_length=10, choices=TYPES_INVEST)
    investigation_center = models.ForeignKey(Centro_investigacion, on_delete=models.PROTECT)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'investigador'

class Calorias(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null= False, blank= False)
    calories = models.FloatField(max_length=250)

    class Meta:
        db_table = 'calorias'
        unique_together = (('id_user', 'time'),)

class Ritmo_cardiaco(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null= False, blank= False)
    heart_rate = models.FloatField(max_length=250)

    class Meta:
        db_table = 'ritmo_cardiaco'
        unique_together = (('id_user', 'time'),)


class Pasos(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null= False, blank= False)
    steps = models.FloatField(max_length=250)

    class Meta:
        db_table = 'pasos'
        unique_together = (('id_user', 'time'),)

class Suenio(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null= False, blank= False)
    sleep_state = models.CharField(max_length=250)
    #sleep_duration = models.FloatField(max_length=250)

    class Meta:
        db_table = 'suenio'
        unique_together = (('id_user', 'time'),)

class Siesta(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null= False, blank= False)
    nap_state = models.CharField(max_length=250)
    #nap_duration = models.FloatField(max_length=250)

    class Meta:
        db_table = 'siesta'
        unique_together = (('id_user', 'time'),)

class Siesta_resumen(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null= False, blank= False)
    nap_main_sleep= models.BooleanField()
    nap_efficiency = models.FloatField(max_length=250)
    nap_duration= models.FloatField(max_length=250)
    nap_minutes_asleep = models.FloatField(max_length=250)
    nap_minutes_light = models.FloatField(max_length=250)
    nap_minutes_deep = models.FloatField(max_length=250)
    nap_minutes_rem = models.FloatField(max_length=250)
    nap_minutes_awake = models.FloatField(max_length=250)
    nap_minutes_in_bed = models.FloatField(max_length=250)
    nap_minutes_restless = models.FloatField(max_length=250)


    class Meta:
        db_table = 'siesta_resumen'
        unique_together = (('id_user', 'time'),)

class Suenio_resumen(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null= False, blank= False)
    sleep_main_sleep= models.BooleanField()
    sleep_efficiency = models.FloatField(max_length=250)
    sleep_duration= models.FloatField(max_length=250)
    sleep_minutes_asleep = models.FloatField(max_length=250)
    sleep_minutes_light = models.FloatField(max_length=250)
    sleep_minutes_deep = models.FloatField(max_length=250)
    sleep_minutes_rem = models.FloatField(max_length=250)
    sleep_minutes_awake = models.FloatField(max_length=250)
    sleep_minutes_in_bed = models.FloatField(max_length=250)

    class Meta:
        db_table = 'suenio_resumen'
        unique_together = (('id_user', 'time'),)

#MEDTRONIC

class Bg_reading(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    bg_reading_mg_dL = models.FloatField(max_length=250)

    class Meta:
        db_table = 'bg_reading'
        unique_together = (('id_user', 'time'),)


class Basal_rate(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    basal_rate_U_h = models.FloatField(max_length=250)

    class Meta:
        db_table = 'basal_rate'
        unique_together = (('id_user', 'time'),)

class Bolus_type(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    bolus_type = models.CharField(max_length=250)

    class Meta:
        db_table = 'bolus_type'
        unique_together = (('id_user', 'time'),)

class Bolus_volume_delivered(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    bolus_volume_delivered_U = models.FloatField(max_length=250)

    class Meta:
        db_table = 'bolus_volume_delivered'
        unique_together = (('id_user', 'time'),)

class Bwz_carb_ratio(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    bwz_carb_ratio_U_EX = models.FloatField(max_length=250)

    class Meta:
        db_table = 'bwz_carb_ratio'
        unique_together = (('id_user', 'time'),)

class Bwz_carb_input(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    bwz_carb_input_EX = models.FloatField(max_length=250)

    class Meta:
        db_table = 'bwz_carb_input'
        unique_together = (('id_user', 'time'),)

class Sensor_calibration(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    sensor_calibration_mg_dL = models.FloatField(max_length=250)

    class Meta:
        db_table = 'sensor_calibration'
        unique_together = (('id_user', 'time'),)

class Sensor_glucose(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    sensor_glucose_mg_dL = models.FloatField(max_length=250)

    class Meta:
        db_table = 'sensor_glucose'
        unique_together = (('id_user', 'time'),)

class Insulina_rapida(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    insulina_rapida_U = models.FloatField(max_length=250)

    class Meta:
        db_table = 'insulina_rapida'
        unique_together = (('id_user', 'time'),)

class Insulina_lenta(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    insulina_lenta_U = models.FloatField(max_length=250)

    class Meta:
        db_table = 'insulina_lenta'
        unique_together = (('id_user', 'time'),)

class Glucosa_sangre(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    glucosa_sangre_mg_dL = models.FloatField(max_length=250)

    class Meta:
        db_table = 'glucosa_sangre'
        unique_together = (('id_user', 'time'),)

class Cetonas(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    cetonas_mmol_L = models.FloatField(max_length=250)

    class Meta:
        db_table = 'cetonas'
        unique_together = (('id_user', 'time'),)

class Peso(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    peso = models.FloatField(max_length=250)

    class Meta:
        db_table = 'peso'
        unique_together = (('id_user', 'time'),)

class Hito_roche(models.Model):
    id_user = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    time = models.DateTimeField(null=False, blank=False)
    hito_roche = models.CharField(max_length=250)

    class Meta:
        db_table = 'hito_roche'
        unique_together = (('id_user', 'time'),)