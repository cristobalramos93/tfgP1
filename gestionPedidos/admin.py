from django.contrib import admin
from gestionPedidos.models import Usuarios,TipoIns,Medico,Paciente,Centro_medico,Tratamiento


admin.site.register(Usuarios)
admin.site.register(TipoIns)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Centro_medico)
admin.site.register(Tratamiento)

# Register your models here.
