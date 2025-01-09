from flask import Flask, request, jsonify
import pickle
import pandas as pd
import traceback

app = Flask(__name__)

# Load the trained model
try:
    with open('../ex/avocado_model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    traceback.print_exc()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Convert the JSON data to a DataFrame
        df = pd.DataFrame([data])

        # Convert the 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Drop the 'Date' column as it was not used in the training
        df = df.drop(columns=['Date'])

        # Make predictions
        prediction = model.predict(df)

        # Convert the prediction to a standard Python float
        prediction = float(prediction[0])

        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction})
    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)