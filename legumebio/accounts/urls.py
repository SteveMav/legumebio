from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.connect, name='login'),
    path('logout/', views.deconnect, name='logout'),
    path('register/', views.register, name='register'),
    path('seecommands/', views.seecommands, name='seecommands'),
    path('seeallcommands/', views.seeallcommands, name='seeallcommands'),
    path('update_status/<int:command_id>/', views.update_status, name='update_status'),
    path('editsite/', views.edit_site, name='editsite'),  
    path('deletevegetable/<int:vegetable_id>/', views.delete_vegetable, name='delete_vegetable'),
    path('addvegetable/', views.add_vegetable, name='add_vegetable'),
    path('editvegetable/<int:vegetable_id>/', views.edit_vegetable, name='edit_vegetable'),
    path('adduserstaff/', views.add_user_staff, name='add_user_staff'),
    path('editaccount', views.edit_account, name='editaccount'),

]
