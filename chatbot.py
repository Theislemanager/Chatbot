import ftplib
import os
import sys
import requests
import json
import time
import re

print(r"""
████████╗██╗░░██╗███████╗  ██╗░██████╗██╗░░░░░███████╗
╚══██╔══╝██║░░██║██╔════╝  ██║██╔════╝██║░░░░░██╔════╝
░░░██║░░░███████║█████╗░░  ██║╚█████╗░██║░░░░░█████╗░░
░░░██║░░░██╔══██║██╔══╝░░  ██║░╚═══██╗██║░░░░░██╔══╝░░
░░░██║░░░██║░░██║███████╗  ██║██████╔╝███████╗███████╗
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚═╝╚═════╝░╚══════╝╚══════╝

███╗░░░███╗░█████╗░███╗░░██╗░█████╗░░██████╗░███████╗██████╗░  
████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝░██╔════╝██╔══██╗  
██╔████╔██║███████║██╔██╗██║███████║██║░░██╗░█████╗░░██████╔╝  
██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██║░░╚██╗██╔══╝░░██╔══██╗  
██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║╚██████╔╝███████╗██║░░██║  
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚═╝  

░█████╗░██╗░░██╗░█████╗░████████╗██████╗░░█████╗░████████╗
██╔══██╗██║░░██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
██║░░╚═╝███████║███████║░░░██║░░░██████╦╝██║░░██║░░░██║░░░
██║░░██╗██╔══██║██╔══██║░░░██║░░░██╔══██╗██║░░██║░░░██║░░░
╚█████╔╝██║░░██║██║░░██║░░░██║░░░██████╦╝╚█████╔╝░░░██║░░░
░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═════╝░░╚════╝░░░░╚═╝░░░

Select "local" or "ftp" in source field
""")

def load_settings():
    try:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            try:
                app_full_path = os.path.realpath(__file__)
                application_path = os.path.dirname(app_full_path)
            except NameError:
                application_path = os.getcwd()

        settings_file = os.path.join(application_path, "settings.json")

        if not os.path.exists(settings_file):
            default_settings = {
                "source": "local",  # Default source set to local other option is ftp. Choose either "local" or "ftp"
                "local_path": "/path/to/log/files/TheIsle.log",  
                "ftp": {
                    "host": "example.com",
                    "port": 21,
                    "username": "ftp_user",
                    "password": "ftp_password",
                    "remote_path": "/path/to/log/files",
                    "filename": "TheIsle.log",
                    "passive": True
                },
                "discord_webhook_url": "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token",
                "refresh_rate": 1, # Select the refresh rate for checking log file
                "capture_patterns": [
                    "LogTheIsleChatData:",
                    "LogIChat:",
                    "LogTheIsleCommandData:"
                ]
            }

            with open(settings_file, "w") as f:
                json.dump(default_settings, f, indent=4)
                print("Created settings.json with default settings.")

        with open(settings_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error:", e)
        return None

def fetch_log_file(settings, last_position):
    try:
        if settings["source"] == "local":
            filename = settings["local_path"]
            if not os.path.exists(filename):
                print(f"File {filename} does not exist.")
                return None
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                last_line = lines[-1].strip() if lines else None
                return last_line
        elif settings["source"] == "ftp":
            ftp_settings = settings["ftp"]
            ftp = ftplib.FTP()
            ftp.connect(ftp_settings["host"], ftp_settings.get("port", 21))
            ftp.login(ftp_settings["username"], ftp_settings["password"])
            ftp.cwd(ftp_settings["remote_path"])
            ftp.set_pasv(ftp_settings["passive"])  
            filename = ftp_settings["filename"]
            local_filename = os.path.join(os.getcwd(), filename)
            try:
                with open(local_filename, "wb") as file:
                    ftp.retrbinary("RETR " + filename, file.write)
                with open(local_filename, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    last_line = lines[-1].strip() if lines else None
                    return last_line
            except ftplib.error_perm as e:
                print(f"Failed to retrieve the file: {e}")
                return None
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        if 'ftp' in locals():
            ftp.quit()

def send_discord_webhook(webhook_url, message):
    payload = {"content": f"`{message}`"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

def print_settings(settings):
    print("Settings:")
    for key, value in settings.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

def main():
    settings = load_settings()
    print_settings(settings)
    source = settings["source"]
    filename = settings["local_path"]
    discord_webhook_url = settings["discord_webhook_url"]
    refresh_rate = settings.get("refresh_rate", 1)
    capture_patterns = settings.get("capture_patterns", []) 
    last_position = {} 
    last_sent_line = None  

    while True:
        log_line = fetch_log_file(settings, last_position)
        if log_line:
            for pattern in capture_patterns:
                if pattern in log_line:
                    log_line_without_timestamp = re.sub(r'\[\d{4}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}:\d{3}\]\[\d+\]', '', log_line)
                    log_line_without_verbose = log_line_without_timestamp.replace("Verbose: ", "")
                    if log_line_without_verbose != last_sent_line:
                        send_discord_webhook(discord_webhook_url, log_line_without_verbose)
                        last_sent_line = log_line_without_verbose
                    break
        else:
            print(f"Failed to fetch the log line from {filename}.")
        time.sleep(refresh_rate)

if __name__ == "__main__":
    main()
