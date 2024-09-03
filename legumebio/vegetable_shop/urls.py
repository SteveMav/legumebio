from django.urls import path
from .import views

app_name = 'vegetable_shop'


urlpatterns = [
    path('', views.index, name='index'),
    path('commande/', views.commands, name='commands'),
    path('contact/', views.contact, name='contact'),
]