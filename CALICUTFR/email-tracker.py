import os
from bs4 import BeautifulSoup
import requests
import time
# Assuming external functions/constants are imported from another module or defined elsewhere
# from your_module import ErrorModule, Title, ChoiceUserAgent, Slow, osint_banner, current_time_hour, BEFORE, AFTER, INFO, INPUT, reset, Censored, WAIT, BEFORE_GREEN, AFTER_GREEN, GEN_VALID, GEN_INVALID, white, red, Continue, Reset, Error

# For demonstration, basic imports are kept, and undefined functions are assumed to be defined elsewhere.

    # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                          ...:----:...                                              
                                     .:=#@@@@@@@@@@@@@@%*-..                                        
                                  .:#@@@@@@@%#*****#%@@@@@@@+..                                     
                               ..-@@@@@%-...... ........+@@@@@@..                                   
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.                                  
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.                                
                            .#@@@%.                 .=@@@@@=. .@@@@-.                               
                           .=@@@#.                    .:%@@@*. -@@@%:.                              
                           .%@@@-                       .*@@*. .+@@@=.                              
                           :@@@#.                              .-@@@#.                              
                           -@@@#                                :%@@@.                              
                           :@@@#.                              .-@@@#.                              
                           .%@@@-.                             .+@@@=.                              
                           .+@@@#.                             -@@@%:.                              
                            .*@@@%.                          .:@@@@-.                               
                             .+@@@@=..                     ..*@@@@:.                                
                               :%@@@@-..                ...+@@@@*.                                  
                               ..-@@@@@%=...         ...*@@@@@@@@#.                                 
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.                              
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.                            
                                        .....:::::::....       ...+@@@@%:                           
                                                                  ..+@@@@%-.                        
                                                                    ..=@@@@%-.                      
                                                                      ..=@@@@@=.                    
                                                                         .=%@@@@=.                  
                                                                          ..-%@@@-.                 
                                                                             .... 

"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError as e:
    # Use a standard Python exception handling for import errors
    # If ErrorModule is a custom function, replace or define it.
    print(f"Error importing modules: {e}")
    # ErrorModule(e) # Uncomment if ErrorModule is defined
    exit(1)


# Title("Email Tracker") # Uncomment if Title is defined

