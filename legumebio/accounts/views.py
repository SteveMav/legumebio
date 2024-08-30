from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from requests import session
from .forms import RegistrationForm, loginForm, VegetableForm
from vegetable_shop.models import Command, Vegetable
from datetime import datetime

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès!')
            return redirect('vegetable_shop:commands')
        else:
            messages.warning(request, 'Erreur lors de la validation du formulaire.')
            return render(request, 'accounts/register.html', {'form': form})
    return render(request, 'accounts/register.html', {'form': form})



@login_required
def seecommands(request):
    total_commands = Command.objects.filter(user=request.user, statut='En cours').count()
    commands = Command.objects.filter(user=request.user).order_by('-date_command')
    return render(request, 'accounts/seecommands.html', {'commands': commands, 'total_commands': total_commands})

@permission_required('vegetable_shop.change_command')
def seeallcommands(request):
    commands = Command.objects.filter(statut='En cours')
    total_commands = commands.count()
    all_commands = Command.objects.all().order_by('-date_command')
    return render(request, 'accounts/seeallcommands.html', {'commands': all_commands, 'total_commands': total_commands})

@permission_required('vegetable_shop.change_command')
def update_status(request, command_id):
    if request.method == 'GET':
        try:
            command = Command.objects.get(id=command_id)
            command.statut = 'effectué'
            command.save()
            return redirect('accounts:seeallcommands')
        except Command.DoesNotExist:
            return render(request,{'success': False, 'error': 'Commande non trouvée'})
    else:
        return redirect('accounts:seeallcommands')
    

@permission_required('accounts.add_user')  
def edit_site(request):
    vegetables = Vegetable.objects.all()
    return render(request, 'accounts/edit_site.html', {'vegetables': vegetables})


@permission_required('accounts.add_user')
def delete_vegetable(request, vegetable_id):
    vegetable = Vegetable.objects.get(id=vegetable_id)
    messages.success(request, 'Légume supprimé avec succès!')
    vegetable.delete()
    return redirect('accounts:editsite')

permission_required('vegetable_shop.add_vegetable')
def add_vegetable(request):
    if request.method == 'POST':
        vegetable_name = request.POST.get('name')
        vegetable_description = 'legume bio'
        vegetable_image = request.FILES.get('picture')
        vegetable_price = request.POST.get('price')
        vegetable_stock = request.POST.get('stock')
        date_add = datetime.now()
        vegetable = Vegetable(name=vegetable_name, description=vegetable_description, picture=vegetable_image, price=vegetable_price, stock=vegetable_stock, date_add=date_add)
        vegetable.save()
        messages.success(request, 'Légume ajouté avec succès!')
        return redirect('accounts:editsite')
    return render(request, 'accounts/add_vegetable.html')

def edit_vegetable(request, vegetable_id):
    vegetable = Vegetable.objects.get(id=vegetable_id)


    if request.method == 'POST':
        if request.POST.get('name') == '':
            vegetable_name = vegetable.name
        else:
            vegetable_name = request.POST.get('name')
        vegetable_description = vegetable.description


        if request.FILES.get('picture') == None:
            vegetable_image = vegetable.picture
        else:
            vegetable_image = request.FILES.get('picture')



        if request.POST.get('price') == '':
            vegetable_price = vegetable.price
        else:
            vegetable_price = float(request.POST.get('price'))



        if request.POST.get('stock') == '':
            vegetable_stock = vegetable.stock
        else:
            vegetable_stock = request.POST.get('stock')
        
        date_edit = vegetable.date_add


        vegetable.name = vegetable_name
        vegetable.description = vegetable_description
        vegetable.picture = vegetable_image
        vegetable.price = vegetable_price
        vegetable.stock = vegetable_stock
        vegetable.date_edit = date_edit
        vegetable.save()
        messages.success(request, 'Légume modifié avec succès!')
        return redirect('accounts:editsite')
    return render(request, 'accounts/edit_vegetable.html', {'vegetable': vegetable})


@permission_required('accounts.add_user')
def add_user_staff(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
        
            user = form.save()
            user.is_staff = True
            user.save()
            

            messages.success(request, 'Utilisateur ajouté avec succès!')
            return redirect('accounts:editsite')
        else:
            messages.warning(request, 'Erreur lors de la validation du formulaire.')
            return render(request, 'accounts/add_user_staff.html', {'form': form})
    return render(request, 'accounts/add_user_staff.html', {'form': form})
    

    
def deconnect(request):
    logout(request)
    return redirect('vegetable_shop:index')



def connect(request):
    form = loginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('vegetable_shop:commands')
        else:
            messages.warning(request, 'Utilisateur ou mot de passe incorrect.')
            return render(request, 'accounts/login.html', {'form': form})
    return render(request, 'accounts/login.html', {'form': form})