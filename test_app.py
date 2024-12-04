from flask import Flask, render_template, request
from keras.models import load_model
import librosa
import numpy as np
import math
import os

app = Flask(__name__)

# Load the CNN model
model = load_model("model_cnn3.h5")

# Genre dictionary for predictions
genre_dict = {
    0: "disco", 1: "pop", 2: "classical", 3: "metal", 4: "rock",
    5: "blues", 6: "hiphop", 7: "reggae", 8: "country", 9: "jazz"
}

# Upload folder for temporary file storage
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def homepage():
    title = "Music Genre Classifier"
    return render_template('homepage.html', title=title)

@app.route("/predict", methods=["POST"])
def predict():
    if "audio_file" not in request.files:
        return "No file uploaded", 400

    # Save the uploaded file
    audio_file = request.files["audio_file"]
    if not audio_file.filename.endswith(".wav"):
        return "Please upload a valid .wav file", 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], audio_file.filename)
    audio_file.save(file_path)

    # Process audio and extract features
    mfcc = process_audio(file_path)

    # Predict genre
    if mfcc is not None:
        X_to_predict = mfcc[np.newaxis, ..., np.newaxis]
        pred = model.predict(X_to_predict)
        predicted_genre = genre_dict[np.argmax(pred)]
        probability = "{:.2f}".format(max(pred[0]) * 100)

        # Clean up the uploaded file
        os.remove(file_path)

        # Return prediction
        return render_template(
            'prediction.html', genre=predicted_genre, probability=probability
        )
    else:
        return "Error processing audio file", 500

def process_audio(file_path, track_duration=30):
    """Extract MFCC features from an audio file."""
    try:
        SAMPLE_RATE = 22050
        NUM_MFCC = 13
        N_FTT = 2048
        HOP_LENGTH = 512
        SAMPLES_PER_TRACK = SAMPLE_RATE * track_duration
        NUM_SEGMENTS = 10

        samples_per_segment = int(SAMPLES_PER_TRACK / NUM_SEGMENTS)

        signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)
        for d in range(NUM_SEGMENTS):
            start = samples_per_segment * d
            finish = start + samples_per_segment

            mfcc = librosa.feature.mfcc(
                signal[start:finish], sample_rate,
                n_mfcc=NUM_MFCC, n_fft=N_FTT, hop_length=HOP_LENGTH
            )
            mfcc = mfcc.T
            return mfcc

    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
