import customtkinter as ctk
from tkinter import filedialog, messagebox

class ProfileManager:
    def __init__(self, api):
        self.api = api

    def open_profile_window(self, root):
        def save_profile():
            name = name_entry.get()
            bio = bio_entry.get()
            try:
                self.api.update_profile(name=name, description=bio)
                messagebox.showinfo("Success", "Profile updated successfully!")
                profile_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def update_profile_image():
            image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
            if image_path:
                try:
                    self.api.update_profile_image(image_path)
                    messagebox.showinfo("Success", "Profile image updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        profile_win = ctk.CTkToplevel(root)
        profile_win.title("Update Profile")

        ctk.CTkLabel(profile_win, text="Name:").pack(pady=5)
        name_entry = ctk.CTkEntry(profile_win, width=300)
        name_entry.pack(pady=5)

        ctk.CTkLabel(profile_win, text="Bio:").pack(pady=5)
        bio_entry = ctk.CTkEntry(profile_win, width=300)
        bio_entry.pack(pady=5)

        ctk.CTkButton(profile_win, text="Update Profile Image", command=update_profile_image).pack(pady=10)
        ctk.CTkButton(profile_win, text="Save Profile", command=save_profile).pack(pady=10)
