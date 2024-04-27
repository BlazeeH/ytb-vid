# YouTube Video Downloader

This is a simple YouTube video downloader application built using Python's Tkinter library. It allows users to enter a YouTube video URL, search for video information such as title, duration, and views, select a desired resolution for download, and download the video.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- Tkinter (should be included with Python)
- pytube
- Pillow
- requests

You can install the dependencies using pip:

```
pip install pytube Pillow requests
```
## How to Use

**Clone the Repository:**
```
git clone https://github.com/BlazeeH/ytb-vid
```

2. **Navigate to the Project Directory:** 
```
cd ytb-vid
```
3. **Run the Application:** 
```
python mnm.py
```
4. **Enter YouTube URL:**
- In the provided entry field, enter the URL of the YouTube video you want to download.
- Click on the "Search Video" button to retrieve video information.

5. **Select Resolution:**
- After searching for the video, a list of available resolutions will be displayed in the dropdown menu.
- Select the desired resolution from the dropdown menu.

6. **Download Video:**
- Once you have selected the resolution, click on the "Download Selected" button to start downloading the video.
- The downloaded video will be saved in the same directory as the application.

7. **Error Handling:**
- If there are any errors during the process, error messages will be displayed in a pop-up window.

## Notes

- This application only supports downloading videos available in progressive streams.
