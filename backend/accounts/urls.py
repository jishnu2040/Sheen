from django.urls import path
from .views import RegisterUserView, VerifyUserEmail,LoginUserView,testAuthenticationView, PasswordResetRequestView,PasswordResetConfirm, SetnewPassword, LogoutUserView


urlpatterns=[
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/',VerifyUserEmail.as_view(), name='verify' ),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', testAuthenticationView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetnewPassword.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

]