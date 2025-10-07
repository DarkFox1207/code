from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
import requests

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        
        # Проверка существования пользователя в User Service
        try:
            response = requests.get(f'http://localhost:8000/api/users/{user_id}/')
            if response.status_code != 200:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except requests.exceptions.RequestException:
            return Response(
                {'error': 'User service unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return super().create(request, *args, **kwargs)