# api.py
from flask import Flask, request, jsonify
from recommender import retrieve_semantic_recommendations
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "")

    # category = data.get("category", "All")
    # tone = data.get("tone", "All") 

    # print("Query:", query)
    # print("Category:", category)
    # print("Tone:", tone)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = retrieve_semantic_recommendations(query)
    # print(results)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
