import string
import requests
import json
import random
import threading
import time
import sys
import os
from typing import Optional

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


# --- Configuration & Utility Functions ---

# Placeholder for custom colors/formatting (replace with your actual implementation)
def get_time_str():
    """Returns a formatted timestamp for console output."""
    return time.strftime("[%H:%M:%S]")

# Simplified color constants for basic readability
GREEN = '\033[92m'
RED = '\033[91m'
WHITE = '\033[97m'
RESET = '\033[0m'
INPUT_PROMPT = f"{get_time_str()} [INPUT]"
STATUS_VALID = f"{GREEN}VALID{RESET}"
STATUS_INVALID = f"{RED}INVALID{RESET}"
STATUS_ERROR = f"{RED}ERROR{RESET}"

# Default settings for the outgoing webhook notification
USERNAME_WEBHOOK = "Webhook Checker Bot"
AVATAR_WEBHOOK = "https://i.imgur.com/your-avatar-here.png" # Placeholder image URL
COLOR_WEBHOOK = 3066993 # Blue color decimal (0x2f3136)

# Global variables
WEBHOOK_URL_NOTIFY: Optional[str] = None # Webhook to send valid codes to
THREADS_NUMBER = 0

def handle_error(e: Exception, context: str = "Script"):
    """Handles exceptions gracefully and exits if critical."""
    print(f"{get_time_str()} {RED}[ERROR]{RESET} {context} failed: {e}")
    if context == "Module Import":
        sys.exit(1)

def is_valid_notify_webhook(url: str) -> bool:
    """Checks if the provided notification webhook URL is valid."""
    if not url.startswith("https://discord.com/api/webhooks/"):
        return False
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# --- Core Logic Functions ---

def send_notification_webhook(embed_content: dict):
    """Sends a notification to the configured webhook URL."""
    if not WEBHOOK_URL_NOTIFY:
        return

    payload = {
        'embeds': [embed_content],
        'username': USERNAME_WEBHOOK,
        'avatar_url': AVATAR_WEBHOOK
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.post(WEBHOOK_URL_NOTIFY, data=json.dumps(payload), headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"{get_time_str()} {RED}[ERROR]{RESET} Failed to send notification: {e}")

def generate_and_check_webhook():
    """Generates a random webhook URL and checks its status."""
    # Webhook ID is typically 18-20 digits. Using 19 as in the original.
    first_part = ''.join([str(random.randint(0, 9)) for _ in range(19)])
    
    # Webhook token is a base64-like string, typically 68 characters.
    token_chars = string.ascii_letters + string.digits + '-' + '_'
    second_part = ''.join(random.choice(token_chars) for _ in range(68))
    
    webhook_test_code = f"{first_part}/{second_part}"
    webhook_test_url = f"https://discord.com/api/webhooks/{webhook_test_code}"

    try:
        # Using a HEAD request is a quick way to check if the URL exists (status 200)
        # However, Discord often returns 404 for non-existent webhooks, 
        # and 200 for valid ones, making it a viable check.
        response = requests.head(webhook_test_url, timeout=5) 
        status_code = response.status_code
        
        if status_code == 200:
            print(f"{get_time_str()} {GREEN}[FOUND]{RESET} Status: {STATUS_VALID} Webhook: {WHITE}{webhook_test_url}{RESET}")
            
            if WEBHOOK_URL_NOTIFY:
                embed_content = {
                    'title': 'Webhook Found!',
                    'description': f"**Valid Webhook:**\n```{webhook_test_url}```",
                    'color': COLOR_WEBHOOK,
                    'footer': {
                        "text": USERNAME_WEBHOOK,
                        "icon_url": AVATAR_WEBHOOK,
                    }
                }
                send_notification_webhook(embed_content)
        else:
            # Discord often returns 404 for invalid webhooks
            print(f"{get_time_str()} {RED}[CHECK]{RESET} Status: {STATUS_INVALID} Webhook: {WHITE}{webhook_test_code}{RESET} (Code: {status_code})")
    except requests.exceptions.RequestException:
        print(f"{get_time_str()} {RED}[CHECK]{RESET} Status: {STATUS_ERROR} Webhook: {WHITE}{webhook_test_code}{RESET} (Connection Error)")

def run_generator():
    """Manages the thread pool for checking webhooks."""
    threads = []
    
    print(f"\n{get_time_str()} [INFO] Starting generator with {THREADS_NUMBER} threads...")
    
    try:
        for _ in range(THREADS_NUMBER):
            t = threading.Thread(target=generate_and_check_webhook)
            t.daemon = True # Allows the main program to exit even if threads are running
            t.start()
            threads.append(t)
            
        # Keep the main thread alive while worker threads are running
        while True:
            # Check if all threads are still alive. 
            # In an infinite loop generator, this is mainly to keep the main thread busy.
            time.sleep(1) 
    except KeyboardInterrupt:
        print(f"\n{get_time_str()} [INFO] Generator stopped by user.")
    except Exception as e:
        handle_error(e, "Generator Loop")

# --- Main Execution ---

if __name__ == "__main__":
    print("\n\n" + "="*40)
    print("      Discord Webhook Generator/Checker")
    print("="*40 + "\n")
    
    try:
        # 1. Ask about notification webhook
        webhook_notify_choice = input(f"{INPUT_PROMPT} Do you want to send valid webhooks to a notification webhook? (y/n) -> {RESET}").strip().lower()
        
        if webhook_notify_choice in ['y', 'yes']:
            while True:
                webhook_url_input = input(f"{INPUT_PROMPT} Notification Webhook URL -> {RESET}").strip()
                if is_valid_notify_webhook(webhook_url_input):
                    WEBHOOK_URL_NOTIFY = webhook_url_input
                    print(f"{get_time_str()} {GREEN}[INFO]{RESET} Notification webhook confirmed.")
                    break
                else:
                    print(f"{get_time_str()} {RED}[ERROR]{RESET} Invalid or unreachable webhook URL.")
        
        # 2. Get thread count
        while True:
            try:
                threads_number_input = input(f"{INPUT_PROMPT} Number of Threads -> {RESET}").strip()
                THREADS_NUMBER = int(threads_number_input)
                if THREADS_NUMBER > 0:
                    break
                else:
                    print(f"{get_time_str()} {RED}[ERROR]{RESET} Please enter a number greater than 0.")
            except ValueError:
                print(f"{get_time_str()} {RED}[ERROR]{RESET} Invalid input. Please enter an integer.")

        # 3. Start the generator
        run_generator()

    except Exception as e:
        handle_error(e, "Main Execution")