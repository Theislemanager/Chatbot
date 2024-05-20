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
                 # Use local option if running the program on same host as server.
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
                "capture_patterns": 
                [
                "LogTheIsleChatData:", # Captures Evrima Chat
                "LogIChat:", # Captures Legacy Chat
                "LogTheIsleCommandData:" # Captures Evrima admin/rcon commands
                ]
            }
```
