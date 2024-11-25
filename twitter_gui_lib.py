import customtkinter as ctk
import tweepy
from tkinter import messagebox

# Library for extended Twitter GUI functionality
class TwitterGUI:
    def __init__(self, root, api):
        self.root = root
        self.api = api
        self.create_menu()
        self.create_tabs()

    def create_menu(self):
        # Menu bar
        menu_frame = ctk.CTkFrame(self.root, height=50, corner_radius=0)
        menu_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(menu_frame, text="Twitter GUI", font=("Arial", 18)).pack(side="left", padx=20)
        ctk.CTkButton(menu_frame, text="Update Profile", command=self.update_profile_window).pack(side="right", padx=10)

    def create_tabs(self):
        # Tabs area
        self.tabview = ctk.CTkTabview(self.root, width=500, height=500)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Tabs: Tweet, Mentions, Direct Messages
        self.tweet_tab = self.tabview.add("Compose Tweet")
        self.mentions_tab = self.tabview.add("Mentions")
        self.dms_tab = self.tabview.add("Direct Messages")

        self.setup_tweet_tab()
        self.setup_mentions_tab()
        self.setup_dms_tab()

    def setup_tweet_tab(self):
        ctk.CTkLabel(self.tweet_tab, text="Compose Tweet:").pack(pady=10)
        self.tweet_entry = ctk.CTkEntry(self.tweet_tab, width=400)
        self.tweet_entry.pack(pady=5)
        ctk.CTkButton(self.tweet_tab, text="Send Tweet", command=self.send_tweet).pack(pady=10)

    def setup_mentions_tab(self):
        ctk.CTkLabel(self.mentions_tab, text="Mentions:").pack(pady=10)
        self.mentions_textbox = ctk.CTkTextbox(self.mentions_tab, width=450, height=300, state="disabled")
        self.mentions_textbox.pack(pady=10)
        ctk.CTkButton(self.mentions_tab, text="Fetch Mentions", command=self.fetch_mentions).pack(pady=10)

    def setup_dms_tab(self):
        ctk.CTkLabel(self.dms_tab, text="Direct Messages:").pack(pady=10)
        self.dms_textbox = ctk.CTkTextbox(self.dms_tab, width=450, height=300, state="disabled")
        self.dms_textbox.pack(pady=10)
        ctk.CTkButton(self.dms_tab, text="Fetch DMs", command=self.fetch_dms).pack(pady=10)

    def send_tweet(self):
        tweet = self.tweet_entry.get()
        if not tweet.strip():
            messagebox.showerror("Error", "Tweet cannot be empty!")
            return
        try:
            self.api.update_status(tweet)
            messagebox.showinfo("Success", "Tweet sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_mentions(self):
        try:
            mentions = self.api.mentions_timeline(count=10)
            mentions_text = "\n".join([f"{m.user.screen_name}: {m.text}" for m in mentions])
            self.mentions_textbox.configure(state="normal")
            self.mentions_textbox.delete("1.0", "end")
            self.mentions_textbox.insert("end", mentions_text or "No mentions found.")
            self.mentions_textbox.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_dms(self):
        try:
            dms = self.api.get_direct_messages(count=10)
            dms_text = "\n".join([f"{dm.message_create['sender_id']}: {dm.message_create['message_data']['text']}" for dm in dms])
            self.dms_textbox.configure(state="normal")
            self.dms_textbox.delete("1.0", "end")
            self.dms_textbox.insert("end", dms_text or "No DMs found.")
            self.dms_textbox.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_profile_window(self):
        def save_profile():
            name = name_entry.get()
            bio = bio_entry.get()
            try:
                self.api.update_profile(name=name, description=bio)
                messagebox.showinfo("Success", "Profile updated successfully!")
                profile_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        profile_win = ctk.CTkToplevel(self.root)
        profile_win.title("Update Profile")

        ctk.CTkLabel(profile_win, text="Name:").pack(pady=5)
        name_entry = ctk.CTkEntry(profile_win, width=300)
        name_entry.pack(pady=5)

        ctk.CTkLabel(profile_win, text="Bio:").pack(pady=5)
        bio_entry = ctk.CTkEntry(profile_win, width=300)
        bio_entry.pack(pady=5)

        ctk.CTkButton(profile_win, text="Save", command=save_profile).pack(pady=10)
