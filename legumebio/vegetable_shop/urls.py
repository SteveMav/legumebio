from django.urls import path
from django.conf.urls import handler404
from .import views

app_name = 'vegetable_shop'

handler404 = 'vegetable_shop.views.custom_404'

urlpatterns = [
    path('', views.index, name='index'),
    path('commande/', views.commands, name='commands'),
    path('contact/', views.contact, name='contact'),
]