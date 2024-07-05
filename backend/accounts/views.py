from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer,LoginSerializer,VerifyEmailSerializer,PasswordResetRequestSerializer,SetnewPasswordSerializer, LogoutUserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User, OneTimePassword
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .tasks import send_code_to_user_task
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .models import Partner
from .serializers import PartnerSerializer
# Create your views here.
class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        email = request.data.get('email')
    
        # Check if user with this email already exists
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            print("this is existing user log")
            if existing_user.is_verified:
                return Response({'error': "Email already registered and verified."}, status=status.HTTP_400_BAD_REQUEST)

            # Send OTP to existing user (user registered but not verified)
            send_code_to_user_task.delay(existing_user.email)
            return Response({'message': 'Verification mail resent.'}, status=status.HTTP_200_OK)
        else:
            user_data = request.data
            print("this is new user log")
            serializer = self.serializer_class(data=user_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()  # triggers the create method of your UserRegisterSerializer
                print("testregister data")
                user = serializer.data
                print("serializer userdata", user)
                # Send email function using Celery task
                send_code_to_user_task.delay(user['email'])

                return Response({ 
                    'data': user,
                    'message': 'Thanks for signing up, a passcode has been sent to your email.'
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class VerifyUserEmail(GenericAPIView):
    serializer_class = VerifyEmailSerializer 
    print("verify hited")

    def post(self, request):
        otpcode= request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user 

            if user_code_obj.expires_at < timezone.now():
                user_code_obj.delete()
                return Response({"error" :'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_verified:
                user.is_verified=True
                user.save() 
                user_code_obj.delete()  # Delete OTP after successful verification
                print(user.user_type)
                return Response({
                    'message':'Email verified successfully. You can now log in.',
                    'user_type': user.user_type,
                    'user_id': user.id
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'user already verified'
            }, status=status.HTTP_204_NO_CONTENT)

        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'passcode is invalid or not provided'
            }, status=status.HTTP_404_NOT_FOUND)


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        print(request)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # Credentials are not valid
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        # Credentials are valid, proceed with login
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class testAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data={
            'msg': "its working in authenticated user"
        }
        return Response(data,status=status.HTTP_200_OK)
    



class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # Accessing the context data
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        User = get_user_model()

        # Check if the email exists in the database
        if not User.objects.filter(email=email).exists():
            return Response({'message': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        # Send password reset email
        # Your logic to send the password reset email goes here

        return Response({'message': 'A link has been sent to your email to reset your password'}, status=status.HTTP_200_OK)


class PasswordResetConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
         try:
             user_id=smart_str(urlsafe_base64_decode(uidb64))
             user=User.objects.get(id=user_id)
             if not PasswordResetTokenGenerator().check_token(user, token):
                 return Response({'message': 'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
             return Response({'success': True, 'message':'credentials is valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
             
         except DjangoUnicodeDecodeError:
             return Response({'message':'credentials is invalid'},status=status.HTTP_401_UNAUTHORIZED)
         

class SetnewPassword(GenericAPIView):
    serializer_class=SetnewPasswordSerializer

    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'password reset successfull'}, status=status.HTTP_200_OK)

class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("logout succesfully")
        return Response(status=status.HTTP_204_NO_CONTENT)



# views.py


class PartnerDetailsView(GenericAPIView):
    serializer_class = PartnerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Assign the authenticated user to the partner profile
            serializer.save(user=self.request.user)  # Assuming user is authenticated
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
