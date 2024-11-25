import tkinter as tk
import customtkinter as ctk
import tweepy
from twitter_gui_lib import TwitterGUI
from profile_manager import ProfileManager
from tweet_scheduler import TweetScheduler
from notification_handler import NotificationHandler

# Authentication setup
def authenticate():
    API_KEY = "your_api_key"
    API_SECRET_KEY = "your_api_secret_key"
    ACCESS_TOKEN = "your_access_token"
    ACCESS_TOKEN_SECRET = "your_access_token_secret"

    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

# Callback functions for notifications
def handle_new_mentions(mentions):
    for mention in mentions:
        messagebox.showinfo("New Mention", f"{mention.user.screen_name}: {mention.text}")

def handle_new_dms(dms):
    for dm in dms:
        messagebox.showinfo("New DM", f"{dm.message_create['sender_id']}: {dm.message_create['message_data']['text']}")

# Initialize GUI
ctk.set_appearance_mode("Dark")
root = ctk.CTk()
root.title("Twitter GUI")

# Authenticate and set up components
api = authenticate()
twitter_gui = TwitterGUI(root, api)

# Add Profile Manager
profile_manager = ProfileManager(api)
twitter_gui.create_menu()
ctk.CTkButton(root, text="Update Profile", command=lambda: profile_manager.open_profile_window(root)).pack()

# Add Tweet Scheduler
scheduler = TweetScheduler(api)
ctk.CTkButton(root, text="Schedule Tweet", command=lambda: scheduler.open_scheduler_window(root)).pack()

# Add Notification Handler
notifications = NotificationHandler(api)
notifications.start_polling(handle_new_mentions, handle_new_dms)

# Start GUI
root.mainloop()
