import whisper
import sys
from pydub import AudioSegment

def transcribe_audio(file_path):
    # Load the Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("base")  # Options: "tiny", "base", "small", "medium", "large"
    
    # Convert audio to Whisper-compatible format if necessary
    print("Processing audio file...")
    try:
        audio = AudioSegment.from_file(file_path)
        processed_path = "processed_audio.wav"
        audio.export(processed_path, format="wav")
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return
    
    # Transcribe the audio
    print("Transcribing audio...")
    result = model.transcribe(processed_path)
    
    # Print the transcription (lyrics)
    print("\nTranscription (Lyrics):")
    print(result["text"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe_lyrics.py <audio_file.wav>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    transcribe_audio(audio_file)
