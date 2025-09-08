from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    UpdateUserView,     # View pour mettre à jour le profil
    UserProfileView     # (optionnel) View pour récupérer les infos de l’utilisateur
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update/', UpdateUserView.as_view(), name='update-user'),        # update profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),     # optionnel
]
