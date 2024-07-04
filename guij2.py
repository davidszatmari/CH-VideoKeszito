import customtkinter as ctk
from tkinter import filedialog, messagebox
import shutil
import os
import threading
from createmp4 import create_slideshow
import sys
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def select_images():
    files = filedialog.askopenfilenames(title="Select Images",
                                        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if files:
        global selected_files
        selected_files = files
        image_count_label.configure(text=f"{len(files)} kiválasztott kép")
        image_list.configure(state="normal")
        image_list.delete("1.0", ctk.END)
        for file in files:
            image_list.insert(ctk.END, file + '\n')
        image_list.configure(state="disabled")

def copy_images():
    image_folder = resource_path('user_images')
    
    # Clear the 'user_images' folder
    try:
        if os.path.exists(image_folder):
            shutil.rmtree(image_folder)
        os.makedirs(image_folder)
    except OSError as e:
        messagebox.showerror("Error", f"Error accessing {image_folder}: {e.strerror}")
        return

    if not selected_files:
        messagebox.showwarning("No Images Selected", "Please select images to copy")
        return

    progress_bar.set(0)
    progress_bar.pack(pady=5)
    app.update()

    total_files = len(selected_files)
    for index, image in enumerate(selected_files):
        try:
            shutil.copy(image, image_folder)
        except Exception as e:
            messagebox.showerror("Error Copying File", f"Error copying {image}: {e}")
            progress_bar.pack_forget()
            return
        progress_bar.set((index + 1) / total_files)
        app.update()

    image_list.configure(state="normal")
    image_list.delete("1.0", ctk.END)
    image_list.insert(ctk.END, "Video Készítés folyamatban..." + '\n')
    image_list.configure(text_color="green")
    app.update()
    time.sleep(1.5)
    #messagebox.showinfo("Success", "Images copied successfully!")
    image_list.delete("1.0", ctk.END)
    image_list.configure(state="disabled")
    progress_bar.pack_forget()
    image_count_label.configure(text="")

    # Parameters
    output_file = 'video.mp4'
    last_image_folder = resource_path('static_files')
    last_image_file = 'last_image.png'
    background_video = resource_path(os.path.join('static_files', 'background.mp4'))
    duration_per_image = 4  # duration for each image in seconds
    fade_duration = 1.5     # duration of fade-out in seconds
    target_size = (1080, 1920)  # 9:16 aspect ratio (1080x1920 for HD)

    # Start the function in a new thread to prevent freezing the GUI
    slideshow_thread = threading.Thread(target=create_slideshow, args=(image_folder, output_file, last_image_file, last_image_folder, background_video, duration_per_image, fade_duration, target_size))
    slideshow_thread.start()

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "dark-blue", "green"

selected_files = []

app = ctk.CTk()
app.title("Video Készítő")

# Create and place widgets
ctk.CTkLabel(app, text="Kiválasztott képek:").pack(pady=10)

image_list = ctk.CTkTextbox(app, width=500, height=200)
image_list.pack(padx=10, pady=5)
image_list.configure(state="disabled")

image_count_label = ctk.CTkLabel(app, text="")
image_count_label.pack(pady=5)

select_images_btn = ctk.CTkButton(app, text="Képek kiválasztása", command=select_images)
select_images_btn.pack(pady=5)

copy_images_btn = ctk.CTkButton(app, text="Indítás", command=copy_images, width=65)
copy_images_btn.pack(pady=20)

progress_bar = ctk.CTkProgressBar(app, mode='determinate', width=400)
progress_bar.set(0)

# Run the application
app.geometry("600x500")
app.mainloop()
