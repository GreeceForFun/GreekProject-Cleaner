from pathlib import Path
import psutil
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label, Frame
import ctypes
import os
import socket
from colored import fg, attr
import errno
from PIL import Image, ImageDraw, ImageSequence
import shutil
import matplotlib.font_manager as fm
import winsound
import threading
import subprocess
import requests
import platform
from datetime import datetime
import psutil
import wmi
import cpuinfo
from pathlib import Path
import winreg
import time
import uuid
from time import sleep
from termcolor import colored
import matplotlib.pyplot as plt
from zipfile import ZipFile
from io import BytesIO
from packaging import version
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path("~").expanduser() / Path("AppData/Local/GreekProject/DoTLook-main/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#Font Installer & Checker
font_path = Path("~").expanduser() / Path("AppData/Local/GreekProject/DoTLook-main/assets/frame0/Moul-Regular.ttf")
check_path = f"C:\Windows\Fonts\Moul-Regular.ttf"

def font_exists(check_path):
    if os.path.exists(check_path):
        return True
    else:
        print(f'{fg(1)}Found Missing Font! Please Wait...')
        sleep(2)
        install_font_system_wide(font_path)

def install_font_system_wide(font_path):
    destination_path = 'C:/Windows/Fonts/'

    if os.path.exists(check_path):
        pass
    else:
        try:
            shutil.copy(font_path, destination_path)
            font_filename = os.path.basename(font_path)

            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, font_filename, 0, winreg.REG_SZ, font_filename)
            winreg.CloseKey(key)

            print(f"{fg(2)}Downloading Required Font...")
            sleep(2)
            print(f"{fg(2)}Downloaded Required Font!")
            sleep(1)
        except Exception as e:
            print(f'{fg(1)}Error Installing Required Font(s), Make Sure To Open As Admin & Try Again!')
            send_error_to_discord(str(e))
            sleep(10)
            sys.exit()

#Internet Check
def check_internet_connection():
    try:
        socket.create_connection(("1.1.1.1", 80))
    except OSError:
        print(f"{fg(1)}No Internet Connection / Bad Internet Connection!")
        sleep(5)
        sys.exit()

#Sound For Cleaned + Error
def play_sound(file_path):
    try:
        winsound.PlaySound(str(file_path), winsound.SND_FILENAME)
    except Exception as e:
        print(f"{fg(1)}Error Playing Done Sound: {e}, Contact Us!")
        send_error_to_discord(str(e))

sound_file_path = Path("~").expanduser() / Path("AppData/Local/GreekProject/DoTLook-main/assets/frame0/done_cleaning.wav")

def play_error_sound():
    frequency = 300  # Hz
    duration = 180  # Milliseconds
    winsound.Beep(frequency, duration)

#File Check + Downloading Required Files
def create_folder():
    try:
        appdata_local_path = os.path.join(os.getenv('LOCALAPPDATA'), 'GreekProject')
        github_url = 'https://github.com/GreeceForFun/DoTLook/archive/main.zip'

        create_folder_if_not_exists(appdata_local_path)

        if not os.listdir(appdata_local_path):
            print(f"{fg(2)}Downloading Required Files... (One-Time Only)")
            sleep(5)
            download_and_extract_zip(github_url, appdata_local_path)
            sleep(8)
            install_font_system_wide(font_path)
            sleep(1)
            print(f"{fg(2)}Done! Thank You For Using Our Cleaner")
            sleep(2)
        else:
            pass
    except Exception as e:
        print(f"{fg(1)}Error Downloading Required Files! (Bad Internet Connection OR No Permission)")
        send_error_to_discord(str(e))
        sleep(10)
        sys.exit()

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def download_and_extract_zip(url, destination_folder):
    response = requests.get(url)
    zip_file = ZipFile(BytesIO(response.content))

    zip_file.extractall(destination_folder)
    zip_file.close()

#Want To Know That Someone Uses This Script :)
def send_notification():

    webhook_url = 'https://discord.com/api/webhooks/1184790370652016771/0gV08mEfBWSQsc8fvkiALVDX2rQfjaZA9Ko3zp-zNDYohoJhLJo_lsjd_lgUW4yvCrh5'
    message = "A User Just Opened The Cleaner V2!"

    data = {"content": message}
    requests.post(webhook_url, json=data)

#Current Version
current_version = "2.0"

#Under Maintenance Check
check_github_link = "https://raw.githubusercontent.com/GreeceForFun/DoTLook/main/test.txt"

def check_github_txt(link):
    try:
        response = requests.get(link)
        response.raise_for_status()

        if "no" in response.text.lower():
            print(f"{fg(1)}Program Is Currently Under Maintenance! Try Again Later!")
            sleep(10)
            sys.exit()
        else:
            pass
    except requests.exceptions.RequestException as e:
        print(f"{fg(1)}Can't Check Maintenance Status! Contact Us!")
        send_error_to_discord(str(e))

