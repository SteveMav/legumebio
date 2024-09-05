from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Vegetable, Command, Suggestions
from .forms import CommandForm, SuggestionForm
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import Command, Vegetable
from .utils_mail import email_command

def index(request):
    if request.user.is_staff:
        commands = Command.objects.filter(statut='En cours')
        total_commands = commands.count()
        vegetables = Vegetable.objects.all()
        random_vegetables = Vegetable.objects.order_by('?')[:4]
        return render(request, 'vegetable_shop/index.html', {'total_commands': total_commands, 'vegetables': vegetables, 'random_vegetables': random_vegetables})
    
    if request.user.is_authenticated:
        user_commands_count = Command.objects.filter(user=request.user, statut='En cours').count()
        vegetables = Vegetable.objects.all()
        random_vegetables = Vegetable.objects.order_by('?')[:4]
        return render(request, 'vegetable_shop/index.html', {'user_commands_count': user_commands_count, 'vegetables': vegetables, 'random_vegetables': random_vegetables})
    
    else:
        vegetables = Vegetable.objects.all()
        random_vegetables = Vegetable.objects.order_by('?')[:4]
        return render(request, 'vegetable_shop/index.html', {'vegetables': vegetables, 'random_vegetables': random_vegetables})
    




@login_required
def commands(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            vegetable = form.cleaned_data['vegetable']
            quantity = form.cleaned_data['quantity']
            
            command = Command(
                user=request.user,
                vegetable=vegetable,
                quantity=quantity,
                name_client=form.cleaned_data['name_client'],
                address_client=form.cleaned_data['address_client'],
                commune_client=form.cleaned_data['commune_client'],
                date_command=datetime.now(),
                statut='En cours',
                amount=vegetable.price * quantity
            )

            if vegetable.stock < quantity:
                messages.warning(request, 'Quantité insuffisante en stock.')
                return redirect('vegetable_shop:commands')
            if vegetable.name != 'pondu' and quantity < 5:
                messages.warning(request, 'Vous devez prendre une quantité minimum de 5 pour un légume autre que le pondu.')
                return redirect('vegetable_shop:commands')
            if vegetable.name == 'pondu' and quantity < 3:
                messages.warning(request, 'Vous devez prendre une quantité minimum de 3 pour un légume pondu.')
                return redirect('vegetable_shop:commands')
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
        form = CommandForm()
        user_commands_count = Command.objects.filter(user=request.user, statut='En cours').count()
        return render(request, 'vegetable_shop/commands.html', {'form': form, 'vegetables': Vegetable.objects.all(), 'user_commands_count': user_commands_count})
    

def contact(request):
    form = SuggestionForm() 
    if request.user.is_staff:
        commands = Command.objects.filter(statut='En cours')
        total_commands = commands.count()
        return render(request, 'vegetable_shop/contact.html', {'form': form, 'total_commands': total_commands})
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.cleaned_data['suggestions']
            name_user = form.cleaned_data['name_user']
            email_user = form.cleaned_data['email_user']
            
            suggestions = Suggestions(
                name_user=name_user,
                email_user=email_user,
                suggestions=suggestion
            )
            suggestions.save()
            messages.success(request, 'Votre message a bien été envoyé!')
            return redirect('vegetable_shop:contact')
        else:
            messages.warning(request, 'Erreur lors de la validation du formulaire.')
    if request.user.is_authenticated:
        user_commands_count = Command.objects.filter(user=request.user, statut='En cours').count()
        return render(request, 'vegetable_shop/contact.html', {'form': form, 'user_commands_count': user_commands_count})
    else:
        return render(request, 'vegetable_shop/contact.html', {'form': form})



def custom_404(request, exception):
    return render(request, 'vegetable_shop/404.html', status=404)

def custom_500_error(request):
    return render(request, 'vegetable_shop/500.html', status=500)


