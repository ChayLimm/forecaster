from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import json
import numpy as np

app = Flask(__name__)

def Forcaste(fname, user_id):
    df = pd.read_csv(fname)
    id = int(user_id)
    df['user_id'] = df['user_id'].astype(int)
    
    # Filter data for the specific user
    df_user = df[df['user_id'] == id].copy()

    # Check if the user_id exists
    if df_user.empty:
        return {"error": f"User ID {id} does not exist in the data."}

    # Convert 'transaction_date' to datetime objects
    df_user['transaction_date'] = pd.to_datetime(df_user['transaction_date'])

    # Group by day and sum the spend
    daily_spend = df_user.groupby(df_user['transaction_date'].dt.date)['amount'].sum()

    # Remove duplicated and null data, detect outliers
    df = df.drop_duplicates().dropna()

    Q1 = df['amount'].quantile(0.25)
    Q3 = df['amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df['amount'] < lower_bound) | (df['amount'] > upper_bound)]

    # Fit an ARIMA model
    model = ARIMA(daily_spend, order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast the next 7 days
    forecast = model_fit.forecast(steps=7)
    last_date = daily_spend.index[-1]
    next_7_days = pd.date_range(start=last_date + pd.DateOffset(days=1), periods=7)
    forecast_df = pd.DataFrame({'transaction_date': next_7_days, 'amount': forecast})

    # Convert forecast and outliers to JSON
    forecast_json = forecast_df.to_json(orient='records', date_format='iso')
    outliers_json = outliers.to_json(orient='records', date_format='iso')

    combined_data = {
        "forecast": json.loads(forecast_json),
        "outliers": json.loads(outliers_json)
    }

    return combined_data

# Flask route to handle forecast API
@app.route('/forecast', methods=['POST'])
def forecast():
    try:
        # Get data from the request
        data = request.get_json()
        fname = data['filename']  # CSV file path
        user_id = data['user_id']  # User ID
        
        # Run the forecast function
        result = Forcaste(fname, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
