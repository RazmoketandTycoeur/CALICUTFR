import smtplib
import os
import time
from email.mime.text import MIMEText
from pwinput import pwinput  # pour masquer le mot de passe
MAX_MESSAGES = 10000  # sécurité

# ----------------------------
# Force all print statements to green
# ----------------------------
VERT = "\033[32m"
RESET = "\033[0m"

# Backup the original print function
original_print = print

# Redefine print to always include green color
def print(*args, **kwargs):
    original_print(VERT, end="")
    original_print(*args, **kwargs)
    original_print(RESET, end="\n")

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

# Codes ANSI pour couleur dans le terminal
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def main():
    print("===  Email SPAMER Sender ===\n")

    sender = input("Enter YOUR email address: ")
    password = input("Enter your email APP PASSWORD: ")
    recipient = input("Enter the CLIENT email address: ")

    try:
        count = int(input(f"How many emails do you want to send ? (1 to {MAX_MESSAGES}): "))
    except ValueError:
        print("Invalid number.")
        return

    if count < 1 or count > MAX_MESSAGES:
        print(f"Error: You must choose between 1 and {MAX_MESSAGES} emails.")
        return

    subject = input("Email subject: ")
    body = input("Email message: ")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            print("\nConnecting to the email server...")
            server.login(sender, password)
            print("Connected successfully!\n")

            for i in range(count):
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = sender
                msg["To"] = recipient

                # Affiche rouge avant envoi
                print(f"{RED}Sending email {i+1}/{count}...{RESET}")

                server.send_message(msg)

                # Affiche vert après envoi
                print(f"{GREEN}Email {i+1}/{count} sent successfully!{RESET}")

    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")


if __name__ == "__main__":
    main()
