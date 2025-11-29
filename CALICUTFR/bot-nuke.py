import requests
import time
import sys
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

# --- Fonction d'envoi de message séquentiel ---
def send_webhook_message_sequentially(webhook_url, data, current_send, total_sends, webhook_index, num_webhooks):
    """
    Attempts to send a message and handles rate limiting (429) errors.
    """
    attempt = 0
    max_attempts = 5
    
    while attempt < max_attempts:
        attempt += 1
        try:
            sys.stdout.write(f"Sending {current_send}/{total_sends} [Webhook {webhook_index}/{num_webhooks}] (Attempt {attempt})... \r")
            sys.stdout.flush()

            response = requests.post(webhook_url, json=data)
            
            # --- Case 1: Success ---
            if response.status_code == 204:
                print(f"SUCCESS: Send {current_send}/{total_sends} via Webhook {webhook_index} completed.                              ")
                return True
            
            # --- Case 2: Rate Limiting (Code 429) ---
            elif response.status_code == 429:
                try:
                    error_data = response.json()
                    wait_time = error_data.get("retry_after", 1.0) 
                    
                    print(f"RATE LIMITED: Send {current_send}/{total_sends}. Waiting {wait_time:.3f}s (Attempt {attempt}/{max_attempts})...")
                    time.sleep(wait_time)
                
                except Exception:
                    print(f"RATE LIMITED: Send {current_send}/{total_sends}, JSON error. Waiting 1s (Attempt {attempt}/{max_attempts})...")
                    time.sleep(1)
            
            # --- Case 3: Other Irrecoverable Errors ---
            else:
                print(f"FAILURE: Send {current_send}/{total_sends} on Webhook {webhook_index}. Error {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"CONNECTION ERROR: Send {current_send}/{total_sends}. Exception occurred: {e}")
            return False
            
    print(f"FINAL FAILURE: Send {current_send}/{total_sends} on Webhook {webhook_index} failed after {max_attempts} attempts.")
    return False

# ----------------------------------------------------------------------
# --- Main Script Execution ---
# ----------------------------------------------------------------------

# --- Get User Inputs ---
bot_name = input("Bot Name: ")
message = input("Message to send: ")

# --- NOUVELLE DEMANDE : URL de l'Avatar ---
avatar_url = input("Bot Avatar URL (optional, leave blank to use default): ") 

# --- Get Webhook URLs ---
webhook_input = input("Discord Webhook URL(s) (separate by commas or spaces): ")

webhook_urls = [url.strip() for url in webhook_input.replace(',', ' ').split() if url.strip()]

if not webhook_urls:
    print("No webhook URL provided. Exiting script.")
    sys.exit(1)

num_webhooks = len(webhook_urls)
print(f"SUCCESS: {num_webhooks} Webhook(s) detected for sending.")

# --- Get Total Send Count ---
try:
    num_sends = int(input("Total number of messages to send: "))
    if num_sends <= 0:
        print("The number of sends must be greater than zero.")
        sys.exit(1)
except ValueError:
    print("Invalid input. The number of sends must be an integer.")
    sys.exit(1)

# --- Prepare the Request Payload ---
data = {
    "username": bot_name,
    "content": message
}

# --- Ajout conditionnel de l'avatar_url ---
if avatar_url:
    data["avatar_url"] = avatar_url
    print(f"INFO: Using custom avatar URL: {avatar_url}")
else:
    print("INFO: Using webhook's default avatar.")

# --- Sequential and Round-Robin Sending Loop ---
print(f"\nStarting sequential send of {num_sends} messages, distributed over {num_webhooks} webhook(s).")

for i in range(num_sends):
    webhook_index_to_use = i % num_webhooks
    current_webhook_url = webhook_urls[webhook_index_to_use]
    
    send_webhook_message_sequentially(
        current_webhook_url, 
        data, 
        i + 1, 
        num_sends, 
        webhook_index_to_use + 1,
        num_webhooks
    )

print("\nSequential multi-webhook operation completed.")