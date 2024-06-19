from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import RegisterView, ActivateAccountView, EmailVerificationSentView, ActivationSuccessView
from . import views


app_name = 'users'

urlpatterns = [
    path('', views.users_main, name='users_main'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('email-verification-sent/', EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('activation-success/', ActivationSuccessView.as_view(), name='activation_success'),

    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
          PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
               success_url='/users/reset-password/complete/'
               ),
          name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
          name='password_reset_complete'),
]