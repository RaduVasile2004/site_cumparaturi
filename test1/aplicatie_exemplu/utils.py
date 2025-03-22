from django.core.mail import send_mail
from django.conf import settings

def trimite_email_confirmare(user):
    subject = "Confirmare e-mail"
    mesaj = f"""
    Bun venit, {user.first_name} {user.last_name}!
    Username-ul tău: {user.username}

    Te rugăm să confirmi e-mailul accesând acest link:
    http://127.0.0.1:8000/confirma_mail/{user.cod}/
    """
    send_mail(
        subject,
        mesaj,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
