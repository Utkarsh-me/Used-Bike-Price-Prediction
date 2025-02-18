from flask import Flask, request, jsonify, render_template
from supabase import create_client, Client
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = "https://ivarjhpbeasabwwtmvnx.supabase.co"  # Add your Supabase URL here
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2YXJqaHBiZWFzYWJ3d3Rtdm54Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MjA3NDksImV4cCI6MjA1MzM5Njc0OX0.ZxUCDNIPBWLjJuN71fc7xlTdplOqNGRI2JPPpEjfW9U"  # Add your Supabase Service Role Key here

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load ML model
model = pickle.load(open('used_bike.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('bike_land.html')

@app.route("/predict", methods=['POST', 'GET'])
def predict():
    try :
        if request.method == "POST":
            kms = (request.form['kms'])
            owner = (request.form['owner'])
            age = (request.form['age'])
            power = (request.form['power'])
            brand = (request.form['brand'])
            
        # Prepare input data for the model
            arr = np.array([[kms, owner, age, power, brand]])
            prediction = model.predict(arr)


            data = {
                'kms' : kms,
                'owner' : owner,
                'age' : age,
                'power' : power,
                'brand' : brand,
                'predicted_price': int(prediction[0])
            }
            response = supabase.table("used_bike_price").insert(data).execute()

        return render_template('bike_res.html', prediction=prediction)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)