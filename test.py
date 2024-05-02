import tkinter as tk
from tkinter import ttk

def on_configure(event):
    url_canvas.configure(scrollregion=url_canvas.bbox("all"))

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("700x520")

# Tạo một frame mẹ cho canvas và scrollbar
url_frame = tk.Frame(root)
url_frame.pack(pady=(20, 0))

# Tạo một canvas trong frame để có thể scroll
url_canvas = tk.Canvas(url_frame)
url_canvas.pack(side="left", fill="both", expand=True)

# Tạo một scrollbar dọc
scrollbar = ttk.Scrollbar(url_frame, orient="vertical", command=url_canvas.yview)
scrollbar.pack(side="right", fill="y")

# Kết nối scrollbar với canvas
url_canvas.configure(yscrollcommand=scrollbar.set)

# Tạo một frame con cho việc thêm các phần tử
url_inner_frame = tk.Frame(url_canvas)
url_canvas.create_window((0, 0), window=url_inner_frame, anchor="nw")

# Hàm tạo các entry frame
def create_entry_frame(num):
    for i in range(num):
        url_entry_frame = tk.Frame(url_inner_frame)
        url_entry_frame.pack(anchor="w", pady=(20,0))
        
        url_label = tk.Label(url_entry_frame, text="Enter YouTube URL:", font=("Arial", 12))
        url_label.pack(side="left", padx=(10, 5))
        
        url_entry = tk.Entry(url_entry_frame, width=40, font=("Arial", 12))
        url_entry.pack(side="left", padx=(5, 10))
        
        search_button = tk.Button(url_entry_frame, text="Search Video", command=search_video_info, font=("Arial", 12))
        search_button.pack(side="left", padx=(0, 10))
    
    # Cập nhật scroll region
    url_canvas.update_idletasks()
    url_canvas.configure(scrollregion=url_canvas.bbox("all"))

# Gọi hàm tạo entry frame
create_entry_frame(10)

# Bind event để cập nhật scroll region khi cửa sổ thay đổi kích thước
url_inner_frame.bind("<Configure>", on_configure)

root.mainloop()