def instagram(email):
    """Checks if the given email is associated with an Instagram account."""
    try:
        # user_agent = ChoiceUserAgent() # Assuming ChoiceUserAgent() is called once globally
        global user_agent # Use global user_agent selected outside this function
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/'
        }

        data = {"email": email}

        # Step 1: Get signup page to obtain CSRF token
        response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        if response.status_code != 200:
            return f"Error: Status Code {response.status_code} in Step 1."

        token = session.cookies.get('csrftoken')
        if not token:
            return "Error: CSRF Token Not Found."

        headers["x-csrftoken"] = token
        headers["Referer"] = "https://www.instagram.com/accounts/emailsignup/"

        # Step 2: Post email to check availability
        response = session.post(
            url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            # Check for indicators that the email is taken
            response_text = response.text
            if "Another account is using the same email." in response_text or "email_is_taken" in response_text:
                return True
            return False
        
        return f"Error: Status Code {response.status_code} in Step 2."
    
    except Exception as e:
        return f"Error: {e}"

def twitter(email):
    """Checks if the given email is associated with a Twitter (X) account."""
    try:
        session = requests.Session()
        # Note: This API endpoint may be deprecated or rate-limited.
        response = session.get(
            url="https://api.twitter.com/i/users/email_available.json",
            params={"email": email}
        )
        if response.status_code == 200:
            return response.json().get("taken", False) # Default to False if key missing
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def pinterest(email):
    """Checks if the given email is associated with a Pinterest account."""
    try:
        session = requests.Session()
        # Note the use of json.dumps or proper formatting for the 'data' parameter in production
        # Keeping original string formatting for consistency with the provided script
        data_param = '{"options": {"email": "' + email + '"}, "context": {}}'
        
        response = session.get(
            "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
            params={"source_url": "/", "data": data_param}
        )

        if response.status_code == 200:
            data = response.json().get("resource_response", {})
            message = data.get("message")
            if message == "Invalid email.":
                return False
            # Check if 'data' field exists and is NOT False (indicating email exists/taken)
            return data.get("data") is not False
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def imgur(email):
    """Checks if the given email is associated with an Imgur account."""
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://imgur.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }

        # Step 1: Get registration page (might be needed for cookies/session setup)
        session.get("https://imgur.com/register?redirect=%2Fuser", headers=headers)

        headers["X-Requested-With"] = "XMLHttpRequest"

        data = {'email': email}
        # Step 2: Check email availability via AJAX endpoint
        response = session.post('https://imgur.com/signin/ajax_email_available', headers=headers, data=data)

        if response.status_code == 200:
            data = response.json().get('data', {})
            # 'available': True means the email is NOT taken (False in this function's context)
            if data.get("available") is True:
                return False
            if "Invalid email domain" in response.text:
                return False # Not an existing account, but an invalid email structure/domain
            return True # Email is not available, thus it's taken
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def patreon(email):
    """Checks if the given email is associated with a Plurk account (Original script used Plurk URL)."""
    # NOTE: The provided script uses 'https://www.plurk.com/Users/isEmailFound'
    # but the function name is 'Patreon'. I'll keep the name 'patreon' but use the Plurk URL.
    # If the intent was to check Patreon, the URL needs to be corrected to a Patreon endpoint.
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            # Changed 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' to standard English preference
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            # Using Plurk Origin as per the original script's logic
            'Origin': 'https://www.plurk.com',
            'DNT': '1',
            'Connection': 'keep-alive',
        }

        data = {'email': email}
        # Plurk check
        response = session.post('https://www.plurk.com/Users/isEmailFound', headers=headers, data=data)
        
        if response.status_code == 200:
            # Assuming 'True' in the response text means email is found/taken
            return "True" in response.text
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def spotify(email):
    """Checks if the given email is associated with a Spotify account."""
    # NOTE: The provided script uses a suspicious URL: 'https://spclient.wg.spotify.com/signup/public/v1/account'
    # which is likely incorrect or defunct. Standard Spotify checks usually involve a registration endpoint.
    # Keeping the original logic structure but noting the unreliable URL.
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        params = {'validate': '1', 'email': email}
        # Using the original (possibly incorrect/defunct) URL
        response = session.get('https://spclient.wg.spotify.com/signup/public/v1/account',
                                headers=headers,
                                params=params)
        
        if response.status_code == 200:
            # Assuming status 20 means email is taken/valid
            status = response.json().get("status")
            return status == 20
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def firefox(email):
    """Checks if the given email is associated with a Firefox account."""
    try:
        session = requests.Session()
        data = {"email": email}
        response = session.post("https://api.accounts.firefox.com/v1/account/status", data=data)

        if response.status_code == 200:
            # Firefox status API returns JSON, checking if 'exists' is not false
            # Assuming 'false' in response text indicates *not* taken/does not exist
            # The API often returns {"exists": true/false}
            return "false" not in response.text
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def last_pass(email):
    """Checks if the given email is associated with a LastPass account."""
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Referer': 'https://lastpass.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }
        
        # Parameters for the GET request
        params = {
            'check': 'avail',
            'skipcontent': '1',
            'mistype': '1',
            'username': email,
        }
        
        # The URL in the original script is redundant/re-constructs the query string poorly.
        # We should primarily rely on the `params` dictionary for GET requests.
        # Keeping the URL structure but relying on `params`
        response = session.get(
            'https://lastpass.com/create_account.php',
            params=params,
            headers=headers
        )
        
        if response.status_code == 200:
            # Assuming "no" in response text means 'not available' or 'already registered'
            # LastPass typically uses "no" to indicate the email/username is taken
            if "no" in response.text:
                return True
            return False
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def archive(email):
    """Checks if the given email is associated with an Archive.org account."""
    try:
        global user_agent
        session = requests.Session()

        # The Content-Type and data structure suggest a multipart/form-data request,
        # which is complex to construct manually. Requests' 'files' or 'data' for x-www-form-urlencoded
        # or properly formed multipart data should be used.
        # Keeping the original complex string data for faithful translation, but noting potential issues.
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            # Content-Type header MUST match the actual body format
            'Content-Type': 'multipart/form-data; boundary=---------------------------', 
            'Origin': 'https://archive.org',
            'Connection': 'keep-alive',
            'Referer': 'https://archive.org/account/signup',
            'Sec-GPC': '1',
            'TE': 'Trailers',
        }

        # NOTE: Manually constructed multipart data is fragile. 
        # The boundary needs to match the one in the Content-Type.
        boundary = '---------------------------'
        data_body = (
            f'{boundary}\r\nContent-Disposition: form-data; name="input_name"\r\n\r\nusername\r\n'
            f'{boundary}\r\nContent-Disposition: form-data; name="input_value"\r\n\r\n{email}\r\n'
            f'{boundary}\r\nContent-Disposition: form-data; name="input_validator"\r\n\r\ntrue\r\n'
            f'{boundary}\r\nContent-Disposition: form-data; name="submit_by_js"\r\n\r\ntrue\r\n'
            f'{boundary}--\r\n' # Closing boundary
        )
        
        # Ensure the header uses the correct, complete boundary:
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary.strip("-")}' # Correcting boundary format

        response = session.post('https://archive.org/account/signup', headers=headers, data=data_body)
        
        if response.status_code == 200:
            # Check for the email taken message
            return "is already taken." in response.text
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def pornhub(email):
    """Checks if the given email is associated with a PornHub account."""
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en,en-US;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Step 1: Get signup page to obtain CSRF token
        response = session.get("https://www.pornhub.com/signup", headers=headers)
        
        if response.status_code == 200:
            # Parse the token from the HTML content
            soup = BeautifulSoup(response.content, features="html.parser")
            token_tag = soup.find(attrs={"name": "token"})
            
            if token_tag is None:
                return "Error: Token Not Found."
            
            token = token_tag.get("value")
        else:
            return f"Error: Status Code {response.status_code} in Step 1."

        # Step 2: Post email to check availability
        params = {'token': token}
        data = {'check_what': 'email', 'email': email}
        response = session.post('https://www.pornhub.com/user/create_account_check', headers=headers, params=params, data=data) 
        
        if response.status_code == 200:
            # Check the JSON response for the 'email taken' message
            if response.json().get("error_message") == "Email has been taken.":
                return True
            return False
        
        return f"Error: Status Code {response.status_code} in Step 2."
    except Exception as e:
        return f"Error: {e}"

