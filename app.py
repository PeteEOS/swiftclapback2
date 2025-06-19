from flask import Flask, jsonify, request
import pandas as pd
import random

app = Flask(__name__)

# Load your lyric data
df = pd.read_csv("Recent_Lyric_Phrases.csv")
df.dropna(subset=["lyric_phrase", "sentiment"], inplace=True)

@app.route("/")
def home():
    return "SwiftClapback backend is running. Use the /clapback endpoint."

@app.route("/clapback", methods=["POST"])
def generate_clapback():
    data = request.get_json()
    sentiment = data.get("sentiment", "snarky").lower()

    matches = df[df["sentiment"].str.lower() == sentiment]
    if matches.empty:
        return jsonify({"responses": ["No clapbacks found for that style."]})

    sample = matches.sample(n=min(3, len(matches)))["lyric_phrase"].tolist()
    footer = random.choice(sample)

    return jsonify({"responses": sample, "footer": footer})

if __name__ == "__main__":
    app.run(debug=True)