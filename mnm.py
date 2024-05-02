import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
from threading import Thread


def search_video_info(url, video_info_label, video_image, res_combobox):
    try:
        yt = YouTube(url)

        # Update video information
        video_info_label.config(
            text=f"Title: {yt.title}\nDuration: {yt.length // 60}:{yt.length % 60:02d}\nViews: {yt.views}",
            wraplength=300,  # Set the maximum width before wrapping to a new line
        )

        # Update video thumbnail
        response = requests.get(yt.thumbnail_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((340, 200), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        video_image.config(image=img)
        video_image.image = img

        res = [
            stream.resolution
            for stream in yt.streams.filter(progressive=True).order_by("resolution")
        ]
        res_combobox["values"] = res
        res_combobox.current(0)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to search video information: {e}")


def download_video(url, selected_index, download_label):
    try:
        download_label.config(text="Downloading...")
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True).order_by("resolution")[
            selected_index
        ]
        stream.download()
        messagebox.showinfo("Success", f"Video from {url} downloaded successfully.")
        download_label.config(text="")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video from {url}: {e}")
        download_label.config(text="")


def download_all(res_comboboxes, download_label):
    for url_entry, video_info_label, video_image, res_combobox in zip(
        url_entry_boxes, video_info_labels, video_images, res_comboboxes
    ):
        selected_index = res_combobox.current()
        if selected_index != -1:
            url = url_entry.get().strip()
            if url:
                Thread(
                    target=download_video, args=(url, selected_index, download_label)
                ).start()
        # else:
        #     messagebox.showwarning("Warning", "Please select a resolution to download.")


def delete_url_entry(
    url_entry, video_info_label, video_image, res_combobox, delete_button, search_button
):
    url_entry.grid_remove()
    video_info_label.grid_remove()
    video_image.grid_remove()
    res_combobox.grid_remove()
    delete_button.grid_remove()
    search_button.grid_remove()


def add_url_entry():
    new_url_entry = tk.Entry(url_frame, width=40, font=("Arial", 12))
    new_url_entry.grid(row=len(url_entry_boxes) + 1, column=1, padx=(5, 10), pady=5)
    url_entry_boxes.append(new_url_entry)

    new_video_info_label = tk.Label(url_frame, text="", font=("Arial", 12))
    new_video_info_label.grid(row=len(url_entry_boxes), column=2, padx=(0, 10))
    video_info_labels.append(new_video_info_label)

    new_video_image = tk.Label(url_frame)
    new_video_image.grid(row=len(url_entry_boxes), column=3, padx=(0, 10))
    video_images.append(new_video_image)

    new_res_combobox = ttk.Combobox(
        url_frame, width=10, state="readonly", font=("Arial", 12)
    )
    new_res_combobox.grid(row=len(url_entry_boxes), column=4, padx=(5, 10))
    res_comboboxes.append(new_res_combobox)

    delete_button = tk.Button(
        url_frame,
        text="Delete",
        command=lambda: delete_url_entry(
            new_url_entry,
            new_video_info_label,
            new_video_image,
            new_res_combobox,
            delete_button,
            search_button,
        ),
        font=("Arial", 12),
    )
    delete_button.grid(row=len(url_entry_boxes), column=5, padx=(0, 10))
    delete_buttons.append(delete_button)

    search_button = tk.Button(
        url_frame,
        text="Search Video",
        command=lambda: search_video_info(
            new_url_entry.get(), new_video_info_label, new_video_image, new_res_combobox
        ),
        font=("Arial", 12),
    )
    search_button.grid(row=new_url_entry.grid_info()["row"], column=6, padx=(0, 10))
    search_buttons.append(search_button)


def create_search_button(url_entry, video_info_label, video_image, res_combobox):
    search_button = tk.Button(
        url_frame,
        text="Search Video",
        command=lambda: search_video_info(
            url_entry.get(), video_info_label, video_image, res_combobox
        ),
        font=("Arial", 12),
    )
    search_button.grid(row=url_entry.grid_info()["row"], column=6, padx=(0, 10))


# Initialize root window
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("1000x520")

# URL Entry Frame
url_frame = tk.Frame(root)
url_frame.pack(pady=(20, 0))

url_label = tk.Label(url_frame, text="Enter YouTube URLs:", font=("Arial", 12))
url_label.grid(row=0, column=0, padx=(10, 5))

url_entry_boxes = []
video_info_labels = []
video_images = []
res_comboboxes = []
delete_buttons = []
search_buttons = []

# Create the first URL entry
url_entry = tk.Entry(url_frame, width=40, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=(5, 10))
url_entry_boxes.append(url_entry)

video_info_label = tk.Label(url_frame, text="", font=("Arial", 12))
video_info_label.grid(
    row=0, column=2, padx=(0, 10), sticky="w"
)  # Set sticky="w" to align the label to the left
video_info_labels.append(video_info_label)

video_image = tk.Label(url_frame)
video_image.grid(row=0, column=3, padx=(0, 10))
video_images.append(video_image)

res_combobox = ttk.Combobox(url_frame, width=10, state="readonly", font=("Arial", 12))
res_combobox.grid(row=0, column=4, padx=(5, 10))
res_comboboxes.append(res_combobox)

create_search_button(
    url_entry, video_info_label, video_image, res_combobox
)  # Add "Search Video" button for the first URL entry

add_url_button = tk.Button(
    url_frame, text="Add URL", command=add_url_entry, font=("Arial", 12)
)
add_url_button.grid(row=1, column=1, padx=(5, 10), pady=5)

# Add a label to display download status
download_label = tk.Label(root, text="", font=("Arial", 12))
download_label.pack(pady=(10, 0))

# Download Button
download_button = tk.Button(
    root,
    text="Download All",
    command=lambda: download_all(res_comboboxes, download_label),
    font=("Arial", 12),
)
download_button.pack(pady=(20, 10))

root.mainloop()