def xnxx(email):
    """Checks if the given email is associated with an XNXX account."""
    # Note: Accessing adult content websites programmatically may violate terms of service.
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-en',
            'Host': 'www.xnxx.com',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive'
        }
        
        # Step 1: Get site to establish session/cookies
        cookie_response = session.get('https://www.xnxx.com', headers=headers)

        if cookie_response.status_code != 200:
            return f"Error: Status Code {cookie_response.status_code} in Step 1."

        # Update headers for the AJAX request
        headers['Referer'] = 'https://www.xnxx.com/video-holehe/palenath_fucks_xnxx_with_holehe'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        # URL-encode the email for the query string (requests.get with `params` handles this better)
        # email_url_encoded = email.replace('@', '%40') # Redundant if using params=
        
        # Step 2: Check email availability
        # Using `params` for safer query string construction
        params = {'email': email}
        response = session.get(
            'https://www.xnxx.com/account/checkemail', 
            headers=headers, 
            params=params,
            cookies=cookie_response.cookies
        )
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                # Check for message indicating email is taken
                if response_json.get('message') == "This email is already in use or its owner has excluded it from our website.":
                    return True
                # Check for message indicating invalid email
                elif response_json.get('message') == "Invalid email address.": 
                    return False
                
                # Check for other result indicators (may be site-specific)
                if response_json.get('result') == "false":
                    return True
                elif response_json.get('code') == 1:
                    return True
                elif response_json.get('result') == "true":
                    return False
                elif response_json.get('code') == 0:
                    return False  
                else:
                    return False
            except requests.exceptions.JSONDecodeError:
                # Handle non-JSON response if necessary
                return f"Error: Invalid response format from XNXX."
        
        return f"Error: Status Code {response.status_code} in Step 2."
    except Exception as e:
        return f"Error: {e}"

