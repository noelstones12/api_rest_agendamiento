from django.contrib import admin
from .models import Comuna, ListaTalleres, Cliente, Agendamiento, Feriados



# Register your models here.

admin.site.register(Comuna)
admin.site.register(ListaTalleres)
admin.site.register(Cliente)
admin.site.register(Agendamiento)
admin.site.register(Feriados)