#Disclaimer
py_file_path = Path("~").expanduser() / Path("AppData/Local/GreekProject/DoTLook-main/assets/frame0/disclaimer.pyw")

def create_check_file(py_file_path):
    directory = os.path.dirname(py_file_path)

    check_file_path = os.path.join(directory, "check.txt")
    if os.path.exists(check_file_path):
        return True
    else:
        with open(check_file_path, 'w') as check_file:
            sleep(0.1)

        disclaimer_script_path = os.path.join(directory, "disclaimer.pyw")
        if os.path.exists(disclaimer_script_path):
            try:
                subprocess.run(['python', disclaimer_script_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"{fg(1)}Failed To Show Disclaimer! Contact Us!")
                send_error_to_discord(str(e))
        else:
            print(f"{fg(1)}Failed To Show Disclaimer! Contact Us!")

#Check(s) To Avoid Crashes
def is_eset_installed():
    program_name = "ecmds.exe"
    for root, dirs, files in os.walk("C:\\Program Files\\ESET\\ESET Security"):
        if program_name in files:
            return True
    return False

def is_ea_installed():
    ea = "EALauncher.exe"
    for root, dirs, files in os.walk("C:\\Program Files\\Electronic Arts\\EA Desktop\\EA Desktop"):
        if ea in files:
            return True
    return False

def is_win10():
    return sys.getwindowsversion().build <= 22000

def check_ram():
    total_ram_bytes = psutil.virtual_memory().total
    total_ram_gb = total_ram_bytes / (1024 ** 3)

    return 2 <= total_ram_gb <= 8

def AVG_Check():
    folder_path = "C:\\ProgramData\\AVG"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return True
    return False

def check_discord():
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == 'Discord.exe':
                subprocess.Popen(["taskkill", "/f", "/im", "discord.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                shutil.rmtree(os.path.expanduser("~") + "\\AppData\\Roaming\\discord\\Cache\\Cache_Data", ignore_errors=True)
                shutil.rmtree(os.path.expanduser("~") + "\\AppData\\Roaming\\discord\\Cache\\GPUCache", ignore_errors=True)
                sleep(1)
                find_and_open_discord()
                return
        shutil.rmtree(os.path.expanduser("~") + "\\AppData\\Roaming\\discord\\Cache\\Cache_Data", ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~") + "\\AppData\\Roaming\\discord\\Cache\\GPUCache", ignore_errors=True)
    except Exception as e:
        sleep(1)
        send_error_to_discord(str(e))

def check_battlenet():
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == 'Battle.net.exe':
                subprocess.Popen(["taskkill", "/f", "/im", "battle.net.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\Battle.net\\Logs")) for file in files if file.endswith(".log")]
                shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Battle.net\\BrowserCaches\\common\\Cache"), ignore_errors=True)
                shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Battle.net\\BrowserCaches\\common\\Code Cache"), ignore_errors=True)
                shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Battle.net\\Cache"), ignore_errors=True)
                sleep(1)
                return
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Battle.net\\BrowserCaches\\common\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Battle.net\\BrowserCaches\\common\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Battle.net\\Cache"), ignore_errors=True)
    except Exception as e:
        sleep(1)
        send_error_to_discord(str(e))


def already_open():
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == 'GreekProject.exe':
                print(f"{fg(1)}This App Is Already Open! Make Sure To Check Task Manager!")
                sleep(10)
                sys.exit()
        else:
            pass
    except Exception as e:
        sleep(2)
        send_error_to_discord(str(e))

#Log(s)
def send_error_to_discord(error_message):
    DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1202017850987118633/QWcXqnnKeZiMsafU0K1ofletc5iDqk6T49YW58dhMsofk9sH8TwuW6ZhVcrp82IAJimx'

    payload = {'content': f'Error! \nError: {error_message}'}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def checks_to_discord(check_message):
    DISCORD_WEBHOOK_URL_CHECK = 'https://discord.com/api/webhooks/1215384356726771812/fP_J5wCzgsTtemEgsmXXNgvILF02rwBt_QFSLH7Rr8EyUP0HNfFzH7hqXqgbU2Cjw-n_'

    payload = {'content': f'Check! \nCheck: {check_message}'}
    requests.post(DISCORD_WEBHOOK_URL_CHECK, json=payload)

# User Information Grabbing (OS / CPU / GPU / RAM)
def get_windows_info():
    system_info = platform.uname()

    os_version = system_info.version

    architecture = system_info.machine

    if architecture == "AMD64":
        architecture = "64-bit"

    if os_version >= '10.0.22000':
        os_text = f"Windows-11 {architecture}"
    else:
        os_text = f"Windows-{os_version} {architecture}"

    return os_text


def get_cpu_info():
    try:
        c = wmi.WMI()
        for processor in c.Win32_Processor():
            cpu_name = processor.Name
            cpu_name = cpu_name.replace("AMD ", "").replace("Processor", "").replace("CPU", "").strip()
            return cpu_name
    except Exception as e:
        print("Error:", e)
        return "Error retrieving CPU info"

def get_ram_info():
    try:
        ram_info = psutil.virtual_memory()
        ram_gb = round(ram_info.total / (1024 ** 3))
        if ram_gb <= 8:
            return 8
        elif ram_gb <= 16:
            return 16
        elif ram_gb <= 24:
            return 24
        elif ram_gb <= 32:
            return 32
        elif ram_gb <= 48:
            return 48
        else:
            return 64
    except Exception as e:
        print("Error:", e)
        return "Error retrieving RAM info"

def get_gpu_info():
    try:
        c = wmi.WMI()
        for gpu in c.Win32_VideoController():
            return gpu.Name
    except Exception as e:
        print("Error:", e)
        return "Error retrieving GPU info"

#Defs For Cleaning + Performance
def set_power_plan():
    power = 'powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'

    try:
        subprocess.run(power, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{fg(1)}Can't set Power Plan To 'High Performance'. Contact Us!")
        send_error_to_discord(str(e))

def delete_local_files_tmp():
    folder_path = os.path.expanduser("~\\AppData\\Local")

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".tmp"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    if e.winerror == 32:
                        return
                    else:
                        return

def delete_roaming_files_tmp():
    folder_path = os.path.expanduser("~\\AppData\\Roaming")

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".tmp"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    if e.winerror == 32:
                        pass
                    else:
                        pass

def delete_windows_files_tmp():
    folder_path = os.path.expanduser("C:\\Windows\\System32\\config\\systemprofile\\AppData\\Local")

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".tmp"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    if e.winerror == 32:
                        return
                    else:
                        return

def delete_txt_files(folder_path):
    try:
        if os.path.exists(folder_path):
            files_and_folders = os.listdir(folder_path)

            target_files = [f for f in files_and_folders if f.endswith(".txt")]

            for target_file in target_files:
                target_file_path = os.path.join(folder_path, target_file)

                if os.path.exists(target_file_path):
                    os.remove(target_file_path)
                else:
                    pass
        else:
            pass
    except Exception as e:
        send_error_to_discord(str(e))

home_directory = os.path.expanduser("~")
filmora_folder_path = os.path.join(home_directory, "AppData", "Local", "Wondershare", "Wondershare Filmora")

def delete_files_with_prefix(directory, prefix):
    try:
        for filename in os.listdir(directory):
            if filename.startswith(prefix):
                file_path = os.path.join(directory, filename)
                try:
                    os.remove(file_path)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        pass
                    elif e.errno == errno.EACCES:
                        pass
                    else:
                        raise
    except Exception as e:
        send_error_to_discord(str(e))

directory_path = r'C:\ProgramData\Microsoft\Windows Defender\Scans'
prefix_to_delete = 'mpcache'

def find_and_open_discord():
    discord_directory = os.path.expanduser("~")
    discord_folder_path = os.path.join(discord_directory, "AppData", "Local", "Discord")

    app_folders = [folder for folder in os.listdir(discord_folder_path) if folder.startswith('app')]

    if app_folders:
        app_folder = app_folders[0]
        discord_exe_path = os.path.join(discord_folder_path, app_folder, 'Discord.exe')

        if os.path.exists(discord_exe_path):
            with open(os.devnull, 'w') as devnull:
                subprocess.Popen([discord_exe_path], stdout=devnull, stderr=devnull)
                return
    return

def remove_old_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".old"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    if e.errno != errno.EACCES:  # Skip only if it's Access Denied
                        pass

def remove_dmp_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dmp"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except OSError as e:
                    if e.errno not in (errno.ENOENT, errno.EACCES):
                        raise

#Threading (Avoid Crashing / Freezing / Bugs)
def start_task():
    thread = threading.Thread(target=cleaning_code)
    thread.start()

#Check(s) (Update Check)
check_internet_connection()
create_folder()
font_exists(check_path)
check_github_txt(check_github_link)
create_check_file(py_file_path)
already_open()


#Cleaning Code
def cleaning_code():
    if not is_admin():
        sleep(0.5)
        return True
    try:
        get_drive_space(1)
        save_and_display_day()
        sleep(1)
        set_power_plan()
        subprocess.Popen(["taskkill", "/f", "/im", "spotify.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Spotify\\Data"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Spotify\\Browser\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Spotify\\Browser\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Spotify\\Browser\\GPUCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Steam\\htmlcache\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Steam\\htmlcache\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\SteamVR\\htmlcache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Microsoft\\OneDrive\\logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\WebCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~") + "\\AppData\\Local\\EpicGamesLauncher\\Saved\\webcache_4430", ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Innova\\4game\\CEF\\global\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Innova\\4game\\CEF\\global\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\password_is_eulen"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Riot Games\\League of Legends\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Program Files (x86)\\Steam\\appcache\\librarycache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Temp"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\NVIDIA"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\AMD"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Intel"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\USOShared\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\Rave\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\Microsoft\\EdgeUpdate\\Log"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\D3DSCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Epic Games\\EOSOverlay\\BrowserCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\Slack\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\NVIDIA Corporation\\NV_Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\Razer\\GameManager\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Program Files (x86)\\Ubisoft\\Ubisoft Game Launcher\\logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\Razer\\Razer Central\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\Razer\\Razer Central\\WebAppCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\Apple\\Installer Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\Razer\\Synapse3\\Log"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Razer\\Synapse3\\Log"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\Slack\\Service Worker\\CacheStorage"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\Desktop\\password_is_eulen"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Insurgency\\Saved\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Overwolf\\Log\\Apps"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Overwolf\\BrowserCache\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Overwolf\\BrowserCache\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\LocalLow\\uTorrent.WebView2\\EBWebView\\Default\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\LocalLow\\uTorrent.WebView2\\EBWebView\\Default\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\LocalLow\\Microsoft\\CryptnetUrlCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\Downloads\\password_is_eulen"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Razer\\Razer Central\\WebAppCache\\Service Worker\\CacheStorage"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Razer\\Razer Central\\WebAppCache\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Razer\\Razer Central\\WebAppCache\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Razer\\Razer Central\\WebAppCache\\GPUCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\OculusClient\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\OculusClient\\GPUCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\Slack\\GPUCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\Slack\\Code Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\Slack\\logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Program Files\\Oculus\\Support\\oculus-touch-tutorial\\TouchNUX2\\MontereySetup\\Content\\ProgramBinaryCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\ProgramData\\Razer\\GameManager\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Temp"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\FortniteGame\\Saved\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\WebCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\Appdata\\Roaming\\.minecraft\\webcache2"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\Appdata\\Roaming\\.minecraft\\logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Riot Games\\Riot Client\\Logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Eulen"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\\Roaming\\.minecraft\\bin"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Overwolf\\PackagesCache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Origin\\Origin\\cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\Spotify\\Storage"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\CrashDumps"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Roaming\\riot-client-ux\\Cache"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\FiveM\\FiveM.app\\crashes\\*"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~") + "\\AppData\\Local\\FiveM\\Fivem.app\\data\\server-cache-priv", ignore_errors=True)
        shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\FiveM\\FiveM.app\\logs"), ignore_errors=True)
        shutil.rmtree(os.path.expanduser("C:\\Windows.old"), ignore_errors=True)
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("C:\\Windows\\LiveKernelReports\\WATCHDOG")) for file in files if file.endswith(".dmp")]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("C:\\Windows\\Minidump")) for file in files if file.endswith(".dmp")]
        delete_windows_files_tmp()

        delete_files_with_prefix(directory_path, prefix_to_delete)
        delete_txt_files(filmora_folder_path)

        if is_eset_installed():

            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxcCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\FortniteGame\\Saved\\Logs")) for file in files if file.endswith(".log") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\RedM\\RedM.app\\data\\cache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxcCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\Wondershare\\Wondershare Filmora")) for file in files if file.endswith(".txt") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".toc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [f.unlink() for f in Path("C:\\Windows\\SoftwareDistribution\\Download").glob("*") if f.is_file() and (lambda p: p.unlink() if os.access(p, os.W_OK) else None)(Path(f)) if os.path.exists(f)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("C:\\Windows\\Prefetch\\")) for file in files if file.endswith(".pf") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [f.unlink() for f in Path("C:\\Windows\\LiveKernelReports\\").glob("*") if f.is_file() and (lambda p: p.unlink() if os.access(p, os.W_OK) else None)(Path(f)) if os.path.exists(f)]
            subprocess.run('powercfg.exe /hibernate off', shell=True, check=False)
            [f.unlink() for f in Path("C:\\").glob("hiberfil.sys") if f.is_file() and (lambda p: p.unlink() if os.access(p, os.W_OK) else None)(Path(f)) if os.path.exists(f)]
            sleep(0.4)
            subprocess.Popen("cleanmgr.exe").wait()
            sleep(0.4)
            subprocess.Popen('wsreset.exe').wait()
            subprocess.run(['taskkill', '/f', '/im', 'WinStore.App.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sleep(1)
            check_discord()
            check_battlenet()
            get_drive_space(2)
            sleep(1)
            get_drive_space(3)
            update_canvas(canvas)
            display_last_scan(canvas)
            print("Done! Thank You For Using Beta Version <3")
        if AVG_Check():
            remove_old_files("C:\\Program Files (x86)")
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files (x86)") for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files") for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files") for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\ProgramData") for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\FortniteGame\\Saved\\Logs")) for file in files if file.endswith(".log") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\RedM\\RedM.app\\data\\cache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\Wondershare\\Wondershare Filmora")) for file in files if file.endswith(".txt") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxcCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".toc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            subprocess.run('powercfg.exe /hibernate off', shell=True, check=False)
            [f.unlink() for f in Path("C:\\").glob("hiberfil.sys") if f.is_file()]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("C:\\Windows\\Prefetch\\")) for file in files if file.endswith(".pf") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [f.unlink() for f in Path("C:\\Windows\\LiveKernelReports\\").glob("*") if f.is_file()]
            sleep(0.4)
            subprocess.Popen("cleanmgr.exe").wait()
            sleep(0.4)
            subprocess.Popen('wsreset.exe').wait()
            subprocess.run(['taskkill', '/f', '/im', 'WinStore.App.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sleep(1)
            check_discord()
            check_battlenet()
            get_drive_space(2)
            sleep(1)
            get_drive_space(3)
            update_canvas(canvas)
            display_last_scan(canvas)
            print("Done! Thank You For Using Beta Version <3")
        if is_ea_installed():
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\Wondershare\\Wondershare Filmora")) for file in files if file.endswith(".txt") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\FortniteGame\\Saved\\Logs")) for file in files if file.endswith(".log") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\RedM\\RedM.app\\data\\cache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxcCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".toc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            subprocess.run('powercfg.exe /hibernate off', shell=True, check=False)
            [f.unlink() for f in Path("C:\\").glob("hiberfil.sys") if f.is_file()]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("C:\\Windows\\Prefetch\\")) for file in files if file.endswith(".pf") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [f.unlink() for f in Path("C:\\Windows\\LiveKernelReports\\").glob("*") if f.is_file()]
            sleep(0.4)
            subprocess.Popen("cleanmgr.exe").wait()
            sleep(0.4)
            subprocess.Popen('wsreset.exe').wait()
            subprocess.run(['taskkill', '/f', '/im', 'WinStore.App.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sleep(1)
            check_discord()
            check_battlenet()
            get_drive_space(2)
            sleep(1)
            get_drive_space(3)
            update_canvas(canvas)
            display_last_scan(canvas)
            print("Done! Thank You For Using Beta Version <3")
        if check_ram():
            remove_old_files("C:\\Program Files (x86)")
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files (x86)") for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files") for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files") for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\ProgramData") for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\ProgramData") for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".old")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".dmp")]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\Wondershare\\Wondershare Filmora")) for file in files if file.endswith(".txt") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\FortniteGame\\Saved\\Logs")) for file in files if file.endswith(".log") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\RedM\\RedM.app\\data\\cache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxcCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".toc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("C:\\Windows\\Prefetch\\")) for file in files if file.endswith(".pf") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
            [f.unlink() for f in Path("C:\\Windows\\LiveKernelReports\\").glob("*") if f.is_file()]
            sleep(0.4)
            subprocess.Popen("cleanmgr.exe").wait()
            sleep(0.4)
            subprocess.Popen('wsreset.exe').wait()
            subprocess.run(['taskkill', '/f', '/im', 'WinStore.App.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sleep(1)
            check_discord()
            check_battlenet()
            get_drive_space(2)
            sleep(1)
            get_drive_space(3)
            update_canvas(canvas)
            display_last_scan(canvas)
            print("Done! Thank You For Using Beta Version <3")

        remove_old_files("C:\\Program Files (x86)")
        [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files (x86)") for file in files if file.endswith(".dmp")]
        [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\Program Files") for file in files if file.endswith(".old")]
        remove_dmp_files("C:\\Program Files")
        [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\ProgramData") for file in files if file.endswith(".old")]
        [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk("C:\\ProgramData") for file in files if file.endswith(".dmp")]
        delete_local_files_tmp()
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".old")]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local")) for file in files if file.endswith(".dmp")]
        delete_roaming_files_tmp()
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".old")]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Roaming")) for file in files if file.endswith(".dmp")]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\FortniteGame\\Saved\\Logs")) for file in files if file.endswith(".log") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file),os.W_OK)]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\RedM\\RedM.app\\data\\cache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file),os.W_OK)]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\Wondershare\\Wondershare Filmora")) for file in files if file.endswith(".txt") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file), os.W_OK)]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxcCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file),os.W_OK)]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\AMD\\DxCache")) for file in files if file.endswith(".parc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file),os.W_OK)]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".bin") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file),os.W_OK)]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("~\\AppData\\Local\\NVIDIA\\DxCache")) for file in files if file.endswith(".toc") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file),os.W_OK)]
        subprocess.run('powercfg.exe /hibernate off', shell=True, check=False)
        [f.unlink() for f in Path("C:\\").glob("hiberfil.sys") if f.is_file()]
        [os.remove(os.path.join(root, file)) for root, _, files in os.walk(os.path.expanduser("C:\\Windows\\Prefetch\\")) for file in files if file.endswith(".pf") and os.path.isfile(os.path.join(root, file)) and not os.access(os.path.join(root, file),os.W_OK)]
        [f.unlink() for f in Path("C:\\Windows\\LiveKernelReports\\").glob("*") if f.is_file()]
        sleep(0.4)
        subprocess.Popen("cleanmgr.exe").wait()
        sleep(0.4)
        subprocess.Popen('wsreset.exe').wait()
        subprocess.run(['taskkill', '/f', '/im', 'WinStore.App.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(1)
        check_discord()
        check_battlenet()
        get_drive_space(2)
        sleep(1)
        get_drive_space(3)
        update_canvas(canvas)
        display_last_scan(canvas)
        print("Done! Thank You For Using Beta Version <3")
    except Exception as e:
            sleep(2)
            send_error_to_discord(str(e))

# Get Last Clean (Last Scan Day)
def save_and_display_day():
    current_date = datetime.now().strftime("%d/%m/%Y")

    directory_path = os.path.join(os.getenv('LOCALAPPDATA'), 'GreekProject', 'DoTLook-main', 'assets', 'frame0')

    os.makedirs(directory_path, exist_ok=True)

    file_path = os.path.join(directory_path, 'day.txt')

    with open(file_path, 'w') as file:
        file.write(current_date)

# Get GB Cleaned (Last Cleaned GB)
def get_drive_space(action):
    global c_drive_space_1
    global c_drive_space_2

    if action == 1:
        disk_usage = psutil.disk_usage("C:\\")
        c_drive_space_1 = int(disk_usage.free / (1024*1024*1024))
        return c_drive_space_1
    elif action == 2:
        disk_usage = psutil.disk_usage("C:\\")
        c_drive_space_2 = int(disk_usage.free / (1024*1024*1024))
        return c_drive_space_2
    elif action == 3:
        if c_drive_space_1 is None or c_drive_space_2 is None:
            return "C drive space not initialized"
        else:
            return c_drive_space_2 - c_drive_space_1

# Updates Canvas
def update_canvas(canvas):
    canvas.delete("last_clean")

    result = get_drive_space(3)
    if len(str(result)) == 2:
        canvas.create_text(
            450.0,
            320.0,
            anchor="nw",
            text=result,
            fill="#009bff",
            font=("Moul Regular", 68 * -1)
        )
    else:
        canvas.create_text(
            470.0,
            320.0,
            anchor="nw",
            text=result,
            fill="#009bff",
            font=("Moul Regular", 68 * -1)
        )

    file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'GreekProject', 'DoTLook-main', 'assets', 'frame0', 'last_clean.txt')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(f"{result}")
    else:
        with open(file_path, 'r') as file:
            content = file.read()

        with open(file_path, 'w') as file:
            file.write(f"{result}")

def update_canvas_last_time(canvas, current_day):
    canvas.delete("last_day")

    result = current_day
    if len(str(result)) == 2:
        canvas.create_text(
            450.0,
            320.0,
            anchor="nw",
            text=result,
            fill="#009bff",
            font=("Moul Regular", 68 * -1),
            tags="last_day"
        )
    else:
        canvas.create_text(
            470.0,
            320.0,
            anchor="nw",
            text=result,
            fill="#009bff",
            font=("Moul Regular", 68 * -1),
            tags="last_day"
        )

    file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'GreekProject', 'DoTLook-main', 'assets', 'frame0', 'day.txt')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(f"{result}")
    else:
        with open(file_path, 'r') as file:
            content = file.read()

        with open(file_path, 'w') as file:
            file.write(f"{result}")

# Display Last Clean + Scan
def display_last_clean(canvas):
    file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'GreekProject', 'DoTLook-main', 'assets', 'frame0', 'last_clean.txt')
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            if content.strip().isdigit():  # Check if content contains only digits
                if len(content.strip()) == 2:
                    canvas.create_text(
                        445.0,
                        320.0,
                        anchor="nw",
                        text=content.strip(),
                        fill="#009bff",
                        font=("Moul Regular", 68 * -1),
                        tags="last_clean"
                    )
                else:
                    canvas.create_text(
                        470.0,
                        320.0,
                        anchor="nw",
                        text=content.strip(),
                        fill="#009bff",
                        font=("Moul Regular", 68 * -1),
                        tags="last_clean"
                    )
            else:
                print("Corrupted Last_Clean.txt found! start a new scan!")
                canvas.create_text(
                    480.0,
                    320.0,
                    anchor="nw",
                    text="-",
                    fill="#009bff",
                    font=("Moul Regular", 68 * -1),
                    tags="last_clean"
                )
    except FileNotFoundError:
        canvas.create_text(
            480.0,
            320.0,
            anchor="nw",
            text="-",
            fill="#009bff",
            font=("Moul Regular", 68 * -1),
            tags="last_clean"
        )

