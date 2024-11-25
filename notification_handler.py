import threading
import time
from tkinter import messagebox

class NotificationHandler:
    def __init__(self, api):
        self.api = api
        self.running = False

    def start_polling(self, callback_mentions, callback_dms):
        self.running = True

        def poll():
            last_mention_id = None
            last_dm_id = None
            while self.running:
                try:
                    mentions = self.api.mentions_timeline(since_id=last_mention_id)
                    if mentions:
                        last_mention_id = mentions[0].id
                        callback_mentions(mentions)

                    dms = self.api.get_direct_messages()
                    if dms:
                        last_dm_id = dms[0].id
                        callback_dms(dms)
                except Exception as e:
                    print(f"Notification error: {e}")
                time.sleep(60)

        threading.Thread(target=poll, daemon=True).start()

    def stop_polling(self):
        self.running = False