def xvideo(email):
    """Checks if the given email is associated with an Xvideo account."""
    # Note: Accessing adult content websites programmatically may violate terms of service.
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.xvideos.com/',
        }

        params = {'email': email}
        response = session.get('https://www.xvideos.com/account/checkemail', headers=headers, params=params)
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                # Check for message indicating email is taken
                if response_json.get('message') == "This email is already in use or its owner has excluded it from our website.": 
                    return True
                # Check for message indicating invalid email
                elif response_json.get('message') == "Invalid email address.": 
                    return False
                
                # Check for other result indicators (may be site-specific)
                if response_json.get('result') == "false":
                    return True
                elif response_json.get('code') == 1:
                    return True
                elif response_json.get('result') == "true":
                    return False
                elif response_json.get('code') == 0:
                    return False  
                else:
                    return False
            except requests.exceptions.JSONDecodeError:
                # Handle non-JSON response if necessary
                return f"Error: Invalid response format from Xvideo."

        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

# --- Main Execution Block ---

try:
    # Assuming ChoiceUserAgent is defined and returns a user agent string
    # user_agent = ChoiceUserAgent() 
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36" # Placeholder

    # Slow(osint_banner) # Uncomment if Slow/osint_banner defined
    # print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Selected User-Agent: {white + user_agent}") # Uncomment if formatting vars defined
    print(f"Selected User-Agent: {user_agent}")
    
    # email = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email -> {reset}") # Uncomment if formatting vars defined
    email = input("Enter Email to check -> ")
    
    # Censored(email) # Uncomment if Censored defined
    # print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning..") # Uncomment if formatting vars defined
    print("Scanning...")


    # Use lowercase for function names for Python style convention (PEP 8)
    sites = [
        instagram, twitter, pinterest, imgur, patreon, spotify, firefox, last_pass, archive, pornhub, xnxx, xvideo
    ]
    
    site_founds = []
    found = 0
    not_found = 0
    unknown = 0
    error = 0

    print("\n--- Results ---")
    for site_func in sites:
        site_name = site_func.__name__.replace('_', ' ').title() # Get human-readable name
        result = site_func(email)
        
        if result is True:
            # print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {site_name}: {white}Found") # Uncomment if formatting vars defined
            print(f" {site_name}: Found")
            site_founds.append(site_name)
            found += 1
        elif result is False:
            # print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} {site_name}: {white}Not Found") # Uncomment if formatting vars defined
            print(f" {site_name}: Not Found")
            not_found += 1
        elif isinstance(result, str) and result.startswith("Error:"):
            # print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} {site_name}: {white}Error ({result})") # Uncomment if formatting vars defined
            print(f" {site_name}: Error ({result})")
            error += 1
        else:
            # print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} {site_name}: {white}Unknown Result") # Uncomment if formatting vars defined
            print(f" {site_name}: Unknown Result")
            unknown += 1

    print("\n--- Summary ---")
    if found:
        # print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Total Found ({white + str(found) + red}): {white}" + ", ".join(site_founds)) # Uncomment if formatting vars defined
        print(f"Total Found ({found}): {', '.join(site_founds)}")
    # print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Not Found: {white + str(not_found) + red} Unknown: {white + str(unknown) + red} Error: {white + str(error) + red}") # Uncomment if formatting vars defined
    print(f"Not Found: {not_found}, Unknown: {unknown}, Error: {error}")
    
    # Continue() # Uncomment if Continue defined
    # Reset() # Uncomment if Reset defined
    
except Exception as e:
    # Error(e) # Uncomment if Error defined
    print(f"An unexpected error occurred in the main process: {e}")