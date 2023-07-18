from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
app_name = 'login_app'

urlpatterns = [
    path('login/nuevo-usuario/', views.nuevo_usuario, name='nuevo-usuario'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('locked/', views.locked, name='locked'),
    # API JWT Tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]