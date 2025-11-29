# Copyright (c) RedTiger 
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import random
import threading
import requests
import time
import os
from datetime import datetime

        # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                    
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                  
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                  
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                   
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                      
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@             

"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# Configuration des couleurs
reset = "\033[0m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
white = "\033[97m"

BEFORE = red + "[" + white + "-" + red + "]" + white
BEFORE_GREEN = green + "[" + white + "+" + green + "]" + white
AFTER = white
AFTER_GREEN = white
GEN_VALID = green + "[" + white + "VALID" + green + "]" + white
GEN_INVALID = red + "[" + white + "INVALID" + red + "]" + white
INPUT = red + "[" + white + ">" + red + "]" + white

# Fonctions utilitaires
def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text):
    for line in text.splitlines():
        print(line)
        time.sleep(0.02)

def ErrorModule(e):
    print(f"{BEFORE} Error Module: {e}")
    time.sleep(2)
    return

def ErrorNumber():
    print(f"{BEFORE} Error Number.")
    time.sleep(2)
    return

def Error(e):
    print(f"{BEFORE} Error: {e}")
    time.sleep(2)
    return

# Bannière Discord
discord_banner = f"""
{blue}╔═╗╦╔╦╗╔═╗╦ ╦╔╗ ╔═╗╦╔╗ ╔╦╗╦ ╦╔═╗╔╗╔╔╦╗
{blue}╠═╝║ ║ ║ ║║║║╠╩╗║╣ ║╠╩╗ ║║║ ║╠═╣║║║ ║ 
{blue}╩  ╩ ╩ ╚═╝╚╩╝╚═╝╚═╝╩╚═╝╩ ╩╚═╝╩ ╩╝╚╝ ╩ 
"""

def ChoiceMultiTokenDiscord():
    print(f"{BEFORE} Enter Discord tokens (separated by '|')")
    tokens_input = input(f"{INPUT} Tokens -> {reset}")
    tokens = [token.strip() for token in tokens_input.split("|") if token.strip()]
    
    if not tokens:
        print(f"{BEFORE} No tokens provided!")
        time.sleep(2)
        return ChoiceMultiTokenDiscord()
    
    return tokens

def ChoiceMultiChannelDiscord():
    print(f"{BEFORE} Enter Discord channel IDs (separated by '|')")
    print(f"{BEFORE} Format: channel_id or full_url")
    print(f"{BEFORE} Example: 123456789012345678 or https://discord.com/channels/123/456")
    
    channels_input = input(f"{INPUT} Channels -> {reset}")
    channels = []
    
    for channel_input in channels_input.split("|"):
        channel_input = channel_input.strip()
        if not channel_input:
            continue
            
        # Si c'est une URL Discord complète, extraire l'ID du canal
        if "discord.com/channels/" in channel_input:
            try:
                # Extraire le dernier segment de l'URL qui est l'ID du canal
                channel_id = channel_input.split("/")[-1]
                channels.append(channel_id)
            except:
                print(f"{BEFORE} Invalid URL format: {channel_input}")
        else:
            # Si c'est déjà un ID, l'utiliser directement
            channels.append(channel_input)
    
    if not channels:
        print(f"{BEFORE} No valid channels provided!")
        time.sleep(2)
        return ChoiceMultiChannelDiscord()
    
    print(f"{BEFORE_GREEN} Found {len(channels)} channels")
    return channels

def raid(tokens, channels, message):
    try:
        token = random.choice(tokens)
        channel = random.choice(channels)
        response = requests.post(
            f"https://discord.com/api/channels/{channel}/messages", 
            json={'content': message},
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        response.raise_for_status()
        print(f"{BEFORE_GREEN}{current_time_hour()}{AFTER_GREEN} {GEN_VALID} Message: {white}{message_sensur}{green} Channel: {white}{channel}{green} Status: {white}Send{green}")
    except Exception as e:
        status_code = ""
        if hasattr(e, 'response') and e.response is not None:
            status_code = f"Error {e.response.status_code}"
        else:
            status_code = "Error (No response)"
        
        print(f"{BEFORE}{current_time_hour()}{AFTER} {GEN_INVALID} Message: {white}{message_sensur}{red} Channel: {white}{channel}{red} Status: {white}{status_code}{red}")

try:
    def Title(title):
        print(f"\n{red}╔═══════════════════════════════════════════════════════════════╗{white}")
        print(f"{red}║ {white}{title.center(67)}{red} ║{white}")
        print(f"{red}╚═══════════════════════════════════════════════════════════════╝{white}")

    Title("Discord Token Server Raid")

    Slow(discord_banner)
    tokens = ChoiceMultiTokenDiscord()
    channels = ChoiceMultiChannelDiscord()

    message = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Spam Message -> {reset}")
    message_len = len(message)
    if message_len > 10:
        message_sensur = message[:10] + "..."
    else:
        message_sensur = message

    try:
        threads_number = int(input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Threads Number (recommended: 2, 4) -> {reset}"))
    except:
        ErrorNumber()
        threads_number = 2

    def request():
        threads = []
        try:
            for _ in range(threads_number):
                t = threading.Thread(target=raid, args=(tokens, channels, message))
                t.start()
                threads.append(t)
        except:
            ErrorNumber()

        for thread in threads:
            thread.join()

    while True:
        request()
        
except Exception as e:
    Error(e)
except KeyboardInterrupt:
    print(f"\n{BEFORE} Script interrupted by user.")