def display_last_scan(canvas):
    file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'GreekProject', 'DoTLook-main', 'assets', 'frame0', 'day.txt')
    canvas.delete("last_day")

    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            try:
                last_date = datetime.strptime(content, "%d/%m/%Y")
                current_date = datetime.now()
                difference = (current_date - last_date).days
                result = difference

                x_position = 270.0 if difference < 10 else 250.0

                canvas.create_text(
                    x_position,
                    320.0,
                    anchor="nw",
                    text=result,
                    fill="#009bff",
                    font=("Moul Regular", 68 * -1),
                    tags="last_day"
                )
            except ValueError:
                canvas.create_text(
                    270.0,
                    320.0,
                    anchor="nw",
                    text="Invalid date format in file",
                    fill="#009bff",
                    font=("Moul Regular", 68 * -1),
                    tags="last_day"
                )
    except FileNotFoundError:
        canvas.create_text(
            270.0,
            320.0,
            anchor="nw",
            text="-",
            fill="#009bff",
            font=("Moul Regular", 68 * -1),
            tags="last_day"
        )

#Icon For App
icon_file_path = Path("~").expanduser() / Path("AppData/Local/GreekProject/DoTLook-main/assets/frame0/icon.ico")

window = Tk()
window.geometry("931x607")
window.configure(bg="#FFFFFF")
window.title("GreekProject | Cleaner")
window.resizable(False, False)
window.iconbitmap(icon_file_path)

