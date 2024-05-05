import ftplib
import os
import sys
import requests
import json
import time
import re

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
                # Use local option if running the program on same host as server.
                "source": "local",  # Default source set to local other option is ftp. Choose either "local" or "ftp"
                "local_path": "/path/to/log/files/TheIsle.log",  
                "ftp": {
                    "host": "example.com",
                    "username": "ftp_user",
                    "password": "ftp_password",
                    "remote_path": "/path/to/log/files",
                    "filename": "TheIsle.log",
                    "passive": True
                },
                "discord_webhook_url": "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token",
                "refresh": "1" # How often to check the log in seconds
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
            ftp.connect(ftp_settings["host"])
            ftp.login(ftp_settings["username"], ftp_settings["password"])
            ftp.cwd(ftp_settings["remote_path"])
            ftp.set_pasv(ftp_settings["passive"])  
            filename = ftp_settings["filename"]
            if filename not in ftp.nlst():
                print(f"File {filename} does not exist in the remote directory.")
                return None
            local_filename = os.path.join(os.getcwd(), filename)
            if last_position.get(filename):
                ftp.sendcmd("TYPE I")
                filesize = ftp.size(filename)
                if filesize > last_position[filename]:
                    with open(local_filename, "wb") as file:
                        ftp.retrbinary("RETR " + filename, file.write)
                    with open(local_filename, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        last_line = lines[-1].strip() if lines else None
                        return last_line
                else:
                    return None
            else:
                with open(local_filename, "wb") as file:
                    ftp.retrbinary("RETR " + filename, file.write)
                with open(local_filename, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    last_line = lines[-1].strip() if lines else None
                    return last_line
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
    last_position = {} 
    last_sent_line = None  

    while True:
        log_line = fetch_log_file(settings, last_position)
        if log_line:
            if 'LogTheIsleChatData:' in log_line or 'LogIChat:' in log_line:
                if log_line != last_sent_line:
                    send_discord_webhook(discord_webhook_url, log_line)
                    last_sent_line = log_line  
        else:
            print(f"Failed to fetch the log line from {filename}.")
        time.sleep(settings["refresh"]) 

if __name__ == "__main__":
    main()
