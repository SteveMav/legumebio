from django.utils import timezone
from asgiref.sync import sync_to_async
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vegetable, Command, Suggestions
from .forms import CommandForm, SuggestionForm
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import Command, Vegetable
from .utils_mail import email_command, suggestion_mail

def index(request):
    # Common variables for all user types
    vegetables = Vegetable.objects.all()
    random_vegetables = Vegetable.objects.order_by('?')[:4]  # Get 4 random vegetables
    context = {'vegetables': vegetables, 'random_vegetables': random_vegetables}

    if request.user.is_staff:
        # For staff users, show total number of ongoing commands
        commands = Command.objects.filter(statut='En cours')
        context['total_commands'] = commands.count()
    elif request.user.is_authenticated:
        # For authenticated non-staff users, show their ongoing commands count
        context['user_commands_count'] = Command.objects.filter(user=request.user, statut='En cours').count()
    
    # Render the index page with the appropriate context
    return render(request, 'vegetable_shop/index.html', context)

@login_required
def commands(request, vegetable_id=None):
    if vegetable_id:
        selected_vegetable = get_object_or_404(Vegetable, vegetable_id=id)
        form = CommandForm(initial={'vegetable': selected_vegetable})

    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            # Extract form data
            vegetable = form.cleaned_data['vegetable']
            quantity = form.cleaned_data['quantity']
            
            # Create a new command instance
            command = Command(
                user=request.user,
                vegetable=vegetable,
                quantity=quantity,
                name_client=form.cleaned_data['name_client'],
                address_client=form.cleaned_data['address_client'],
                commune_client=form.cleaned_data['commune_client'],
                date_command=timezone.now(),
                statut='En cours',
                amount=vegetable.price * quantity
            )

            # Validate stock and minimum quantity requirements
            if vegetable.stock < quantity:
                messages.warning(request, 'Quantité insuffisante en stock.')
                return redirect('vegetable_shop:commands')
            if vegetable.name != 'pondu' and quantity < 5:
                messages.warning(request, 'Vous devez prendre une quantité minimum de 5 pour un légume autre que le pondu.')
                return redirect('vegetable_shop:commands')
            if vegetable.name == 'pondu' and quantity < 3:
                messages.warning(request, 'Vous devez prendre une quantité minimum de 3 pour un légume pondu.')
                return redirect('vegetable_shop:commands')
            
            # Save the command and update stock
            command.save()
            vegetable.stock -= quantity
            vegetable.save()
            
        
            email_command(request.user)  
            messages.success(request, 'Commande passée avec succès!')
            return redirect('vegetable_shop:commands')
        else:
            messages.warning(request, 'Erreur lors de la validation du formulaire.')
            return render(request, 'vegetable_shop/commands.html', {'form': form})
    else:
        # Display the command form for GET requests
        form = CommandForm()
        user_commands_count = Command.objects.filter(user=request.user, statut='En cours').count()
        return render(request, 'vegetable_shop/commands.html', {
            'form': form, 
            'vegetables': Vegetable.objects.all(), 
            'user_commands_count': user_commands_count
        })

def contact(request):
    form = SuggestionForm()
    context = {'form': form}

    if request.user.is_staff:
        # For staff users, show total number of ongoing commands
        commands = Command.objects.filter(statut='En cours')
        context['total_commands'] = commands.count()
    elif request.user.is_authenticated:
        # For authenticated non-staff users, show their ongoing commands count
        context['user_commands_count'] = Command.objects.filter(user=request.user, statut='En cours').count()

    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            # Save the suggestion
            suggestions = Suggestions(
                name_user=form.cleaned_data['name_user'],
                email_user=form.cleaned_data['email_user'],
                suggestions=form.cleaned_data['suggestions']
            )
            suggestions.save()
            messages.success(request, 'Votre message a bien été envoyé!')
            suggestion_mail(suggestions)
            return redirect('vegetable_shop:contact')
        else:
            messages.warning(request, 'Erreur lors de la validation du formulaire.')

    return render(request, 'vegetable_shop/contact.html', context)

# Custom error handlers
def custom_404(request, exception):
    return render(request, 'vegetable_shop/404.html', status=404)

def custom_500_error(request):
    return render(request, 'vegetable_shop/500.html', status=500)


