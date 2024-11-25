import customtkinter as ctk
from twitter_gui import TwitterGUI
from twitter_backend import TwitterBackend


class TwitterLoginGUI:
    def __init__(self, root):
        self.root = root
        self.backend = None

        # Root Window Setup
        self.root.title("Twitter Login")
        self.root.geometry("400x500")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Login UI
        self.create_login_screen()

    def create_login_screen(self):
        """Creates the login UI for entering Twitter API credentials."""
        login_frame = ctk.CTkFrame(self.root, corner_radius=10)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            login_frame, text="Twitter Login", font=("Arial", 24, "bold"), anchor="center"
        ).pack(pady=20)

        # Input Fields
        self.api_key_entry = self.create_input_field(login_frame, "API Key")
        self.api_secret_entry = self.create_input_field(login_frame, "API Secret")
        self.access_token_entry = self.create_input_field(login_frame, "Access Token")
        self.access_token_secret_entry = self.create_input_field(login_frame, "Access Token Secret")

        # Login Button
        ctk.CTkButton(
            login_frame, text="Login", command=self.handle_login, fg_color="#1DA1F2"
        ).pack(pady=20)

        # Status Label
        self.status_label = ctk.CTkLabel(login_frame, text="", text_color="red", anchor="center")
        self.status_label.pack(pady=10)

    def create_input_field(self, parent, placeholder):
        """Creates a labeled input field."""
        ctk.CTkLabel(parent, text=placeholder).pack(pady=(10, 0))
        entry = ctk.CTkEntry(parent, width=300)
        entry.pack(pady=5)
        return entry

    def handle_login(self):
        """Handle login logic and transition to the main application."""
        # Get API Credentials
        api_key = self.api_key_entry.get()
        api_secret = self.api_secret_entry.get()
        access_token = self.access_token_entry.get()
        access_token_secret = self.access_token_secret_entry.get()

        # Validate Inputs
        if not all([api_key, api_secret, access_token, access_token_secret]):
            self.status_label.configure(text="All fields are required!", text_color="red")
            return

        try:
            # Initialize Backend
            self.backend = TwitterBackend(api_key, api_secret, access_token, access_token_secret)
            self.status_label.configure(text="Login successful!", text_color="green")

            # Transition to Main GUI
            self.load_main_gui()
        except Exception as e:
            self.status_label.configure(text=f"Login failed: {str(e)}", text_color="red")

    def load_main_gui(self):
        """Destroys the login screen and loads the main Twitter GUI."""
        self.root.destroy()
        main_root = ctk.CTk()
        TwitterGUI(main_root, self.backend)
        main_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    TwitterLoginGUI(root)
    root.mainloop()
