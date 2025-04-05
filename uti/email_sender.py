# uti
# /email_sender.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 💡 Configuration SMTP de ton Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "babaissandiaye242@gmail.com"
EMAIL_PASSWORD = "ornl mmvg zykn nity"  # mot de passe d'application Gmail

def envoyer_email(destinataire, sujet, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = destinataire
    msg['Subject'] = sujet

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"📧 Email envoyé avec succès à {destinataire}")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi d'email : {e}")
