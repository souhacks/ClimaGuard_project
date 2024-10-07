import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaling.pkl', 'rb'))

# Season mapping (string to integer)
season_mapping = {
    "fall": 0,
    "spring": 1,
    "summer": 2,
    "winter": 3
}

# Prediction mapping (numeric output to string)
prediction_mapping = {
    0: "Diseased",
    1: "Healthy"
}

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = request.json['data']
        print("Received data:", data)  # Debugging: Check received data

        # Convert the 'Season' from string to int using the mapping
        if 'Season' in data and isinstance(data['Season'], str):
            print("Season before conversion:", data['Season'])  # Debugging
            data['Season'] = season_mapping.get(data['Season'].lower(), -1)  # Convert Season to int
            print("Converted Season:", data['Season'])  # Debugging

        # Check if the season mapping failed
        if data['Season'] == -1:
            return jsonify({'error': 'Invalid season provided'}), 400

        # Convert other columns to float/int as necessary
        data['Temperature_(°C)'] = float(data.get('Temperature_(°C)', 0))  # Default to 0 if not present
        data['Humidity_(%)'] = float(data.get('Humidity_(%)', 0))
        data['Moisture_(%)'] = float(data.get('Moisture_(%)', 0))
        data['Rainfall_Density_(mm)'] = float(data.get('Rainfall_Density_(mm)', 0))
        data['Leaf_Wetness_(units)'] = float(data.get('Leaf_Wetness_(units)', 0))
        data['Month'] = int(data.get('Month', 1))  # Default to January (1) if not present

        # Insert placeholders for 'Day' and 'Hour' (since they're missing in the new input)
        data['Day'] = 0  # Placeholder value
        data['Hour'] = 0  # Placeholder value

        # Debugging: Print the final data dictionary after conversions
        print("Prepared Data after conversion:", data)

        # Prepare the input for the model (with all features including the placeholders)
        input_array = np.array(list(data.values()))
        print("Input Array before Reshape:", input_array)  # Debugging

        # Check if the input array is valid and not empty
        if input_array.size == 0:
            return jsonify({'error': 'Empty input data'}), 400

        # Reshape and scale the input data
        reshaped_data = input_array.reshape(1, -1)
        print("Reshaped Data:", reshaped_data)  # Debugging

        # Scale the data
        new_data = scaler.transform(reshaped_data)
        print("Scaled Data:", new_data)  # Debugging

        # Make a prediction
        output = model.predict(new_data)
        print("Model Output:", output)  # Debugging

        # Convert the output to a readable format
        prediction = output[0].item()  # Convert NumPy to Python
        result = prediction_mapping.get(prediction, "Unknown")  # Map to "Healthy" or "Diseased"

        return jsonify(result)

    except Exception as e:
        # Print error for debugging purposes
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Gather form values and process them
        form_data = request.form.to_dict()
        print("Form Data:", form_data)

        # Convert Season string to corresponding integer using the season_mapping
        season_str = form_data.get('Season')
        season_value = season_mapping.get(season_str.lower())  # Map the season string to its numeric value
        form_data['Season'] = season_value

        # Convert other fields to float for the model input
        form_data['Temperature_(°C)'] = float(form_data['Temperature_(°C)'])
        form_data['Humidity_(%)'] = float(form_data['Humidity_(%)'])
        form_data['Moisture_(%)'] = float(form_data['Moisture_(%)'])
        form_data['Rainfall_Density_(mm)'] = float(form_data['Rainfall_Density_(mm)'])
        form_data['Leaf_Wetness_(units)'] = float(form_data['Leaf_Wetness_(units)'])
        form_data['Month'] = int(form_data['Month'])

        # Insert placeholders for 'Day' and 'Hour' (since they're missing in the new input)
        form_data['Day'] = 0  # Placeholder value
        form_data['Hour'] = 0  # Placeholder value

        # Convert the form data dictionary into a list of values
        input_data = list(form_data.values())
        print("Processed Form Data:", input_data)  # Debugging

        # Scale the input and make predictions
        final_input = scaler.transform(np.array(input_data).reshape(1, -1))
        output = model.predict(final_input)[0]
        result = prediction_mapping.get(output, "Unknown")  # Map prediction to "Healthy" or "Diseased"

        return render_template("home.html", prediction_text="The apple leaf is {}".format(result))

    except Exception as e:
        print("Error:", e)
        return render_template("home.html", prediction_text="Error: {}".format(e))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
