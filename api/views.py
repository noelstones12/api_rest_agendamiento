from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, timedelta
from .models import ListaTalleres, Agendamiento, Feriados, Cliente
from .serializers import ListaTalleresSerializer, AgendamientoSerializer, ClienteSerializer
import re

class ListaTalleresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ListaTalleres.objects.all()
    serializer_class = ListaTalleresSerializer

    @action(detail=True, methods=['get'])
    def disponibilidad(self, request, pk=None):
        taller = self.get_object()
        fecha_inicio = datetime.now().date() + timedelta(days=1)
        fecha_fin = fecha_inicio + timedelta(weeks=4)

        dias_disponibles = []
        current_date = fecha_inicio
        while current_date <= fecha_fin:
            if current_date.weekday() < 5 and not Feriados.objects.filter(fecha=current_date).exists():
                horas_disponibles = [
                    hora for hora in ['10:00', '14:00']
                    if not Agendamiento.objects.filter(
                        taller=taller,
                        fecha=current_date,
                        hora=hora,
                        agendado=True,
                        cancelado=False
                    ).exists()
                ]
                if horas_disponibles:
                    dias_disponibles.append({
                        'fecha': current_date,
                        'horas_disponibles': horas_disponibles
                    })
            current_date += timedelta(days=1)

        return Response(dias_disponibles)

class AgendamientoViewSet(viewsets.ModelViewSet):
    queryset = Agendamiento.objects.all()
    serializer_class = AgendamientoSerializer

    def create(self, request):
        cliente_data = request.data.pop('cliente', None)
        if not cliente_data:
            return Response({'error': 'Datos de cliente requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar RUT
        if not self.validar_rut(cliente_data.get('rut'), cliente_data.get('dv')):
            return Response({'error': 'RUT inválido'}, status=status.HTTP_400_BAD_REQUEST)

        cliente_serializer = ClienteSerializer(data=cliente_data)
        if cliente_serializer.is_valid():
            cliente = cliente_serializer.save()
        else:
            return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        agendamiento_data = request.data
        agendamiento_data['cliente'] = cliente.id

        # Validar disponibilidad
        if not self.validar_disponibilidad(agendamiento_data):
            return Response({'error': 'Horario no disponible'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=agendamiento_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def eliminar_por_rut(self, request):
        rut = request.data.get('rut')
        dv = request.data.get('dv')

        if not self.validar_rut(rut, dv):
            return Response({'error': 'RUT inválido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente = Cliente.objects.get(rut=rut, dv=dv)
            agendamiento = Agendamiento.objects.filter(
                cliente=cliente, 
                agendado=True, 
                cancelado=False
            ).first()

            if agendamiento:
                agendamiento.cancelado = True
                agendamiento.save()
                return Response({'message': 'Agendamiento cancelado exitosamente'})
            else:
                return Response({'error': 'No se encontró un agendamiento activo para este cliente'}, 
                                status=status.HTTP_404_NOT_FOUND)

        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def validar_rut(rut, dv):
        try:
            rut = int(rut)
            dv = dv.upper()
            s = 1
            t = 0
            for i in range(len(str(rut))):
                s = (s + rut % 10 * (9 - i % 6)) % 11
                rut = rut // 10
            v = (11 - s) % 11
            if v == 10:
                return dv == 'K'
            else:
                return str(v) == dv
        except:
            return False

    @staticmethod
    def validar_disponibilidad(data):
        fecha = data.get('fecha')
        hora = data.get('hora')
        taller_id = data.get('taller')

        # Verificar si es día hábil
        if datetime.strptime(fecha, '%Y-%m-%d').weekday() >= 5:
            return False

        # Verificar si es feriado
        if Feriados.objects.filter(fecha=fecha).exists():
            return False

        # Verificar si el horario está disponible
        if Agendamiento.objects.filter(
            taller_id=taller_id,
            fecha=fecha,
            hora=hora,
            agendado=True,
            cancelado=False
        ).exists():
            return False

        return True