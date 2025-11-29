import requests
import time
import json
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


def spam_webhook(webhook_url, message_content, count, delay=0.5):
    """
    Sends a message repeatedly to a Discord Webhook.

    :param webhook_url: The full Discord Webhook URL.
    :param message_content: The content of the message to send.
    :param count: The number of times to send the message.
    :param delay: Delay in seconds between each message to respect rate limits.
    """
    if not all([webhook_url, message_content, count]):
        print("Error: All parameters (URL, content, count) must be provided.")
        return

    # Data payload for the POST request
    payload = {
        "content": message_content
        # You can add "username" or "avatar_url" here if you want to customize the sender name
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    print(f"\n--- Starting Spamming ({count} times) ---")
    
    sent_count = 0
    
    for i in range(count):
        try:
            # Send the POST request to the Webhook URL
            response = requests.post(webhook_url, headers=headers, json=payload)
            
            # Discord returns 204 No Content on success for Webhook POST
            if response.status_code == 204:
                sent_count += 1
                print(f"[{i + 1}/{count}] Message sent successfully.")
            
            # Handle Discord Rate Limits (Error 429)
            elif response.status_code == 429:
                data = response.json()
                retry_after = data.get('retry_after', 1) / 1000.0  # Discord returns ms, convert to seconds
                print(f"RATE LIMITED! Waiting for {retry_after:.2f} seconds before retrying...")
                time.sleep(retry_after)
                # Retry the message attempt without incrementing 'i' in the loop
                continue 
            
            # Handle other errors (e.g., 400 Bad Request, 404 Not Found)
            else:
                print(f"[{i + 1}/{count}] ERROR: Failed to send message (Status: {response.status_code}).")
                print("Response content:", response.text)
                # Stop if a major error occurs to avoid excessive retries on a bad link
                break

        except requests.exceptions.RequestException as e:
            print(f"[{i + 1}/{count}] Connection Error: {e}")
            break
        
        # Wait a small delay between messages to mitigate rate limiting
        time.sleep(delay)

    print(f"\n--- Spamming Finished ---")
    print(f"Total successful messages sent: {sent_count}")
    print(f"Total attempts: {count}")
    

# --- Main script execution ---

print("--- DISCORD WEBHOOK SPAMMER TOOL ---")

# 1. Ask the user for required inputs
WEBHOOK_LINK = input("Enter the full Discord Webhook URL: ")
MESSAGE_CONTENT = input("Enter the message content to send: ")

while True:
    try:
        # Get and validate the number of messages
        MESSAGE_COUNT = int(input("Enter the number of times to send the message: "))
        if MESSAGE_COUNT <= 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# 2. Execute the spam function
spam_webhook(WEBHOOK_LINK, MESSAGE_CONTENT, MESSAGE_COUNT)