def junk_page_blue():
    global button_3

    button_3.place(
        x=681.0,
        y=449.0,
        width=212.0,
        height=71.0
    )

    # Show images
    canvas.itemconfigure(image_4, state='normal')
    canvas.itemconfigure(image_5, state='normal')
    canvas.itemconfigure(image_6, state='normal')
    canvas.itemconfigure(image_9, state='normal')
    canvas.itemconfigure(image_10, state='normal')
    canvas.itemconfigure(image_11, state='normal')
    canvas.itemconfigure(image_14, state='hidden')

    # Hide images
    canvas.itemconfigure(image_13, state='hidden')

    # Show other items if needed
    canvas.itemconfigure("last_clean", state='normal')
    canvas.itemconfigure("last_day", state='normal')

def settings_page_blue():
    global button_1
    global button_2
    global button_3

    # Button place
    button_3.place(
        x=1081.0,
        y=449.0,
        width=212.0,
        height=71.0
    )

    # Hide images
    canvas.itemconfigure(image_4, state='hidden')
    canvas.itemconfigure(image_5, state='hidden')
    canvas.itemconfigure(image_6, state='hidden')
    canvas.itemconfigure(image_9, state='hidden')
    canvas.itemconfigure(image_10, state='hidden')
    canvas.itemconfigure(image_11, state='hidden')
    canvas.itemconfigure(image_14, state='hidden')

    canvas.itemconfigure(image_13, state='normal')

    # Hide other items if needed
    canvas.itemconfigure("last_clean", state='hidden')
    canvas.itemconfigure("last_day", state='hidden')

