from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random

app = Flask(__name__)
CORS(app)  # <- This enables CORS for all origins

# Load the CSV file
df = pd.read_csv("Recent_Lyric_Phrases.csv")
df.dropna(subset=["lyric_phrase", "sentiment"], inplace=True)

@app.route("/clapback", methods=["POST"])
def clapback():
    data = request.get_json()
    sentiment = data.get("sentiment", "").lower()

    filtered = df[df["sentiment"].str.lower() == sentiment]
    if filtered.empty:
        return jsonify({
            "responses": ["I'm too classy to respond to that."],
            "random_lyric": "I bury hatchets, but I keep maps of where I put them."
        })

    responses = filtered["lyric_phrase"].sample(min(3, len(filtered))).tolist()
    random_lyric = filtered["lyric_phrase"].sample(1).iloc[0]
    return jsonify({
        "responses": responses,
        "random_lyric": random_lyric
    })

if __name__ == "__main__":
    app.run(debug=True)