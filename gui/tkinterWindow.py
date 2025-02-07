# --- Imports ---#
import customtkinter as ctk
from tkinter import messagebox

# --- other shit here --- #

# --- Functions for Main --- #
def open_window() :
    # Prompt user to enter pinterest board URL w/ Tkinter GUI

    def on_submit() :
        nonlocal url # nonlocal keyword needed
        url = entry.get().strip()
        if url and url.startswith("https://www.pinterest.com/"):  # Basic validation
            root.destroy()
        else:
            messagebox.showerror("Invalid URL", "Please enter a valid Pinterest board URL.")
    
    # Variable to store the URL
    url = None

    # Set the appearance mode (light/dark)
    ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"

    # Set the default color theme
    ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

    # Create the CustomTkinter window
    root = ctk.CTk()
    root.title("Pinterest Board URL")
    root.geometry("400x150")

    # Add a label
    label = ctk.CTkLabel(root, text="Enter the Pinterest board URL:")
    label.pack(pady=10)

    # Add a text entry box
    entry = ctk.CTkEntry(root, width=300)
    entry.pack(pady=10)

    # Add a submit button
    submit_button = ctk.CTkButton(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    # Run the CustomTkinter event loop
    root.mainloop()

    # Return the URL after the window is closed
    return url