def creators_page_blue():
    global button_1
    global button_2
    global button_3

    # Button place
    button_3.place(
        x=1081.0,
        y=449.0,
        width=212.0,
        height=71.0
    )

    # Hide images
    canvas.itemconfigure(image_4, state='hidden')
    canvas.itemconfigure(image_5, state='hidden')
    canvas.itemconfigure(image_6, state='hidden')
    canvas.itemconfigure(image_9, state='hidden')
    canvas.itemconfigure(image_10, state='hidden')
    canvas.itemconfigure(image_11, state='hidden')
    canvas.itemconfigure(image_13, state='hidden')

    canvas.itemconfigure(image_14, state='normal')

    # Hide other items if needed
    canvas.itemconfigure("last_clean", state='hidden')
    canvas.itemconfigure("last_day", state='hidden')

# Global Stuff
button_1 = None
button_2 = None
button_3 = None
c_drive_space_1 = None
c_drive_space_2 = None

windows_info = get_windows_info()
cpu_info = get_cpu_info()
ram_gb = get_ram_info()
gpu_info = get_gpu_info()

#Admin Check
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=607,
    width=931,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

display_last_clean(canvas)
display_last_scan(canvas)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    96.0,
    303.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    97.0,
    87.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    87.0,
    588.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    309.0,
    335.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    511.0,
    335.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    357.0,
    117.0,
    image=image_image_6
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png")
)
button_1 = Button(
    window,
    image=button_image_1,
    borderwidth=0,
    bg="#0e56c1",
    activebackground="#0e56c1",
    activeforeground="#0e56c1",
    command=junk_page_blue,
    relief="flat"
)
button_1.place(
    x=9.0,
    y=134.0,
    width=177.67483520507812,
    height=45.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    window,
    image=button_image_2,
    borderwidth=0,
    bg="#0e56c1",
    activebackground="#0e56c1",
    activeforeground="#0e56c1",
    command=lambda: settings_page_blue(),
    relief="flat"
)
button_2.place(
    x=9.0,
    y=204.0,
    width=176.67483520507812,
    height=45.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    window,
    image=button_image_3,
    borderwidth=0,
    bg="#FFFFFF",
    activebackground="#FFFFFF",
    activeforeground="#FFFFFF",
    command=lambda: start_task(),
    relief="flat"
)
button_3.place(
    x=681.0,
    y=449.0,
    width=212.0,
    height=71.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    window,
    image=button_image_5,
    borderwidth=0,
    bg="#0e56c1",
    activebackground="#0e56c1",
    activeforeground="#0e56c1",
    command=lambda: creators_page_blue(),
    relief="flat"
)
button_5.place(
    x=11.0,
    y=474.0,
    width=174.67483520507812,
    height=45.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    window,
    image=button_image_6,
    borderwidth=0,
    bg="#0e56c1",
    activebackground="#0e56c1",
    activeforeground="#0e56c1",
    command=lambda: called_update(),
    relief="flat"
)
button_6.place(
    x=57.0,
    y=1560.0,
    width=59.0,
    height=20.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    97.0,
    35.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    562.0,
    578.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    351.0,
    398.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    562.0,
    398.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    804.0,
    265.99997853286436,
    image=image_image_11
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    562.0,
    303.0,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    557.0,
    287.0,
    image=image_image_14
)

