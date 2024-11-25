from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
from threading import Timer

class TweetScheduler:
    def __init__(self, api):
        self.api = api

    def open_scheduler_window(self, root):
        def schedule_tweet():
            tweet = tweet_entry.get()
            delay = int(delay_entry.get())
            if not tweet.strip():
                messagebox.showerror("Error", "Tweet cannot be empty!")
                return

            def send():
                try:
                    self.api.update_status(tweet)
                    messagebox.showinfo("Success", "Scheduled tweet sent successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            Timer(delay, send).start()
            scheduler_win.destroy()
            messagebox.showinfo("Scheduled", f"Tweet will be sent in {delay} seconds.")

        scheduler_win = ctk.CTkToplevel(root)
        scheduler_win.title("Schedule Tweet")

        ctk.CTkLabel(scheduler_win, text="Tweet Content:").pack(pady=5)
        tweet_entry = ctk.CTkEntry(scheduler_win, width=300)
        tweet_entry.pack(pady=5)

        ctk.CTkLabel(scheduler_win, text="Delay (seconds):").pack(pady=5)
        delay_entry = ctk.CTkEntry(scheduler_win, width=100)
        delay_entry.pack(pady=5)

        ctk.CTkButton(scheduler_win, text="Schedule Tweet", command=schedule_tweet).pack(pady=10)
