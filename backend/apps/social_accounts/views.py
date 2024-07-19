from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings  # Import Django settings
from datetime import timedelta, datetime, timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed
from .serializers import GoogleSignInSerializer

class Google:
    @staticmethod
    def validate(access_token):
        try:
            print("Validating Google token...")
            id_info = id_token.verify_oauth2_token(access_token, requests.Request())
            
            if "accounts.google.com" not in id_info['iss']:
                raise AuthenticationFailed(detail="Invalid token issuer.")
            
            current_time = datetime.now(timezone.utc)
            issued_time = datetime.fromtimestamp(id_info['iat'], timezone.utc)
            allowed_skew = timedelta(seconds=60)  # Increased skew to 60 seconds
            
            if issued_time > (current_time + allowed_skew):
                raise AuthenticationFailed(detail="Token used too early. Check that your computer's clock is set correctly.")
            
            return id_info
        except Exception as e:
            print("Token validation failed:", e)
            raise AuthenticationFailed(detail="Invalid or expired token.")

class GoogleSignInView(GenericAPIView):
    serializer_class = GoogleSignInSerializer

    def post(self, request):
        print("GoogleSignInView POST request data:", request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']
        
        try:
            # Validate Google token using Google class method
            id_info = Google.validate(access_token)
            
            # Process further with validated id_info if needed
            
            return Response(id_info, status=status.HTTP_200_OK)
        
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
