import instaloader
import sys
import os
import contextlib

# Assuming 'ErrorModule', 'Title', 'Slow', 'osint_banner', 'BEFORE', 'current_time_hour', 
# 'AFTER', 'INPUT', 'reset', 'ERROR', 'Continue', 'Reset', 'white', 'INFO_ADD', and 'Error' 
# are custom functions/variables from an external library, they are kept as-is 
# for functional consistency, but their names are noted for potential revision.

try:
    # --- Import Handling ---
    import instaloader
    import sys
    import os
    import contextlib
except Exception as e:
    # ErrorModule(e) # Uncomment if ErrorModule is defined
    pass
    
# Title("Instagram Account") # Uncomment if Title is defined

try:
    # --- Function to Search and Get Profile ---
    def search_profile(username):
        """
        Retrieves the Instaloader object and the Profile object for the given username.
        Uses a context manager to temporarily suppress stdout/stderr output from Instaloader.
        """
        @contextlib.contextmanager
        def suppress_output():
            """Temporarily suppresses stdout and stderr."""
            with open(os.devnull, 'w') as devnull:
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = devnull
                sys.stderr = devnull
                try:
                    yield
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

        with suppress_output():
            loader = instaloader.Instaloader()
            # loader.compress_json = False # Optional: to avoid compression if needed
            profile = instaloader.Profile.from_username(loader.context, username)
            
        return loader, profile

    # Assuming 'Slow(osint_banner)' is a function to display a banner slowly.
    # Slow(osint_banner) 
    
    # Using placeholders for custom variables/functions
    BEFORE = ""
    current_time_hour = lambda: "HH:MM:SS"
    AFTER = ""
    INPUT = "[?]"
    reset = ""
    ERROR = "[!]"
    INFO_ADD = "[+]"
    white = ""

    username = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Instagram Username -> {reset}")

    try:
        loader, profile = search_profile(username)
    except Exception: # Catch specific exceptions if possible (e.g., ProfileNotExistsException)
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} You have exceeded your limit or the user does not exist, try again in a few minutes.")
        # Continue() # Uncomment if Continue is defined
        # Reset() # Uncomment if Reset is defined
        sys.exit(1) # Exit if search fails
        
    # --- Display Profile Information ---
    # Slow() is likely used to print the information slowly.
    # Slow(f"""...""") 
    print(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  {INFO_ADD} Full Name       : {white}{profile.full_name}
  {INFO_ADD} Username        : {white}{profile.username}
  {INFO_ADD} Instagram ID    : {white}{profile.userid}
  {INFO_ADD} Biography       : {white}{profile.biography}
  {INFO_ADD} Profile URL     : {white}https://instagram.com/{profile.username}
  {INFO_ADD} Profile Photo   : {white}{profile.profile_pic_url}
  {INFO_ADD} Posts           : {white}{profile.mediacount}
  {INFO_ADD} Followers       : {white}{profile.followers}
  {INFO_ADD} Following       : {white}{profile.followees}
  {INFO_ADD} Verified        : {white}{'True' if profile.is_verified else 'False'}
  {INFO_ADD} Private Account : {white}{'True' if profile.is_private else 'False'}
  {INFO_ADD} Professional    : {white}{'True' if profile.is_business_account else 'False'}""")

    if profile.is_business_account:
        # 'Category Pro' is translated to 'Business Category' or 'Professional Category'
        print(f"    {INFO_ADD} Business Category : {white}{profile.business_category_name}")

    print(f"{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
    
    # --- Display Latest Posts (limited to 5) ---
    # Check if the account is not private or if the user is logged in as the profile owner
    if not profile.is_private: # Removed 'or loader.context.username == profile.username' unless login is implemented
        try:
            posts = profile.get_posts()
            print(f"\n{white}--- Latest Posts (Up to 5) ---")
            for i, post in enumerate(posts):
                # Slow() is likely used to print the information slowly.
                # Slow(f"""...""")
                print(f"""  
  {INFO_ADD} Post N°{i+1}
  {INFO_ADD} URL         : {white}https://www.instagram.com/p/{post.shortcode}/
  {INFO_ADD} Date        : {white}{post.date}
  {INFO_ADD} Likes       : {white}{post.likes}
  {INFO_ADD} Comments    : {white}{post.comments}
  {INFO_ADD} Caption     : {white}{post.caption.replace('\n', ' ')[:100] + '...' if post.caption else 'No Caption'} # Truncate long captions
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────""")
                if i == 4: # Limit to 5 posts (0 to 4)
                    break
            print()
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error retrieving posts: {e}")
    else:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO_ADD} Cannot retrieve posts: Account is private.")
        
    # Continue() # Uncomment if Continue is defined
    # Reset() # Uncomment if Reset is defined

except Exception as e:
    # Error(e) # Uncomment if Error is defined
    print(f"An unexpected error occurred: {e}")