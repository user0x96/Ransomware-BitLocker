# Copyright 2025 © @user0x96
# Github: https://github.com/user0x96
# Donate⭐ 
# +USDT(TRC-20): TCLCdvvvgy6Pbj5VnTzaYBwGKzBDyBEyGL
# +BTC: 3EALRZzA5vp7i6kXhELTujphiJC4WwZESF
import os
import glob
import socket
import time
import getpass
import subprocess
import threading
import requests

# ANSI color codes for console output
YELLOW = '\033[93m'
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

# Create a long title string for scrolling effect
base_title = 'Decryption BitLocker* ' * 10

#====================== Function to animate the console title ======================
def animated_title():
    while True:
        for i in range(len(base_title)):
            title = base_title[i:] + base_title[:i]
            os.system(f'title {title}')
            time.sleep(0.1)

#====================== Function to list available drives ======================
def list_drives():
    drives = []
    try:
        bitmask = subprocess.check_output("fsutil fsinfo drives", shell=True).decode().strip().split()
        for drive in bitmask[1:]:
            drives.append(drive)
    except subprocess.CalledProcessError:
        pass
    return drives

#====================== Function to unlock user folders ======================
def unlock_folders():
    user_profile = os.getenv('USERPROFILE')
    folders_to_unlock = ['Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos']
    for folder_name in folders_to_unlock:
        folder_path = os.path.join(user_profile, folder_name)
        if os.path.isdir(folder_path):
            try:
                subprocess.run(['icacls', folder_path, '/remove:d', 'everyone'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                pass

#====================== Function to fetch content from a URL ======================
def get_http_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return ""

#====================== Function to shutdown the computer ======================
def shutdown_computer():
    try:
        subprocess.run(['shutdown', '/s', '/f', '/t', '0'], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.CalledProcessError:
        pass

#====================== Function to display system information ======================
def display_system_info():
    computer_name = socket.gethostname()
    user_name = getpass.getuser()
    print(f'{YELLOW}#DeviceName: {computer_name}{RESET}')
    print(f'{YELLOW}#UserName: {user_name}{RESET}')
    drives = list_drives()
    print(f'{YELLOW}#Available Drives: {" ".join(drives)}{RESET}')
    print()

#====================== Function to get user input ======================
def get_user_input():
    drive_letter = input(f'{YELLOW}>>Enter Drive To Decrypt (D, E, F...): {RESET}').upper()
    recovery_key = input(f'{YELLOW}>>Enter Recovery Key: {RESET}')
    
    if drive_letter not in "DEFGHIJKLMNOPQRSTUVWXYZ":
        print(f'{RED}Invalid Drive Letter!{RESET}')
        time.sleep(2)
        os._exit(0)
    
    if len(recovery_key) < 48:
        print(f'{RED}Invalid Key! Minimum 48 Characters Required!{RESET}')
        time.sleep(2)
        os._exit(0)
    
    return drive_letter, recovery_key

#====================== Function to run a command ======================
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    return process.returncode, output, error

#====================== Function to decrypt a drive ======================
def decrypt_drive(drive_letter, recovery_key):
    unlock_command = f'manage-bde -unlock {drive_letter}: -RecoveryPassword {recovery_key}'
    return_code, output, error = run_command(unlock_command)
    
    if return_code != 0:
        print(f'{RED}Failed to Unlock Drive! Please Check the Key!{RESET}')
        print(f'{RED}Error: {error}{RESET}')
        time.sleep(2)
        os._exit(0)
    
    off_command = f'manage-bde -off {drive_letter}:'
    run_command(off_command)

#====================== Function to update system settings ======================
def update_system_settings():
    os.system('cls')
    subprocess.run('reg add HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer /v NoDrives /t REG_DWORD /d 0 /f', shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.run('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 0 /f', shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.run('taskkill /F /IM explorer.exe & start explorer', shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

#====================== Function to delete .txt files from Startup folder ======================
def delete_txt_from_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    txt_files = glob.glob(os.path.join(startup_path, '*.txt'))
    
    for file in txt_files:
        try:
            os.remove(file)
        except Exception:
            pass

#====================== Main function to orchestrate decryption process ======================
def pain():
    # Start animated title in a separate thread
    thread = threading.Thread(target=animated_title)
    thread.daemon = True
    thread.start()

    # Display system information
    display_system_info()

    try:
        # Get user input
        drive_letter, recovery_key = get_user_input()

        # Decrypt the drive
        decrypt_drive(drive_letter, recovery_key)

        # Update system settings
        update_system_settings()

        # Unlock user folders
        unlock_folders()
        
        # Delete .txt files from Startup
        delete_txt_from_startup()
        
        # Notify success
        print(f'{GREEN}Decryption Completed Successfully!{RESET}')
        time.sleep(1)
        os._exit(0)
    except Exception:
        os._exit(0)

if __name__ == "__main__":
    pain()