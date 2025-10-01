import yt_dlp
import os
import math
import subprocess
import time

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

def get_input_with_timeout(prompt, timeout=3, default=""):
    """
    Simple input with timeout that doesn't use threading
    """
    print(prompt)
    start_time = time.time()
    user_input = ""
    
    print(f"You have {timeout} seconds to type a custom name, or we'll use: '{default}'")
    print("Type your input and press Enter, or just wait...")
    
    # Simple input with timeout
    try:
        while (time.time() - start_time) < timeout:
            if os.name == 'nt':  # Windows
                import msvcrt
                if msvcrt.kbhit():
                    user_input = input()
                    break
            else:  # Unix/Linux/Mac
                import select
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    user_input = input()
                    break
            time.sleep(0.1)
    except:
        pass
    
    if user_input:
        return user_input.strip()
    else:
        print(f"Using default: '{default}'")
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
    
    # Step 2: Get folder name for GIFs
    print("\n" + "=" * 40)
    print("🔄 CONVERTING TO GIFS")
    print("=" * 40)
    
    # Extract video name for default folder name
    video_filename = os.path.basename(downloaded_video_path)
    video_name_without_ext = os.path.splitext(video_filename)[0]
    default_folder_name = video_name_without_ext.replace(" ", "_") + "_gifs"
    
    # Hardcoded base directory
    HARDCODED_BASE_DIR = r"C:\Users\harip\ALL TEST"
    
    # Get folder name with timeout
    folder_name = get_input_with_timeout(
        f"\n📂 Enter folder name for GIFs (will be created in {HARDCODED_BASE_DIR}):",
        timeout=3,
        default=default_folder_name
    )
    
    # Create the final output directory path
    final_output_dir = os.path.join(HARDCODED_BASE_DIR, folder_name)
    
    print(f"\n🎯 Final output directory: {final_output_dir}")
    
    # Step 3: Convert the downloaded video to GIFs
    video_to_gifs(downloaded_video_path, final_output_dir)
    
    print("\n🎉 All processes completed successfully!")
    print(f"📁 Video downloaded to: {downloaded_video_path}")
    print(f"📁 GIFs saved to: {final_output_dir}")
