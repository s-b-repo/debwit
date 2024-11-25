import tkinter as tk
from tkinter import messagebox
import tweepy
import json
import os

CONFIG_FILE = "config.json"

# Load API credentials
def load_credentials():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

# Save API credentials
def save_credentials(api_key, api_secret_key, access_token, access_token_secret):
    credentials = {
        "api_key": api_key,
        "api_secret_key": api_secret_key,
        "access_token": access_token,
        "access_token_secret": access_token_secret,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(credentials, f)

# Authenticate with Twitter API
def authenticate():
    credentials = load_credentials()
    if not credentials:
        messagebox.showinfo("Info", "Please enter your Twitter API credentials.")
        credentials_window()
        return None

    try:
        auth = tweepy.OAuth1UserHandler(
            credentials["api_key"],
            credentials["api_secret_key"],
            credentials["access_token"],
            credentials["access_token_secret"],
        )
        api = tweepy.API(auth)
        api.verify_credentials()  # Verify credentials are valid
        return api
    except Exception as e:
        messagebox.showerror("Error", f"Authentication failed: {e}")
        return None

# GUI to collect API credentials
def credentials_window():
    def save_and_close():
        api_key = api_key_entry.get()
        api_secret_key = api_secret_key_entry.get()
        access_token = access_token_entry.get()
        access_token_secret = access_token_secret_entry.get()

        if not (api_key and api_secret_key and access_token and access_token_secret):
            messagebox.showerror("Error", "All fields are required!")
            return

        save_credentials(api_key, api_secret_key, access_token, access_token_secret)
        credentials_win.destroy()

    credentials_win = tk.Toplevel(root)
    credentials_win.title("Enter Twitter API Credentials")
    credentials_win.geometry("400x300")

    tk.Label(credentials_win, text="API Key:").pack(pady=5)
    api_key_entry = tk.Entry(credentials_win, width=40)
    api_key_entry.pack()

    tk.Label(credentials_win, text="API Secret Key:").pack(pady=5)
    api_secret_key_entry = tk.Entry(credentials_win, width=40)
    api_secret_key_entry.pack()

    tk.Label(credentials_win, text="Access Token:").pack(pady=5)
    access_token_entry = tk.Entry(credentials_win, width=40)
    access_token_entry.pack()

    tk.Label(credentials_win, text="Access Token Secret:").pack(pady=5)
    access_token_secret_entry = tk.Entry(credentials_win, width=40)
    access_token_secret_entry.pack()

    tk.Button(credentials_win, text="Save", command=save_and_close).pack(pady=20)

# Send a Tweet
def send_tweet():
    tweet = tweet_entry.get()
    if not tweet.strip():
        messagebox.showerror("Error", "Tweet cannot be empty!")
        return

    try:
        api.update_status(tweet)
        messagebox.showinfo("Success", "Tweet sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fetch mentions
def fetch_mentions():
    try:
        mentions = api.mentions_timeline(count=10)
        mentions_text = "\n".join([f"{m.user.screen_name}: {m.text}" for m in mentions])
        mentions_textbox.config(state=tk.NORMAL)
        mentions_textbox.delete(1.0, tk.END)
        mentions_textbox.insert(tk.END, mentions_text or "No mentions found.")
        mentions_textbox.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fetch DMs
def fetch_dms():
    try:
        dms = api.get_direct_messages(count=10)
        dms_text = "\n".join([f"{dm.message_create['sender_id']}: {dm.message_create['message_data']['text']}" for dm in dms])
        dms_textbox.config(state=tk.NORMAL)
        dms_textbox.delete(1.0, tk.END)
        dms_textbox.insert(tk.END, dms_text or "No DMs found.")
        dms_textbox.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Twitter GUI")

# Load credentials and authenticate
api = authenticate()
if not api:
    root.destroy()

# Tweet section
tk.Label(root, text="Compose Tweet:").pack(pady=5)
tweet_entry = tk.Entry(root, width=50)
tweet_entry.pack(pady=5)
tk.Button(root, text="Send Tweet", command=send_tweet).pack(pady=5)

# Mentions section
tk.Label(root, text="Mentions:").pack(pady=5)
mentions_textbox = tk.Text(root, width=60, height=10, state=tk.DISABLED)
mentions_textbox.pack(pady=5)
tk.Button(root, text="Fetch Mentions", command=fetch_mentions).pack(pady=5)

# DMs section
tk.Label(root, text="Direct Messages:").pack(pady=5)
dms_textbox = tk.Text(root, width=60, height=10, state=tk.DISABLED)
dms_textbox.pack(pady=5)
tk.Button(root, text="Fetch DMs", command=fetch_dms).pack(pady=5)

# Start the application
root.mainloop()
