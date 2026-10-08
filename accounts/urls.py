from django.urls import path

from .views import (
    CSRFView, ChangePasswordView, LoginView, LogoutView, ProfileView, RegisterView,
)


app_name = 'accounts'

urlpatterns = [
    path('csrf/', CSRFView.as_view(), name='csrf'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
