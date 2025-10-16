import cv2
import os
import time
import numpy as np
import shutil
from pytubefix import YouTube
import tempfile
from pathlib import Path

def frame_to_ascii(frame, width):
    """Convert a video frame to ASCII art"""
    chars = np.asarray(list(" .:-=+*#%@"))
    height = max(1, int(frame.shape[0] * width / frame.shape[1] / 2))
    small = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    indices = (gray / 255.0 * (len(chars) - 1)).astype(int)
    ascii_frame = "\n".join("".join(chars[i] for i in row) for row in indices)
    return ascii_frame

def play_ascii_video(video_path):
    """Play video as ASCII art (auto fullscreen terminal)"""
    if not os.path.exists(video_path):
        print(f"❌ Error: '{video_path}' not found")
        return

    term_size = shutil.get_terminal_size((80, 24))
    width = term_size.columns

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1.0 / fps if fps > 0 else 1.0 / 30

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("\n✅ End of video 🎬")
                break

            ascii_art = frame_to_ascii(frame, width)
            print("\033[H\033[J", end="")  # clear screen fast
            print("\033[92m" + ascii_art + "\033[0m", end="", flush=True)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("\n\n🛑 Playback stopped by user")
    finally:
        cap.release()

def download_youtube_video(url):
    """Download YouTube video using pytubefix"""
    print("📥 Downloading YouTube video...")
    yt = YouTube(url)

    # En iyi progresif MP4 stream'i seç
    stream = yt.streams.filter(file_extension='mp4', progressive=True)\
                       .order_by('resolution').desc().first()

    # Geçici dizin oluştur
    tmp_dir = Path(tempfile.gettempdir()) / "qwazz_ascii"
    tmp_dir.mkdir(exist_ok=True)
    file_path = tmp_dir / "temp_video.mp4"

    print(f"📂 Saving to: {file_path}")
    stream.download(output_path=tmp_dir, filename="temp_video.mp4")

    if not file_path.exists():
        raise FileNotFoundError("❌ Download failed — file not found.")

    print(f"✅ Downloaded: {yt.title[:40]}...")
    return str(file_path)

if __name__ == "__main__":
    print("\n🎞️  QwaZz ASCII Video Player – YouTube Edition 🎞️")
    print("Supports: Local video files or YouTube links\n")

    video = input("Enter video file path or YouTube URL: ").strip()

    if video.startswith("http"):
        video = download_youtube_video(video)

    print("\n🚀 Starting fullscreen ASCII playback...\n")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    play_ascii_video(video)
