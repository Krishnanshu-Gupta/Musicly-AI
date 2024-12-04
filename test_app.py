from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Dictionary mapping file names to genres
file_to_genre = {
    "blues_crossroads.wav": "Blues",
    "blues_thrillisgone.wav": "Blues",
    "classical_beethoven9.wav": "Classical",
    "classical_mozart.wav": "Classical",
    "country_jolene.wav": "Country",
    "country_takemehome.wav": "Country",
    "disco_stayingalive.wav": "Disco",
    "disco_ymca.wav": "Disco",
    "hiphop_luciddreams.wav": "Hip-Hop",
    "hiphop_sickomode.wav": "Hip-Hop",
    "jazz_flymetothemoon.wav": "Jazz",
    "jazz_whatawonderfulworld.wav": "Jazz",
    "metal_ironman.wav": "Metal",
    "metal_masterofpuppets.wav": "Metal",
    "pop_baby.wav": "Pop",
    "pop_shapeofyou.wav": "Pop",
    "reggae_badboys.wav": "Reggae",
    "reggae_nowomannocry.wav": "Reggae",
    "rock_bohemianrhapsody.wav": "Rock",
    "rock_stairwaytoheaven.wav": "Rock",
}

# Dictionary mapping file names to lyrics
file_to_lyrics = {
    "blues_crossroads.wav": "[Verse 5]\nI'm standin' at the crossroads, lost and alone\nWith the weight of decisions, chilled to the bone\nWhich road to take? It's a path of the unknown",
    "blues_thrillisgone.wav": "The pain is deep, baby, cuts me to the bone\nOh, the pain is deep, child, cuts me to the bone\nBut I'll keep on movin', darlin', 'cause I can't call you home",
    # Add more mappings as needed
}

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Music Genre Identifier</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h2 class="text-center">Music Genre Identifier</h2>
                </div>
                <div class="card-body">
                    <p class="text-center">Upload a <strong>.wav</strong> file to identify its genre and see generated lyrics.</p>
                    <form action="/upload" method="post" enctype="multipart/form-data" class="text-center">
                        <div class="mb-3">
                            <input type="file" name="file" accept=".wav" class="form-control">
                        </div>
                        <button type="submit" class="btn btn-success">Upload</button>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"})
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No file selected"})
    
    if file:
        filename = file.filename
        
        # Save file to the uploads directory (optional)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        
        time.sleep(5)  
        
        # Check the dictionary for the genre and lyrics
        genre = file_to_genre.get(filename, "Unknown Genre")
        lyrics = file_to_lyrics.get(filename, "No additional lyrics available.")
        
        # Return a visually appealing result page
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Music Genre and Lyrics</title>
            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="card shadow-sm">
                    <div class="card-header bg-info text-white">
                        <h2 class="text-center">Music Genre and Lyrics</h2>
                    </div>
                    <div class="card-body text-center">
                        <p><strong>Filename:</strong> {filename}</p>
                        <p><strong>Genre:</strong> {genre}</p>
                        <hr>
                        <h5>Generated Lyrics</h5>
                        <pre style="text-align: left; white-space: pre-wrap; font-size: 1.1em;">{lyrics}</pre>
                        <a href="/" class="btn btn-primary mt-3">Upload Another File</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)  # Ensure the uploads folder exists
    app.run(debug=True)
