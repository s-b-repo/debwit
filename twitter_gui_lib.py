import customtkinter as ctk
from tkinter import messagebox
from twitter_backend import TwitterBackend


class TwitterGUI:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend

        self.root.title("Twitter GUI")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_menu()
        self.create_tabs()
        self.create_status_bar()

        self.root.bind("<Configure>", self.on_resize)

    def create_menu(self):
        self.menu_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.menu_frame.pack(fill="x", pady=10, padx=10)

        self.menu_label = ctk.CTkLabel(self.menu_frame, text="Twitter GUI", font=("Arial", 24, "bold"))
        self.menu_label.pack(side="left", padx=20)

        self.update_profile_button = ctk.CTkButton(
            self.menu_frame, text="Update Profile", command=self.update_profile_window, fg_color="#4CAF50"
        )
        self.update_profile_button.pack(side="right", padx=10)

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tweet_tab = self.tabview.add("Compose Tweet")
        self.mentions_tab = self.tabview.add("Mentions")
        self.dms_tab = self.tabview.add("Direct Messages")

        self.setup_tweet_tab()
        self.setup_mentions_tab()
        self.setup_dms_tab()

    def create_status_bar(self):
        self.status_var = ctk.StringVar(value="Welcome to Twitter GUI!")
        self.status_bar = ctk.CTkLabel(self.root, textvariable=self.status_var, font=("Arial", 14), anchor="w")
        self.status_bar.pack(fill="x", pady=(0, 10), padx=10)

    def setup_tweet_tab(self):
        ctk.CTkLabel(self.tweet_tab, text="Compose a Tweet", font=("Arial", 20, "bold")).pack(pady=10)
        self.tweet_entry = ctk.CTkTextbox(self.tweet_tab, height=150)
        self.tweet_entry.pack(fill="x", expand=True, padx=20, pady=10)

        ctk.CTkButton(self.tweet_tab, text="Send Tweet", command=self.send_tweet, fg_color="#1DA1F2").pack(pady=10)

    def setup_mentions_tab(self):
        ctk.CTkLabel(self.mentions_tab, text="Your Mentions", font=("Arial", 20, "bold")).pack(pady=10)
        self.mentions_textbox = ctk.CTkTextbox(self.mentions_tab, state="disabled")
        self.mentions_textbox.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkButton(self.mentions_tab, text="Fetch Mentions", command=self.fetch_mentions, fg_color="#1DA1F2").pack(
            pady=10
        )

    def setup_dms_tab(self):
        ctk.CTkLabel(self.dms_tab, text="Your Direct Messages", font=("Arial", 20, "bold")).pack(pady=10)
        self.dms_textbox = ctk.CTkTextbox(self.dms_tab, state="disabled")
        self.dms_textbox.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkButton(self.dms_tab, text="Fetch DMs", command=self.fetch_dms, fg_color="#1DA1F2").pack(pady=10)

    def send_tweet(self):
        tweet = self.tweet_entry.get("1.0", "end").strip()
        if not tweet:
            self.update_status("Tweet cannot be empty!", error=True)
            return
        try:
            self.backend.send_tweet(tweet)
            self.update_status("Tweet sent successfully!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)

    def fetch_mentions(self):
        try:
            mentions = self.backend.get_mentions()
            mentions_text = "\n\n".join([f"@{m.user.screen_name}: {m.text}" for m in mentions])
            self.mentions_textbox.configure(state="normal")
            self.mentions_textbox.delete("1.0", "end")
            self.mentions_textbox.insert("end", mentions_text or "No mentions found.")
            self.mentions_textbox.configure(state="disabled")
            self.update_status("Mentions fetched successfully!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)

    def fetch_dms(self):
        try:
            dms = self.backend.get_direct_messages()
            dms_text = "\n\n".join([f"{dm.message_create['sender_id']}: {dm.message_create['message_data']['text']}" for dm in dms])
            self.dms_textbox.configure(state="normal")
            self.dms_textbox.delete("1.0", "end")
            self.dms_textbox.insert("end", dms_text or "No DMs found.")
            self.dms_textbox.configure(state="disabled")
            self.update_status("DMs fetched successfully!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)

    def update_status(self, message, error=False):
        self.status_var.set(message)
        self.status_bar.configure(fg_color="#FF6347" if error else "#4CAF50")

    def update_profile_window(self):
        profile_win = ctk.CTkToplevel(self.root)
        profile_win.title("Update Profile")
        profile_win.geometry("400x300")

        ctk.CTkLabel(profile_win, text="Update Profile", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(profile_win, text="Name:").pack(pady=5)
        name_entry = ctk.CTkEntry(profile_win, width=300)
        name_entry.pack(pady=5)
        ctk.CTkLabel(profile_win, text="Bio:").pack(pady=5)
        bio_entry = ctk.CTkTextbox(profile_win, width=300, height=100)
        bio_entry.pack(pady=5)
        ctk.CTkButton(profile_win, text="Save", command=lambda: self.save_profile(name_entry, bio_entry), fg_color="#4CAF50").pack(pady=10)

    def save_profile(self, name_entry, bio_entry):
        try:
            self.backend.update_profile(name=name_entry.get(), bio=bio_entry.get("1.0", "end").strip())
            self.update_status("Profile updated successfully!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
