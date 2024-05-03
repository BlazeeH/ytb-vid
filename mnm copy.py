import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re


def search_video_info(entry,i):
    

    url = entry.get()
    try:
        yt = YouTube(url)
        
        # Update video thumbnail
        response = requests.get(yt.thumbnail_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((200, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        video_image.config(image=img)
        video_image.image = img
        
        # Update video information
        global youtube_title
        video_info.config(text=f"Title: {yt.title}\nDuration: {yt.length // 60}:{yt.length % 60:02d}\nViews: {yt.views}")
        youtube_title = yt.title
        res = [stream.resolution for stream in yt.streams.filter(progressive=True).order_by('resolution')]
        # res_combobox['values'] = res
        # res_combobox.current(0)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to search video information: {e}")

# def download_selected():
#     try:        
#         selected_index = res_combobox.current()        
#         if selected_index != -1:
#             url = url_entry.get()
#             yt = YouTube(url)
#             stream = yt.streams.filter(progressive=True).order_by('resolution')[selected_index]
#             save_path = save_path_entry.get()
#             if save_path:
#                 global selected_file_path
#                 if selected_file_path:
#                     stream.download(output_path=os.path.dirname(selected_file_path), filename=os.path.basename(selected_file_path))
#                     messagebox.showinfo("Success", "Video downloaded successfully.")
#                 else:
#                     messagebox.showwarning("Warning", "Please choose a file path.")    
#             else:
#                 messagebox.showwarning("Warning", "Please choose a save path.")
#         else:
#             messagebox.showwarning("Warning", "Please enter YouTube URL to download.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to download video: {e}")

# def choose_save_path():
#     global selected_file_path
#     global youtube_title
#     resolution = res_combobox.get()
#     youtube_title = transform_youtube_title(youtube_title)
#     file_name = youtube_title + "_"+ resolution
#     selected_file_path = filedialog.asksaveasfilename(defaultextension='.mp4',
#                                                       filetypes=[(".mp4", ".mp4"), ("All files", ".*")],
#                                                       initialfile=f"{file_name}.mp4")
#     if selected_file_path:
#         save_path_entry.delete(0, tk.END)
#         save_path_entry.insert(0, selected_file_path)

def transform_youtube_title(title):
    # Xóa các ký tự không hợp lệ trong tên file và thư mục trên Windows
    title = re.sub(r'[\/:*?"<>|]', '', title)
    
    # Thay thế dấu khoảng trắng và dấu chấm cuối bằng dấu gạch dưới
    title = title.strip().replace(' ', '_').rstrip('.')
    
    return title

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("800x520")

# Tạo thanh cuộn dọc
scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side="right", fill="y")

# Tạo một khu vực có thể cuộn
canvas = tk.Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

# Thiết lập thanh cuộn để lắng nghe sự kiện di chuyển của khu vực có thể cuộn
scrollbar.config(command=canvas.yview)

# Tạo một frame mới để chứa tất cả nội dung
content_frame = tk.Frame(canvas)
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Thêm frame chứa nội dung vào khu vực có thể cuộn
canvas.create_window((0, 0), window=content_frame, anchor="nw")

def create_URL_Entry(num):
    for i in range(num):
        # Video Information Frame
        video_image = tk.Label(content_frame)
        video_image.grid(row=i+1, column=0, padx=(10, 5), pady=(20, 0))

        video_info = tk.Label(content_frame, text="", font=("Arial", 12))
        video_info.grid(row=i+1, column=2)

        url_label = tk.Label(content_frame, text="Enter YouTube URL:", font=("Arial", 12))
        url_label.grid(row=i, column=0, padx=(10, 5), pady=(20, 0))
        url_entry = tk.Entry(content_frame, width=40, font=("Arial", 12))
        url_entry.grid(row=i, column=1, padx=(5, 10), pady=(20, 0))
        search_button = tk.Button(content_frame, text="Search Video", command=lambda entry=url_entry : search_video_info(entry,i), font=("Arial", 12))
        search_button.grid(row=i, column=2, padx=(0, 10), pady=(20, 0))

        

create_URL_Entry(15)  # Thử nghiệm với số lượng entry nhiều hơn để thấy thanh cuộn hoạt động




# # Resolution Combobox Frame
# res_frame = tk.Frame(root)
# res_frame.pack(pady=(10, 0))
# resolution_label = tk.Label(res_frame, text="Select Resolution:", font=("Arial", 12))
# resolution_label.grid(row=0, column=0, padx=(10, 5))
# res_combobox = ttk.Combobox(res_frame, width=10, state="readonly", font=("Arial", 12))
# res_combobox.grid(row=0, column=1, padx=(5, 10))

# save_path_frame = tk.Frame(root)
# save_path_frame.pack(pady=(10, 0))

# save_path_label = tk.Label(save_path_frame, text="Save to:", font=("Arial", 12))
# save_path_label.grid(row=0, column=0, padx=(10, 5))

# save_path_entry = tk.Entry(save_path_frame, width=40, font=("Arial", 12))
# save_path_entry.grid(row=0, column=1, padx=(5, 10))

# browse_button = tk.Button(save_path_frame, text="Browse", command=choose_save_path, font=("Arial", 12))
# browse_button.grid(row=0, column=2, padx=(0, 10))
# # Download Button
# download_button = tk.Button(root, text="Download Selected", command=download_selected, font=("Arial", 12))
# download_button.pack(pady=(20, 10))

# File name to save
selected_file_path = ""
youtube_title =" "

root.mainloop()
