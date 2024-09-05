from django.core.mail import send_mail
from django.conf import settings
from .models import Command
from django.utils.dateformat import DateFormat


def email_command(user):
    last_command = Command.objects.filter(user=user).last()
    formatted_date = DateFormat(last_command.date_command).format('d-m-Y H:i')

    subject = 'Commande passée'
    message = f"""
Bonjour {user.username},

Merci d'avoir passé commande chez Madeleine Légumes Bio !

Nous sommes ravis de vous informer que votre commande a été reçue et est en cours de préparation. Voici les détails de votre commande :

- Numéro de commande : {last_command.id}
- Date de commande : {formatted_date}
- Légume : {last_command.vegetable}
- Quantité : {last_command.quantity}
- Total : {last_command.amount} fc

Nous mettons tout en œuvre pour vous livrer des légumes frais et bio dans les meilleurs délais. Vous recevrez un email de confirmation dès que votre commande sera expédiée.

En attendant, n'hésitez pas à explorer notre site pour découvrir nos recettes et conseils pour profiter au mieux de vos légumes.

Merci de votre confiance et à très bientôt !

Cordialement,

L'équipe Madeleine Légumes Bio
"""
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)
