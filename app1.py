import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__) 

# Load the model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaling.pkl', 'rb'))

# Season mapping (string to integer)
season_mapping = {
    "Fall": 0,
    "spring": 1,
    "summer": 2,
    "Winter": 4
}

# Prediction mapping (numeric output to string)
prediction_mapping = {
    0: "Diseased",
    1: "Healthy"
}

@app.route('/')   # first root
def home():
    return render_template('home.html')  # redirect to the home

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)

    # Convert the 'Season' from string to int using the mapping
    if 'Season' in data and isinstance(data['Season'], str):
        data['Season'] = season_mapping.get(data['Season'].lower(), -1)  # Handle invalid season

    # Convert other columns' numpy types to Python types
    data['Temperature_(°C)'] = float(data['Temperature_(°C)'])
    data['Humidity_(%)'] = float(data['Humidity_(%)'])
    data['Moisture_(%)'] = float(data['Moisture_(%)'])
    data['Rainfall_Density_(mm)'] = float(data['Rainfall_Density_(mm)'])
    data['Leaf_Wetness_(units)'] = float(data['Leaf_Wetness_(units)'])
    data['Month'] = int(data['Month'])

    # Insert placeholders for 'Day' and 'Hour' (since they're missing in the new input)
    data['Day'] = 0  # Placeholder value
    data['Hour'] = 0  # Placeholder value

    # Prepare the input for the model (with all 9 features including the placeholders)
    print(np.array(list(data.values())).reshape(1, -1))
    new_data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    output = model.predict(new_data)

    # Convert NumPy output to Python int for JSON serialization and map to "Healthy" or "Diseased"
    prediction = output[0].item()  # Convert NumPy to Python
    result = prediction_mapping.get(prediction, "Unknown")  # Map to "Healthy" or "Diseased"

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
