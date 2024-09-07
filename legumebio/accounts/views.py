# Import necessary modules and functions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RegistrationForm, loginForm, VegetableForm, EditAccountForm
from vegetable_shop.models import Command, Vegetable
from datetime import datetime
from accounts.utils_mail import send_welcome_email, email_add_stock_command
from validate_email_address import validate_email


# User registration view
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        if validate_email(request.POST.get('email')):
            form = RegistrationForm(request.POST)
            if form.is_valid():
                try:
                    # Create user, send welcome email, and log in
                    user = form.save()
                    send_welcome_email(user) 
                    login(request, user)
                    messages.success(request, 'Compte créé avec succès!')
                    return redirect('vegetable_shop:commands')
                except Exception as e:
                    messages.warning(request, f'Erreur lors de la création du compte: {str(e)}')
            else:
                # Handle form validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        if 'username' in error:
                            messages.warning(request, 'Nom d\'utilisateur déjà pris, veuillez en choisir un autre.')
                        elif 'email' in error:
                            messages.warning(request, 'Adresse e-mail déjà utilisée, veuillez en choisir une autre.')
                        elif 'password' in error:
                            messages.warning(request, 'Erreur de mot de passe: ' + error)
                        else:
                            messages.warning(request, f'Erreur dans le champ {field}: {error}')
                return render(request, 'accounts/register.html', {'form': form})
        else:
            messages.warning(request, 'L\'adresse email n\'est pas valide.')
            return render(request, 'accounts/register.html', {'form': form})
    return render(request, 'accounts/register.html', {'form': form})


# View for users to see their commands
@login_required
def seecommands(request):
    total_commands = Command.objects.filter(user=request.user, statut='En cours').count()
    commands = Command.objects.filter(user=request.user).order_by('-date_command')
    return render(request, 'accounts/seecommands.html', {'commands': commands, 'total_commands': total_commands})

# View for staff to see all commands
@permission_required('vegetable_shop.change_command')
def seeallcommands(request):
    ongoing_commands = Command.objects.filter(statut='En cours').order_by('-date_command')
    other_commands = Command.objects.exclude(statut='En cours').order_by('-date_command')
    all_commands = list(ongoing_commands) + list(other_commands)
    total_commands = Command.objects.filter(statut= 'En cours').count()
    return render(request, 'accounts/seeallcommands.html', {'commands': all_commands, 'total_commands': total_commands})


# View to update command status
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
    

# View to edit site content
@permission_required('vegetable_shop.view_vegetable')
def edit_site(request):
    vegetables = Vegetable.objects.all()
    total_commands = Command.objects.filter(statut= 'En cours').count()
    return render(request, 'accounts/edit_site.html', {'vegetables': vegetables, 'total_commands': total_commands})


# View to delete a vegetable
@permission_required('accounts.add_user')
def delete_vegetable(request, vegetable_id):
    vegetable = Vegetable.objects.get(id=vegetable_id)
    messages.success(request, 'Légume supprimé avec succès!')
    vegetable.delete()
    return redirect('accounts:editsite')

# View to add a new vegetable
@permission_required('vegetable_shop.add_vegetable')
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
    total_commands = Command.objects.filter(statut= 'En cours').count()
    return render(request, 'accounts/add_vegetable.html', {'total_commands': total_commands})


# View to edit a vegetable (placeholder)
@permission_required('vegetable_shop.add_vegetable')
def edit_vegetable(request, vegetable_id):
    vegetable = Vegetable.objects.get(id=vegetable_id)


# View to edit a vegetable
@permission_required('vegetable_shop.change_vegetable')
def edit_vegetable(request, vegetable_id):
    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    total_commands = Command.objects.filter(statut='En cours').count()

    if request.method == 'POST':
        updated = False

        # Check and update each field if changed
        if request.POST.get('name') and request.POST.get('name') != vegetable.name:
            vegetable.name = request.POST.get('name')
            updated = True

        if request.POST.get('description') and request.POST.get('description') != vegetable.description:
            vegetable.description = request.POST.get('description')
            updated = True

        if request.FILES.get('picture') and request.FILES.get('picture') != vegetable.picture:
            vegetable.picture = request.FILES.get('picture')
            updated = True

        if request.POST.get('price') and float(request.POST.get('price')) != vegetable.price:
            try:
                vegetable.price = float(request.POST.get('price'))
                updated = True
            except ValueError:
                messages.warning(request, 'Mettez un nombre valide pour le prix.')

        if request.POST.get('stock') and int(request.POST.get('stock')) != vegetable.stock:
            current_stock = vegetable.stock
            vegetable.stock = int(request.POST.get('stock'))
            users = User.objects.all()
            if current_stock < vegetable.stock:
              for user in users:
                email_add_stock_command(user, vegetable, vegetable.stock)
            updated = True

        if updated:
            vegetable.save()
            messages.success(request, 'Légume modifié avec succès!')
        else:
            messages.info(request, 'Aucune modification détectée.')

        return redirect('accounts:editsite')

    return render(request, 'accounts/edit_vegetable.html', {'vegetable': vegetable, 'total_commands': total_commands})


# View for users to edit their account
@login_required
def edit_account(request):
    user = request.user
    total_commands = Command.objects.filter(user=request.user, statut='En cours').count()
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=user)
        if form.is_valid():
            if form.has_changed():
                form.save() 
                messages.success(request, 'Votre compte a été mis à jour avec succès.')
            else:
                messages.info(request, 'Aucune modification détectée.')

            return redirect('accounts:editaccount')
        else:
            messages.warning(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = EditAccountForm(instance=user)

    return render(request, 'accounts/edit_account.html', {'form': form, 'total_commands': total_commands})


# View to add a staff user
@permission_required('accounts.add_user')
def add_user_staff(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create user, set as staff, and add to technical team group
            user = form.save()
            user.is_staff = True
            user.save()
            technical_team = Group.objects.get(name='technical_team')
            user.groups.add(technical_team)

            messages.success(request, 'Utilisateur ajouté avec succès!')
            return redirect('accounts:editsite')
        else:
            messages.warning(request, 'Erreur lors de la validation du formulaire.')
            total_commands = Command.objects.filter(statut= 'En cours').count()
            return render(request, 'accounts/add_user_staff.html', {'form': form, 'total_commands': total_commands})
    total_commands = Command.objects.filter(statut= 'En cours').count()
    return render(request, 'accounts/add_user_staff.html', {'form': form, 'total_commands': total_commands})
    

# View to log out user    
def deconnect(request):
    logout(request)
    return redirect('vegetable_shop:index')


# View to log in user
def connect(request):
    form = loginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
           
            # Handle redirects based on 'next' parameter and user type
            next_url = request.GET.get('next')
            if next_url and next_url == '/commande/':
                if user.is_staff:
                    return redirect('accounts:seeallcommands')
                else:
                    return redirect('vegetable_shop:commands')
            if next_url and next_url == '/accounts/seecommands/':
                if user.is_staff:
                    return redirect('accounts:add_user_staff')
                else:
                    return redirect('accounts:seecommands')
            return redirect('vegetable_shop:index')
        else:
            messages.warning(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return render(request, 'accounts/login.html', {'form': form})
    return render(request, 'accounts/login.html', {'form': form})