canvas.create_text(
    220.0,
    583.0,
    anchor="nw",
    text=windows_info,
    fill="#808080",
    font=("Moul Regular", 12 * -1)
)

canvas.create_text(
    380.0,
    583.0,
    anchor="nw",
    text=cpu_info,
    fill="#808080",
    font=("Moul Regular", 12 * -1)
)

canvas.create_text(
    580.0,
    583.0,
    anchor="nw",
    text=f"{ram_gb}GB RAM",
    fill="#808080",
    font=("Moul Regular", 12 * -1)
)

canvas.create_text(
    700.0,
    583.0,
    anchor="nw",
    text=gpu_info,
    fill="#808080",
    font=("Moul Regular", 12 * -1)
)

# Check For Update
def check_for_updates_and_notify(current_version):
    repo_owner = "GreeceForFun"
    repo_name = "GreekProject-Cleaner"

    try:
        latest_version_str = get_latest_version_from_github(repo_owner, repo_name)

        current_version_obj = version.parse(current_version)
        latest_version_obj = version.parse(latest_version_str)

        if latest_version_obj > current_version_obj:
            button_6.place(
                x=57.0,
                y=560.0,
                width=59.0,
                height=20.0
            )
            sleep(2)
        else:
            return

    except requests.exceptions.RequestException as req_error:
        print("Error making the request:", req_error)
    except version.InvalidVersion as version_error:
        print("Error parsing version:", version_error)
    except Exception as e:
        print(f"{fg(1)}Error Checking For Update! Contact Us! {e}")
        send_error_to_discord(str(e))

