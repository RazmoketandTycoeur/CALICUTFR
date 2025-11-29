import concurrent.futures
import random
import subprocess
import sys
import os
import requests
import json
import threading
import time # Added for time functions

    # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                 @@@@@@@@@@@@@@@@@@@                                 
                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    
                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@             
                           @@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@          
                        @@@@@@@@@@@@@              @@@@@@@@@@@@@@@              @@@@@@@@@@@@@        
                       @@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@       
                       @@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@       
                        @@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@        
                                  @@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@                  
                                @@@@@@@@@@@@@                           @@@@@@@@@@@@@                
                               @@@@@@@@@@            @@@@@@@@@@@            @@@@@@@@@@               
                                @@@@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@@@                
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                         @@@@@@@@@@@             @@@@@@@@@@@                         
                                        @@@@@@@@@                   @@@@@@@@@                        
                                         @@@@@@        @@@@@@@        @@@@@@                         
                                                    @@@@@@@@@@@@@                                    
                                                   @@@@@@@@@@@@@@@                                   
                                                  @@@@@@@@@@@@@@@@@                                  
                                                  @@@@@@@@@@@@@@@@@                                  
                                                   @@@@@@@@@@@@@@@                                   
                                                    @@@@@@@@@@@@@                                    
                                                       @@@@@@@     
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# --- Definitions for Missing Utility Functions/Variables ---
# These are basic stand-ins required for the script to execute.
# You should replace these with your actual definitions if they exist
# in another file or module.

# Style Variables (colors, etc.)
reset = '\033[0m'
green = '\033[92m'
red = '\033[91m'
white = '\033[97m'
BEFORE = f"[{white}INFO{reset}]"
AFTER = f"{white}|{reset}"
BEFORE_GREEN = f"[{green}SUCCESS{reset}]"
AFTER_GREEN = f"{green}|{reset}"
GEN_VALID = f"[{green}VALID{reset}]"
GEN_INVALID = f"[{red}INVALID{reset}]"
INPUT = f"[{white}INPUT{reset}]"

# Default Webhook Settings (to be replaced)
username_webhook = "IP Checker Bot"
avatar_webhook = "" # Avatar URL
color_webhook = 3066993 # A blue/green color code

def current_time_hour():
    """Simulates the time function for display."""
    return time.strftime("%H:%M:%S")

def Title(text):
    """Simulates the function to change the console title."""
    sys.stdout.write(f"\033]0;{text}\a")
    sys.stdout.flush()

def ErrorModule(e):
    """Simulates import error handling."""
    print(f"Import Error: {e}")
    sys.exit(1)

def CheckWebhook(url):
    """Simulates webhook validation."""
    # A proper URL validation should be implemented here
    pass 

def ErrorNumber():
    """Simulates thread number error handling."""
    print(f"\n{BEFORE}{AFTER} {red}Error: Invalid Threads Number.{reset}")
    sys.exit(1)

def ErrorPlateform():
    """Simulates platform error handling."""
    print(f"\n{BEFORE}{AFTER} {red}Error: Unsupported Platform.{reset}")
    sys.exit(1)

def Error(e):
    """Simulates general error handling."""
    print(f"\n{BEFORE}{AFTER} {red}General Error: {e}{reset}")
    sys.exit(1)
# -----------------------------------------------------------

Title("Ip Generator")

