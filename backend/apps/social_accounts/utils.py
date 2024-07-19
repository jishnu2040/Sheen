from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta, datetime, timezone
from django.conf import settings  # Import Django settings

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

from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

User = get_user_model()

def register_social_user(provider, email, first_name, last_name):
    filtered_user_by_email = User.objects.filter(email=email)
    
    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            return {
                'email': filtered_user_by_email[0].email,
                'username': filtered_user_by_email[0].username,
                'tokens': filtered_user_by_email[0].tokens()
            }
        else:
            raise AuthenticationFailed(
                detail=f'Please continue your login using {filtered_user_by_email[0].auth_provider}'
            )
    else:
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=settings.SOCIAL_SECRET,
            auth_provider=provider
        )
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
