from rest_framework import serializers
from .models import Comuna, ListaTalleres, Cliente, Agendamiento, Feriados

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class ListaTalleresSerializer(serializers.ModelSerializer):
    comuna = ComunaSerializer(read_only=True)

    class Meta:
        model = ListaTalleres
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class AgendamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamiento
        fields = '__all__'

class FeriadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriados
        fields = '__all__'