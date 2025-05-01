from flask import Flask, request, jsonify
from recommender import retrieve_semantic_recommendations
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "")
    category = data.get("category", "All")
    tone = data.get("tone", "All")

    recommendations = retrieve_semantic_recommendations(query, category, tone)

    results = []
    for _, row in recommendations.iterrows():
        results.append({
            "title": row["name"],
            "description": " ".join(row["description"].split()[:30]) + "...",
            "thumbnail": row["large_thumbnail"]
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=False)
