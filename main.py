import yt_dlp
import os
import math
import subprocess
import time
import threading

def download_video_from_url(url):
    """
    Downloads the best quality video from a given URL using yt-dlp.
    Returns the path to the downloaded video file.
    """
    
    # 1. Define the directory to save the file
    download_dir = "D:\downloads"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # 2. Define the options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        'outtmpl': os.path.join(download_dir, '%(title)s [%(id)s].%(ext)s'),
        'noprogress': False, 
        'noplaylist': True,
    }

    print(f"Attempting to download: {url}")
    
    try:
        # Use YoutubeDL to get video info and download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info to get the filename
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
        
        print("\n✅ Download complete!")
        return downloaded_file

    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ An error occurred during download: {e}")
        return None
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        return None

def video_to_gifs(video_path, output_dir, clip_length=3, fps=15):
    """
    Converts a video file to multiple GIF clips.
    """
    # ✅ Ensure output folder exists (create if not present)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📂 Created output directory: {output_dir}")
    else:
        print(f"📂 Using existing output directory: {output_dir}")

    # Get video duration using ffprobe
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    try:
        duration = float(result.stdout.strip())
    except ValueError:
        print("❌ Could not read video duration. Check ffmpeg installation.")
        return

    print(f"Video length: {duration:.2f} seconds")

    # Number of GIFs to create
    num_clips = math.ceil(duration / clip_length)
    print(f"Creating {num_clips} GIF clips of {clip_length} seconds each...")

    for i in range(num_clips):
        start = i * clip_length
        output_path = os.path.join(output_dir, f"output_{i+1}.gif")

        # ffmpeg command
        command = [
            "ffmpeg", "-y",             
            "-ss", str(start),          
            "-t", str(clip_length),     
            "-i", video_path,           
            "-vf", f"fps={fps},scale=480:-1:flags=lanczos", 
            output_path
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"✅ Saved: {output_path}")

def input_with_timeout(prompt, timeout=3, default=""):
    """
    Get user input with a timeout. If no input is provided within the timeout period,
    returns the default value.
    """
    print(f"{prompt} (Waiting {timeout} seconds...)")
    
    # Flag to track if we got input
    got_input = False
    user_input = default
    
    def get_input():
        nonlocal got_input, user_input
        try:
            user_input = input().strip().strip('"').strip("'")
            got_input = True
        except:
            pass
    
    # Start the input thread
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()
    
    # Wait for the thread to complete or timeout
    input_thread.join(timeout)
    
    if got_input:
        return user_input
    else:
        print(f"\nNo input received. Using default directory: '{default}'")
        return default

# --- Main Program Execution ---
if __name__ == "__main__":
    
    # Step 1: Download video from URL
    print("🎥 VIDEO DOWNLOADER & GIF CONVERTER")
    print("=" * 40)
    
    video_link = input("Paste the video URL and press Enter: ").strip()

    if not video_link:
        print("No URL provided. Exiting.")
        exit()

    # Download the video
    downloaded_video_path = download_video_from_url(video_link)
    
    if not downloaded_video_path or not os.path.exists(downloaded_video_path):
        print("❌ Video download failed. Exiting.")
        exit()

    print(f"📁 Downloaded video: {downloaded_video_path}")
    
    # Step 2: Get output directory for GIFs with timeout
    print("\n" + "=" * 40)
    print("🔄 CONVERTING TO GIFS")
    print("=" * 40)
    
    # Hardcoded GIF directory
    HARDCODED_GIF_DIR = r"C:\Users\harip\ALL TEST"
    
    output_dir = input_with_timeout(
        f"📁 Enter custom output folder for GIFs (or press Enter to use default: {HARDCODED_GIF_DIR})", 
        timeout=3, 
        default=HARDCODED_GIF_DIR
    )
    
    # Step 3: Convert the downloaded video to GIFs
    video_to_gifs(downloaded_video_path, output_dir)
    
    print("\n🎉 All processes completed successfully!")
    print(f"📁 Video downloaded to: {downloaded_video_path}")
    print(f"📁 GIFs saved to: {output_dir}")
