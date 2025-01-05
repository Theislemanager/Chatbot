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

# Read TheIsle.log file using FTP or local filesystem and send Discord Webhooks

## This works for Legacy and Evrima branch

Run the exe file and settings.json will be created in same directory as the launcher. Insert FTP and webhooks details and run the launcher again.

- Added local or ftp option in new release.
- Compile the chatbot.py using PyInstaller if you don't trust the release file. (python -m PyInstaller "chatbot.py" --onefile)
  
```
default_settings = {
                "source": "local",
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
                "webhook_urls": {
                    "LogTheIsleChatData": "https://discord.com/api/webhooks/chat_webhook_id/chat_webhook_token",
                    "LogTheIsleKillData": "https://discord.com/api/webhooks/kill_webhook_id/kill_webhook_token",
                    "LogTheIsleJoinData": "https://discord.com/api/webhooks/join_webhook_id/join_webhook_token",
                    "Custom": ""
                },
                "features": {
                    "LogTheIsleChatData": True,
                    "LogTheIsleKillData": True,
                    "LogTheIsleJoinData": True,
                    "Custom": False
                },
                "refresh_rate": 1,
                "capture_patterns": [
                    "LogTheIsleChatData",
                    "LogTheIsleKillData",
                    "LogTheIsleJoinData",
                    "Custom"
                ]
            }
```
