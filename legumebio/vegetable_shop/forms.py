from django import forms
from .models import Command, Vegetable, Suggestions

class CommandForm(forms.ModelForm):
    COMMUNE_CHOICES = [
        ('gombe', 'Gombe'),
        ('lingwala', 'Lingwala'),
        ('kinshasa', 'kinshasa'),
    ]

    commune_client = forms.ChoiceField(
        choices=COMMUNE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control my-3', 'id': 'communeSelect'}),
        label='Commune'
    )

    class Meta:
        model = Command
        fields = ['vegetable', 'quantity', 'name_client', 'address_client', 'commune_client', 'date_command', 'statut', 'amount']
        labels = {
            'vegetable': 'Légume',
            'quantity': 'Quantité',
            'name_client': 'Nom et prénom',
            'address_client': 'Adresse de livraison',
            'commune_client': 'Commune',
            'date_command': 'Date Commande',
            'statut': 'Statut',
            'amount': 'Montant',
        }
        widgets = {
            'vegetable': forms.Select(attrs={'class': 'form-control my-3', 'id': 'vegetableSelect', 'onchange': 'updateRangeMax()'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control my-3', 'id': 'rangeInput', 'min': '3', 'max': '0', 'value': '0', 'oninput': 'amount.value=rangeInput.value'}),
            'name_client': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'address_client': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'date_command': forms.HiddenInput(),
            'statut': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
        }

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestions
        fields = ['name_user', 'email_user', 'suggestions']
        widgets = {
            'name_user': forms.TextInput(attrs={'class': 'form-control border-0 py-3 mb-4', 'placeholder': 'votre nom'}),
            'email_user': forms.EmailInput(attrs={'class': 'form-control border-0 py-3 mb-4', 'placeholder': 'email'}),
            'suggestions': forms.Textarea(attrs={'class': 'form-control border-0 mb-4', 'rows': '5', 'cols': '10', 'placeholder': 'votre message'}),
        }

