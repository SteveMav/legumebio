from django.conf import settings
from django.core.mail import send_mail



def send_welcome_email(user):
    subject = 'Bienvenue sur Madeleine Légumes Bio'
    message = f"""
    Bonjour {user.username},

    Nous vous souhaitons la bienvenue sur Madeleine Légumes Bio !

    Merci de vous être inscrit sur notre plateforme. Nous sommes ravis de vous compter parmi nos membres et nous espérons que vous apprécierez notre service de commande de légumes bio en ligne.

    Si vous avez des questions ou des besoins particuliers, n'hésitez pas à nous contacter. Nous sommes là pour vous aider.

    Cordialement,

    L'équipe Madeleine Légumes Bio
    """

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)
