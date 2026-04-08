import webview
import subprocess
import socket
import time
import threading
import os

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_n8n():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            subprocess.Popen(['n8n', 'start'], startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            subprocess.Popen(['npx.cmd', 'n8n', 'start'], startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception:
        pass

def check_and_load(window):
    retries = 30
    while retries > 0:
        if is_port_open(5678):
            window.load_url('http://localhost:5678')
            return
        time.sleep(1)
        retries -= 1
    
    error_html = "<html><body style='background:#1a1a1a;color:white;text-align:center;padding-top:20%;font-family:sans-serif;'><h2>Erreur : n8n introuvable</h2><p>Vérifiez que n8n est installé (npm install n8n -g)</p></body></html>"
    window.load_html(error_html)

def main():
    loading_html = "<html><body style='background:#1a1a1a;color:white;text-align:center;padding-top:20%;font-family:sans-serif;'><h2>Initialisation de n8n...</h2><div style='width:200px;height:4px;background:#333;margin:20px auto;'><div style='width:50%;height:100%;background:#ff6d5a;'></div></div></body></html>"
    
    if not is_port_open(5678):
        start_n8n()

    window = webview.create_window('n8n Launcher', html=loading_html, width=1280, height=800)
    threading.Thread(target=check_and_load, args=(window,), daemon=True).start()
    webview.start()

if __name__ == '__main__':
    main()