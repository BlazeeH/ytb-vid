import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO

def search_video_info():
    url = url_entry.get()
    try:
        yt = YouTube(url)
        
        # Update video thumbnail
        response = requests.get(yt.thumbnail_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((340, 200), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        video_image.config(image=img)
        video_image.image = img
        
        # Update video information
        video_info.config(text=f"Title: {yt.title}\nDuration: {yt.length // 60}:{yt.length % 60:02d}\nViews: {yt.views}")
        
        res = [stream.resolution for stream in yt.streams.filter(progressive=True).order_by('resolution')]
        res_combobox['values'] = res
        res_combobox.current(0)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to search video information: {e}")

def download_selected():
    try:
        selected_index = res_combobox.current()
        if selected_index != -1:
            url = url_entry.get()
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True).order_by('resolution')[selected_index]
            stream.download()
            messagebox.showinfo("Success", "Video downloaded successfully.")
        else:
            messagebox.showwarning("Warning", "Please enter YouTube URL to download.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("700x520")

# URL Entry Frame
url_frame = tk.Frame(root)
url_frame.pack(pady=(20, 0))

url_label = tk.Label(url_frame, text="Enter YouTube URL:", font=("Arial", 12))
url_label.grid(row=0, column=0, padx=(10, 5))
url_entry = tk.Entry(url_frame, width=40, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=(5, 10))
search_button = tk.Button(url_frame, text="Search Video", command=search_video_info, font=("Arial", 12))
search_button.grid(row=0, column=2, padx=(0, 10))

# Video Information Frame
video_frame = tk.Frame(root)
video_frame.pack(pady=(10, 0))

video_image = tk.Label(video_frame)
video_image.pack()

video_info = tk.Label(video_frame, text="", font=("Arial", 12))
video_info.pack()

# Resolution Combobox Frame
res_frame = tk.Frame(root)
res_frame.pack(pady=(10, 0))
resolution_label = tk.Label(res_frame, text="Select Resolution:", font=("Arial", 12))
resolution_label.grid(row=0, column=0, padx=(10, 5))
res_combobox = ttk.Combobox(res_frame, width=10, state="readonly", font=("Arial", 12))
res_combobox.grid(row=0, column=1, padx=(5, 10))

# Download Button
# Download Button
download_button = tk.Button(root, text="Download Selected", command=download_selected, font=("Arial", 12))
download_button.pack(pady=(20, 10))


root.mainloop()