def get_latest_version_from_github(repo_owner, repo_name):
    github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/Files"
    response = requests.get(github_api_url)

    try:
        response.raise_for_status()
        files = response.json()
        version_file = next(file for file in files if file["name"].startswith("version"))
        version_content_url = version_file["download_url"]
        return requests.get(version_content_url).text.strip()
    except (requests.exceptions.RequestException, StopIteration, KeyError, version.InvalidVersion) as e:
        raise Exception(f"{fg(1)}Error Getting New Version: {e}, Contact Us!")

def get_new_version(github_url, exe_filename):
    try:
        print(f"{fg(2)}Downloading New Version...")
        sleep(1)

        raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        response = requests.get(raw_url)

        if response.status_code == 200:
            with open(exe_filename, 'wb') as file:
                file.write(response.content)
            shutil.rmtree(os.path.expanduser("~\\AppData\\Local\\GreekProject"), ignore_errors=True)
            sleep(1)
            create_folder_update()
        else:
            print(f"{fg(1)}Failed To Download New Version. Download New Version Manually!")
    except Exception as e:
        print(f"{fg(1)}Failed To Download New Version. Download New Version Manually!")
        send_error_to_discord(str(e))

github_link = "https://github.com/GreeceForFun/GreekProject-Cleaner/blob/main/GreekProject.py"
exe_filename = "GreekProject.py"

