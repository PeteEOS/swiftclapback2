from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load and clean data
df = pd.read_csv("Recent_Lyric_Phrases.csv")
df.dropna(subset=['lyric_phrase', 'sentiment'], inplace=True)
df['sentiment'] = df['sentiment'].str.strip().str.lower()
df['lyric_phrase'] = df['lyric_phrase'].str.strip()

# Fallback list for unmatched sentiments
fallback_lyrics = [
    "I bury hatchets, but I keep maps of where I put them.",
    "You can walk away, but I’m still the queen of this story.",
    "The old me can't come to the phone right now... she's thriving."
]

@app.route("/clapback", methods=["POST"])
def generate_clapback():
    try:
        data = request.get_json()
        sentiment = data.get("sentiment", "").strip().lower()

        if not sentiment:
            return jsonify({"error": "Sentiment not provided."}), 400

        matches = df[df['sentiment'] == sentiment]

        if matches.empty:
            choices = random.sample(fallback_lyrics, min(3, len(fallback_lyrics)))
        else:
            phrases = matches['lyric_phrase'].dropna().unique().tolist()
            random.shuffle(phrases)
            choices = phrases[:3] if len(phrases) >= 3 else phrases

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return jsonify({
            "responses": choices,
            "timestamp": timestamp
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("SwiftClapback backend is running. Use the /clapback endpoint.")
    app.run(debug=True)