try:
    # 1. User Input Handling
    webhook = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook ? (y/n) -> {reset}")
    if webhook.lower() in ['y', 'yes']:
        webhook_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {reset}")
        CheckWebhook(webhook_url)
    else:
        webhook_url = None

    try:
        # Ensure input is an integer and greater than 0
        threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads Number -> {reset}"))
        if threads_number <= 0:
             raise ValueError
    except ValueError:
        ErrorNumber()

    # 2. Webhook Sending Function Definition
    def SendWebhook(embed_content):
        if not webhook_url:
            return # Do nothing if webhook is not enabled
            
        payload = {
            'embeds': [embed_content],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }

        headers = {'Content-Type': 'application/json'}

        try:
            # Added timeout and HTTP status check
            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=5)
            response.raise_for_status() # Raise exception for HTTP errors (4xx or 5xx)
        except requests.RequestException as e:
            # Better error handling for webhook sending
            print(f"\n{BEFORE + current_time_hour() + AFTER} {red}Error sending webhook: {e}{reset}")
    
    # Using a Lock for shared global variables in a multi-threaded environment
    lock = threading.Lock()
    number_valid = 0
    number_invalid = 0

    # 3. IP Check Function
    def IpCheck():
        global number_valid, number_invalid

        # Use 'lock' to safely read the current counter values
        with lock:
            current_valid = number_valid
            current_invalid = number_invalid
            
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))

        # IMPORTANT: A ping timeout of 0.1s is too short. Increased to 1s.
        PING_TIMEOUT = 1 
        
        try:
            if sys.platform.startswith("win"):
                # Windows: -n 1 (count 1), -w 1000 (timeout 1000ms)
                result = subprocess.run(['ping', '-n', '1', '-w', str(int(PING_TIMEOUT*1000)), ip], capture_output=True, text=True, timeout=PING_TIMEOUT + 0.5)
            elif sys.platform.startswith("linux"):
                # Linux: -c 1 (count 1), -W 1 (timeout 1s)
                result = subprocess.run(['ping', '-c', '1', '-W', str(PING_TIMEOUT), ip], capture_output=True, text=True, timeout=PING_TIMEOUT + 0.5)
            else:
                ErrorPlateform()

            if result.returncode == 0:
                with lock:
                    number_valid += 1
                
                # Webhook is sent OUTSIDE the lock to prevent blocking other threads
                if webhook.lower() in ['y', 'yes']:
                    embed_content = {
                        'title': 'Ip Valid !',
                        'description': f"**Ip:**\n```{ip}```",
                        'color': color_webhook,
                        'footer': {
                            "text": username_webhook,
                            "icon_url": avatar_webhook,
                        }
                    }
                    SendWebhook(embed_content) 
                    
                # Logging output
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Logs: {white}{current_invalid} invalid - {current_valid + 1} valid{green} Status:  {white}Valid{green}  Ip: {white}{ip}{green}")
            else:
                with lock:
                    number_invalid += 1
                # Logging output
                print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Logs: {white}{current_invalid + 1} invalid - {current_valid} valid{red} Status: {white}Invalid{red} Ip: {white}{ip}{red}")
                
        except (subprocess.TimeoutExpired, Exception) as e:
            # Catches timeout from the subprocess or any other error
            with lock:
                number_invalid += 1
            # Logging output
            print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Logs: {white}{current_invalid + 1} invalid - {current_valid} valid{red} Status: {white}Error/Invalid{red} Ip: {white}{ip}{red} ({e.__class__.__name__})")
            
        # Update the title
        Title(f"Ip Generator - Invalid: {number_invalid} - Valid: {number_valid}")
        
    # 4. Thread Loop Function
    def run_ip_check_loop():
        """Function executed by each thread in an infinite loop."""
        while True:
            IpCheck()
            # time.sleep(0.01) # Uncomment to slow down the process slightly

    # 5. Main Execution Loop
    def Request():
        """Manages the creation and lifetime of the worker threads."""
        threads = []
        for _ in range(threads_number):
            # Create a dedicated thread that runs the infinite loop
            t = threading.Thread(target=run_ip_check_loop, daemon=True)
            threads.append(t)
            t.start()
            
        # The main thread waits for the worker threads to finish (which they won't 
        # because the loop is infinite), effectively keeping the script running.
        for t in threads:
            t.join() 
            
    # Run the continuous thread management once
    Request()
        
except Exception as e:
    Error(e)