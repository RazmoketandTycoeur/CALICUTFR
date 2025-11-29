import requests
import sys
import time
from datetime import datetime
import os

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


# --- Minimal Placeholders for Missing Custom Functions/Variables ---
# The previous errors (NameError) indicated that these were missing.
# If these functions/variables exist in another utility file, replace this
# block with the correct 'from your_module import ...' line.

class CustomColors:
    """Minimal class to simulate custom color variables."""
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"

# Simulating custom variables and constants
red = CustomColors.RED
white = CustomColors.WHITE
INFO_ADD = "[+]" # Placeholder for a custom info indicator
BEFORE = "["
AFTER = "]"
INPUT = ">>"

def Title(text):
    """Simulates a custom function to set the terminal title."""
    print(f"\n--- {text} ---")

def Slow(text):
    """Simulates a function for slow/typewriter-style printing."""
    # This simplified version just prints the text immediately
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        # time.sleep(0.005) # Uncomment for actual slow printing
    print()

def current_time_hour():
    """Simulates a function to get the current time (e.g., [HH:MM])."""
    return datetime.now().strftime("%H:%M")

def CheckWebhook(url):
    """Simulates a custom function to validate the webhook URL format."""
    # In a real scenario, this would check if the URL looks like a Discord webhook
    return "discord.com/api/webhooks" in url or "discordapp.com/api/webhooks" in url

def Error(message):
    """Simulates a custom error reporting function."""
    print(f"{CustomColors.RED}ERROR: {message}{CustomColors.RESET}")
    sys.exit(1) # Exit the script after an error

def ErrorWebhook():
    """Simulates a custom function for invalid webhook error."""
    Error("Invalid Webhook URL format.")

def Continue():
    """Simulates a function to pause and wait for user input."""
    input("\nPress Enter to continue...")

def Reset():
    """Simulates a function to restart or reset the state."""
    print("Resetting script state...")
    # In a real script, this would typically be a loop or function call

# The original function 'ErrorModule' is kept here in case it's defined elsewhere
def ErrorModule(e):
    """Placeholder for the original ErrorModule function."""
    Error(f"Module Import Error: {e}")
    
# --- End of Placeholders ---

# The original incorrect try/except around import is removed.

Title("Discord Webhook Info")

try:
    def get_webhook_info(webhook_url):
        """Fetches and displays information about a Discord webhook."""
        
        headers = {
            'Content-Type': 'application/json',
        }

        # Making the request and checking for a valid response
        response = requests.get(webhook_url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        webhook_info = response.json()

        webhook_id = webhook_info.get('id', "None")
        webhook_token = webhook_info.get('token', "None")
        webhook_name = webhook_info.get('name', "None")
        webhook_avatar = webhook_info.get('avatar', "None")
        
        # Translating 'webhook utilisateur' to 'User Webhook'
        webhook_type = "Bot" if webhook_info.get('type') == 1 else "User Webhook" 
        
        channel_id = webhook_info.get('channel_id', "None")
        guild_id = webhook_info.get('guild_id', "None") 

        Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} ID         : {white}{webhook_id}{red}
 {INFO_ADD} Token      : {white}{webhook_token}{red}
 {INFO_ADD} Name       : {white}{webhook_name}{red}
 {INFO_ADD} Avatar     : {white}{webhook_avatar}{red}
 {INFO_ADD} Type       : {white}{webhook_type}{red}
 {INFO_ADD} Channel ID : {white}{channel_id}{red}
 {INFO_ADD} Server ID  : {white}{guild_id}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

        if 'user' in webhook_info:
            user_info = webhook_info['user']
            
            user_id = user_info.get('id', "None")
            username = user_info.get('username', "None")
            display_name = user_info.get('global_name', "None") 
            discriminator = user_info.get('discriminator', "None") 
            user_avatar = user_info.get('avatar', "None")
            user_flags = user_info.get('flags', "None")
            accent_color = user_info.get('accent_color', "None")
            avatar_decoration = user_info.get('avatar_decoration_data', "None")
            banner_color = user_info.get('banner_color', "None")

            Slow(f"""{red}User information associated with the Webhook:
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} ID          : {white}{user_id}{red}
 {INFO_ADD} Username    : {white}{username}{red}
 {INFO_ADD} Display Name: {white}{display_name}{red}
 {INFO_ADD} Discriminator: {white}{discriminator}{red}
 {INFO_ADD} Avatar      : {white}{user_avatar}{red}
 {INFO_ADD} Public Flags: {white}{user_flags}{red} 
 {INFO_ADD} Accent Color: {white}{accent_color}{red}
 {INFO_ADD} Decoration  : {white}{avatar_decoration}{red}
 {INFO_ADD} Banner Color: {white}{banner_color}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)

    # Main execution block
    webhook_url = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {CustomColors.RESET}")
    
    if not CheckWebhook(webhook_url):
        ErrorWebhook() 
    
    get_webhook_info(webhook_url)
    Continue()
    Reset()

except requests.exceptions.HTTPError as errh:
    # Handle HTTP errors (e.g., 404 Not Found, 401 Unauthorized)
    Error(f"HTTP Error: {errh}")
except requests.exceptions.RequestException as err:
    # Handle general request errors (e.g., connection issues)
    Error(f"Request Error: {err}")
except Exception as e:
    # Handle other unexpected errors
    Error(e)