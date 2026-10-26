import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Versión en línea de GHunt: https://osint.industries
# Configuración de tu remitente (puedes usar un Gmail de pruebas con "Contraseñas de aplicación")
REMITENTE = "tu_correo_de_pruebas@gmail.com"
PASSWORD = "tu_contraseña_de_aplicacion_aqui"


def enviar_ping_verificacion(correo_destino):
  msg = MIMEMultipart("alternative")
  msg["Subject"] = "Verificación de contacto de la aplicación"
  msg["From"] = REMITENTE
  msg["To"] = correo_destino

  # Tu píxel invisible apuntando a un backend que registre la apertura
  url_pixel = f"https://tuservidor.com{correo_destino}"

  html = f"""
    <html>
      <body>
        <p>Hola, estamos validando la disponibilidad de este canal de comunicación.</p>
        <!-- Píxel de seguimiento tracking invisible -->
        <img src="{url_pixel}" width="1" height="1" style="display:none !important;" />
      </body>
    </html>
    """

  msg.attach(MIMEText(html, "html"))

  try:
    with smtplib.SMTP_SSL("://gmail.com", 465) as server:
      server.login(REMITENTE, PASSWORD)
      server.sendmail(REMITENTE, correo_destino, msg.as_string())
    print(f"📧 Correo de prueba enviado a: {correo_destino}")
  except Exception as e:
    print(f"❌ Error enviando a {correo_destino}: {e}")


# Prueba de envío
enviar_ping_verificacion("correo_a_probar@gmail.com")
