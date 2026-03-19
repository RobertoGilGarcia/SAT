
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:llave>', views.get_content),
]
