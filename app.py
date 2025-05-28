# Infinity Downloader - A simple Flask app to download YouTube videos in specified quality

from flask import Flask, render_template, request   # Import Flask modules
import yt_dlp                                       # Import yt_dlp for downloading videos
import os
from pathlib import Path
# Set the download directory to "Downloads/Infinity_Store" in the user's home folder
download_dir = str(Path.home()/"Downloads" / "Infinity_Store")
os.makedirs(download_dir, exist_ok=True)    # Create the directory if it doesn't exist

app = Flask(__name__)   # Define the main route for GET and POST requests

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        video_url = request.form.get('url')
        quality = request.form.get('quality')

        if video_url and quality:   # Proceed only if both URL and quality are provided
            try:
                # Set yt_dlp options for downloading the video in the selected quality
                ydl_opts = {
                    'format': f'bestvideo[height={quality}][ext=mp4]+bestaudio[ext=m4a]/best',
                    'merge_output_format': 'mp4',   # Merge video and audio into mp4
                    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                message = f'Video downloaded successfully'  # Success message
            except Exception as e:
                # If an error occurs, show an error message
                message = 'Please provide a valid link and select quality.'
        # else:
        #     message = ""

    # Render the HTML template and pass the message variable
    return render_template('index.html', message=message)

if __name__ == '__main__':
    # app.run(debug=True) 
    port = int(os.environ.get('PORT', 5000))  # use port from render
    app.run(host='0.0.0.0', port=port)  # Run the app on all available IP addresses