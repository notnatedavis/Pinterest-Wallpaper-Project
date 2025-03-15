# --- Imports ---#
from utils.logger import logger
import customtkinter as ctk
from tkinter import messagebox
import requests
from urllib.parse import urlparse
import threading

# --- Functions for Main --- #
def open_window():
    def validate_pinterest_url(input_url: str) -> bool:
        # checks if URL is a valid Pinterest board URL
        # normalize URL format
        if not input_url.startswith(('http://', 'https://')):
            input_url = 'https://' + input_url
        
        try:
            parsed = urlparse(input_url)
            # remove www. prefix and validate domain
            normalized_domain = parsed.netloc.lower().replace('www.', '')
            if normalized_domain != 'pinterest.com':
                return False
            
            # validate path structure
            path_parts = [p for p in parsed.path.split('/') if p]
            return len(path_parts) >= 2  # At least username/boardname

        except Exception:
            return False

    def check_url_accessible(url: str) -> bool:
        # verifies URL is accessible and remains on Pinterest
        try:
            # use browser-like headers and full GET request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }

            response = requests.get(
                url, 
                headers=headers,
                allow_redirects=True, 
                timeout=10,
                verify=True  # Keep SSL verification
            )

            # normalize final URL
            final_url = response.url.lower()
            return (
                response.status_code == 200 and 
                'pinterest.com' in final_url and
                ('/board/' in final_url or '/pin/' not in final_url)
            )

        except requests.RequestException as e:
            # logging.debug(f"Access check failed: {str(e)}")
            return False

    def on_submit() :
        nonlocal url
        input_url = entry.get().strip()
        
        if not input_url :
            messagebox.showerror("Error", "Please enter a URL")
            return

        submit_button.configure(state="disabled", text="Validating...")
        
        def validation_thread() :
            # invalid url
            if not validate_pinterest_url(input_url):
                root.after(0, lambda: messagebox.showerror(
                    "Invalid Format", 
                    "Must be a Pinterest board URL format:\n"
                    "e.g. https://www.pinterest.com/username/boardname/"
                ))
            # not accessible
            elif not check_url_accessible(input_url) :
                root.after(0, lambda: messagebox.showerror(
                    "Access Failed",
                    "Could not access this Pinterest board.\n"
                    "1. Check your internet connection\n"
                    "2. Ensure the board is public\n"
                    "3. Could be format"
                ))
            # else valid
            else :
                nonlocal url
                url = input_url
                root.after(0, root.destroy)
            
            root.after(0, lambda: submit_button.configure(
                state="normal", 
                text="Submit"
            ))

        threading.Thread(target=validation_thread, daemon=True).start()

    url = None  # moved before UI setup

    # window setup
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Pinterest Board URL")
    root.geometry("450x200")

    # UI elements
    label = ctk.CTkLabel(root, 
        text="Enter Pinterest Board URL:\n"
             "Ex: https://www.pinterest.com/username/boardname/")
    label.pack(pady=15)

    entry = ctk.CTkEntry(root, width=380)
    entry.pack(pady=10)

    submit_button = ctk.CTkButton(root, text="Submit", command=on_submit)
    submit_button.pack(pady=15)

    root.mainloop()
    return url
