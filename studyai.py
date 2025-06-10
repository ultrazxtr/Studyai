import yt_dlp
import whisper
import sys
import os

def download_audio(url, output_path="audio.mp3"):
    """Download audio from a YouTube video using yt-dlp."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Audio downloaded successfully to {output_path}")
    except Exception as e:
        print(f"Error downloading audio: {e}")
        sys.exit(1)

def transcribe_audio(audio_path, output_file="transcript.txt", output_srt="transcript.srt"):
    """Transcribe audio to text using Whisper."""
    try:
        # Load Whisper model (use 'base' for speed, 'large' for better accuracy)
        model = whisper.load_model("base")
        # Transcribe audio
        result = model.transcribe(audio_path)
        # Save transcript to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"Transcript saved to {output_file}")
        
        # Save transcript in SRT format
        with open(output_srt, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                f.write(f"{i+1}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")
        print(f"Transcript saved to {output_srt} in SRT format")
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        sys.exit(1)
    finally:
        # Clean up audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Cleaned up temporary audio file: {audio_path}")

def format_time(time_in_seconds):
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def main():
    # Get YouTube video URL from user input
    VIDEO_URL = input("Enter the YouTube video URL: ").strip()
    AUDIO_PATH = "audio.mp3"
    OUTPUT_FILE = "transcript.txt"
    OUTPUT_SRT = "transcript.srt"
    # Download audio
    download_audio(VIDEO_URL, AUDIO_PATH)
    # Transcribe audio to text
    transcribe_audio(AUDIO_PATH, OUTPUT_FILE, OUTPUT_SRT)

if __name__ == "__main__":
    main()
