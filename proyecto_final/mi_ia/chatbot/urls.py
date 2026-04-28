from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='cuenta'), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('cuenta/', views.cuenta, name='cuenta'),
]