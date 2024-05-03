import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re

# Xử lý sự kiện tìm kiếm video
def search_video_info():
    url = url_entry.get()
    try:
        yt = YouTube(url)
        
        # Update video thumbnail
        response = requests.get(yt.thumbnail_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        video_image.config(image=img)
        video_image.image = img
        
        # Update video information
        global youtube_title
        video_info.config(text=f"Title: {yt.title}")
        video_duration.config(text=f"Duration: {yt.length // 60}:{yt.length % 60:02d}  \nViews: {yt.views}")
        youtube_title = yt.title
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
            save_path = save_path_entry.get()
            if save_path:
                global selected_file_path
                if selected_file_path:
                    stream.download(output_path=os.path.dirname(selected_file_path), filename=os.path.basename(selected_file_path))
                    messagebox.showinfo("Success", "Video downloaded successfully.")
                else:
                    messagebox.showwarning("Warning", "Please choose a file path.")    
            else:
                messagebox.showwarning("Warning", "Please choose a save path.")
        else:
            messagebox.showwarning("Warning", "Please enter YouTube URL to download.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

def choose_save_path():
    global selected_file_path
    global youtube_title
    resolution = res_combobox.get()
    youtube_title = transform_youtube_title(youtube_title)
    file_name = youtube_title + "_"+ resolution
    selected_file_path = filedialog.asksaveasfilename(defaultextension='.mp4',
                                                      filetypes=[(".mp4", ".mp4"), ("All files", ".*")],
                                                      initialfile=f"{file_name}.mp4")
    if selected_file_path:
        save_path_entry.delete(0, tk.END)
        save_path_entry.insert(0, selected_file_path)

def transform_youtube_title(title):
    # Xóa các ký tự không hợp lệ trong tên file và thư mục trên Windows
    title = re.sub(r'[\/:*?"<>|]', '', title)
    
    # Thay thế dấu khoảng trắng và dấu chấm cuối bằng dấu gạch dưới
    title = title.strip().replace(' ', '_').rstrip('.')
    
    return title

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

video_image = tk.Label(video_frame,bg="lightblue")
video_image.pack()

video_info = tk.Label(video_frame, text="", font=("Arial", 12),anchor="w")
video_info.pack()

video_duration = tk.Label(video_frame, text="", font=("Arial", 12),anchor="w")
video_duration.pack()

# Resolution Combobox Frame
res_frame = tk.Frame(root)
res_frame.pack(pady=(10, 0))
resolution_label = tk.Label(res_frame, text="Select Resolution:", font=("Arial", 12))
resolution_label.grid(row=0, column=0, padx=(10, 5))
res_combobox = ttk.Combobox(res_frame, width=10, state="readonly", font=("Arial", 12))
res_combobox.grid(row=0, column=1, padx=(5, 10))

save_path_frame = tk.Frame(root)
save_path_frame.pack(pady=(10, 0))

save_path_label = tk.Label(save_path_frame, text="Save to:", font=("Arial", 12))
save_path_label.grid(row=0, column=0, padx=(10, 5))

save_path_entry = tk.Entry(save_path_frame, width=40, font=("Arial", 12))
save_path_entry.grid(row=0, column=1, padx=(5, 10))

browse_button = tk.Button(save_path_frame, text="Browse", command=choose_save_path, font=("Arial", 12))
browse_button.grid(row=0, column=2, padx=(0, 10))
# Download Button
download_button = tk.Button(root, text="Download Selected", command=download_selected, font=("Arial", 12))
download_button.pack(pady=(20, 10))

# File name to save
selected_file_path = ""
youtube_title =" "

root.mainloop()
