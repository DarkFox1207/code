import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class SecureDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers.get('Authorization', '').split(' ')[-1]
        
        # Проверка токена в Auth Service
        try:
            response = requests.get(
                'https://auth-service/api/validate_token/',
                headers={'Authorization': f'Bearer {token}'},
                verify="/path/to/cert.pem"  # Проверка сертификата
            )

            if response.status_code != 200:
                return Response({'error': 'Invalid token'}, status=403)
                
            # Обработка данных...
            return Response({'data': 'Secure data here'})
            
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=500)