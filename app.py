from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load model
with open("models/iris_model.pkl", "rb") as f:
    model = pickle.load(f)

print("model loaded successfully")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Iris Model API. Use POST /predict to make predictions."})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    input_features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(input_features)
    return jsonify({"prediction": int(prediction[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"