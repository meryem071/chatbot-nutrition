
#en gros pour générer un code envoyé par mail à l'user pour tester si c'est correct lol
"""
import random
import smtplib
from email.mime.text import MIMEText


def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(to_email, otp):
    sender = "ton_email@gmail.com"
    password = "ton_mot_de_passe_app"  # mot de passe d'application Gmail
    msg = MIMEText(f"Votre code OTP : {otp}")
    msg["Subject"] = "Votre code de vérification"
    msg["From"] = sender
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()
        print("Email envoyé")
    except Exception as e:
        print("Erreur lors de l'envoi de l'email :", e)"""
