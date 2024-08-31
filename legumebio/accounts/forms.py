from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from vegetable_shop.models import Vegetable

class RegistrationForm(UserCreationForm):
    COMMUNE_CHOICES = [
        ('gombe','gombe'),
        ('lingwala', 'ligwala'),
        ('kinshasa', 'kinshasa')
    ]
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        label='Numéro de téléphone', 
        widget=forms.NumberInput(attrs={'class': 'form-control my-3', 'id': 'phoneNumberInput'}), 
        help_text=''
    )
    commune = forms.ChoiceField(
        choices=COMMUNE_CHOICES,
        required=False, 
        label='Commune', 
        widget=forms.Select(attrs={'class': 'form-control my-3', 'id': 'communeInput'}), 
        help_text=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'commune', 'password1', 'password2']
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Email',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-3', 'id': 'usernameInput'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-3', 'id': 'emailInput'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control my-3', 'id': 'passwordInput'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control my-3', 'id': 'confirmPasswordInput'}),
        }
        help_texts = {
            'username': '',
            'email': '',
            'phone_number': '',
            'commune': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control my-3', 'id': 'passwordInput'})
        self.fields['password1'].help_text = 'Le mot de passe doit contenir au moins 8 caractères, dont une lettre majuscule, une lettre minuscule, un chiffre et un caractère spécial.'
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmation du mot de passe'
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs.update({'class': 'form-control my-3', 'id': 'confirmPasswordInput'})

        

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, phone_number=self.cleaned_data['phone_number'], commune=self.cleaned_data['commune'])
            profile.save()
        return user
    
class loginForm(forms.Form):
    username = forms.CharField(
        max_length=15, 
        required=True, 
        label='Nom d\'utilisateur', 
        widget=forms.TextInput(attrs={'class': 'form-control my-3', 'id': 'usernameInput'}), 
        help_text=''
    )
    password = forms.CharField(
        max_length=15, 
        required=True, 
        label='Mot de passe', 
        widget=forms.PasswordInput(attrs={'class': 'form-control my-3', 'id': 'passwordInput'}), 
        help_text=''
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control my-3', 'id': 'passwordInput'})
        self.fields['password'].help_text = ''
        self.fields['password'].label = 'Mot de passe'



class VegetableForm(forms.Form):
    class Meta:
        model = Vegetable
        fields = ['name', 'picture', 'price', 'stock']
        labels = {
            'name': 'Nom du légume',
            'picture': 'Photo du légume',
            'price': 'Prix du légume',
            'stock': 'Stock du légume',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control my-3', 'id': 'nameInput'}),
            'picture': forms.FileInput(attrs={'class': 'form-control my-3', 'id': 'pictureInput'}),
            'price': forms.NumberInput(attrs={'class': 'form-control my-3', 'id': 'priceInput'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control my-3', 'id': 'stockInput'}),
        }




class EditAccountForm(forms.ModelForm):
    COMMUNE_CHOICES = [
        ('gombe', 'gombe'),
        ('lingwala', 'lingwala'),
        ('kinshasa', 'kinshasa')
    ]
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control my-3', 'placeholder': ''})
    )
    commune = forms.ChoiceField(
        choices=COMMUNE_CHOICES,
        required=False, 
        widget=forms.Select(attrs={'class': 'form-control my-3', 'placeholder': 'Commune'})
    )
        
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Email',
            'phone_number': 'Numéro de téléphone',
            'commune': 'Commune',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-3', 'placeholder': 'Nom d\'utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-3', 'placeholder': 'Email'}),
        }
        help_texts = {
            'username': None,
            'email': None,
        }

    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['phone_number'].initial = self.instance.profile.phone_number
            self.fields['commune'].initial = self.instance.profile.commune

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile.phone_number = self.cleaned_data['phone_number']
        user.profile.commune = self.cleaned_data['commune']
        if commit:
            user.save()
            user.profile.save()
        return user