current_directory = os.path.dirname(os.path.abspath(__file__))
destination_file_path = os.path.join(current_directory, exe_filename)

def called_update():
    print(f"{fg(2)}Starting Update...")
    sleep(2)
    get_new_version(github_link, destination_file_path)

#File Check (After Update)
def create_folder_update():
    try:
        appdata_local_path = os.path.join(os.getenv('LOCALAPPDATA'), 'GreekProject')
        github_url = 'https://github.com/GreeceForFun/DoTLook/archive/main.zip'

        create_folder_if_not_exists(appdata_local_path)

        if not os.listdir(appdata_local_path):
            print(f"{fg(2)}Downloading Updated Files...")
            sleep(5)
            download_and_extract_zip(github_url, appdata_local_path)
            print(f"{fg(2)}Done! Thank You For Using Our Cleaner",)
            sleep(2)
            sys.exit()
        else:
            pass
    except Exception as e:
        print(f"{fg(1)}Error Downloading Updated Files, Make Sure To Open As Admin & Try Again!")
        send_error_to_discord(str(e))
        sleep(10)
        sys.exit()

check_for_updates_and_notify(current_version)

canvas.itemconfigure(image_13, state='hidden')
canvas.itemconfigure(image_14, state='hidden')

window.resizable(False, False)
window.mainloop()

# Thanks To All Of My Friends For Supporting Me <3 (P / B / E / S / G / M / N / A)
