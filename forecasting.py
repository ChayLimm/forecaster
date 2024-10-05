import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import json
import numpy as np

def Forcaste(fname, user_id):
    df = pd.read_csv(fname)
    # print(df.head()) 
    
    id = int(user_id)
    df['user_id'] = df['user_id'].astype(int)
    # Filter data for the specific user
    df_user = df[df['user_id'] == id].copy()  # Explicitly create a copy

     # Check if the user_id exists
    if df_user.empty:
        print(f"Error: User ID {id} does not exist in the data.")
        return None  # Return None if the user ID does not exist

    # Convert 'transaction_date' to datetime objects
    df_user['transaction_date'] = pd.to_datetime(df_user['transaction_date'])

    # Group by day and sum the spend
    daily_spend = df_user.groupby(df_user['transaction_date'].dt.date)['amount'].sum()

    # Find and print duplicated data
    duplicate_rows = df[df.duplicated()]
    print("Duplicated Rows:")
    print(duplicate_rows)

    # Delete duplicated data
    df = df.drop_duplicates()

    # Find and print null data
    null_data = df[df.isnull().any(axis=1)]
    print("Null Data:")
    print(null_data)

    # Delete rows with null values
    df = df.dropna()

    # Find and print outliers using IQR method
    Q1 = df['amount'].quantile(0.25)
    Q3 = df['amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df['amount'] < lower_bound) | (df['amount'] > upper_bound)]
    print("Outliers:")
    print(outliers)

    # Delete outliers
    df = df[(df['amount'] >= lower_bound) & (df['amount'] <= upper_bound)]

    # Convert 'transaction_date' to datetime objects and sort
    df_user['transaction_date'] = pd.to_datetime(df_user['transaction_date'])
    df_user = df_user.sort_values('transaction_date')

    # Group by day and sum the spend
    daily_spend = df_user.groupby('transaction_date')['amount'].sum()

    # Fit an ARIMA model
    model = ARIMA(daily_spend, order=(5, 1, 0))  # Adjust the order as needed
    model_fit = model.fit()

    # Forecast the next 7 days
    forecast = model_fit.forecast(steps=7)

    # Create a date range for the next 7 days
    last_date = daily_spend.index[-1]
    next_7_days = pd.date_range(start=last_date + pd.DateOffset(days=1), periods=7)

    # Create a DataFrame for the forecast
    forecast_df = pd.DataFrame({'transaction_date': next_7_days, 'amount': forecast})
    forecast_json = forecast_df.to_json(orient='records', date_format='iso')
    outliers_json = outliers.to_json(orient='records', date_format='iso')
    
    combined_data = {
        "forecast" : forecast_json,
        "outliner" : outliers_json
    }

    json_data = json.dumps(combined_data, indent=4) # what to return to the fronted


    # Plot the forecast
    total_forecast = forecast_df['amount'].sum()
    print(f"Total forecasted spend for the next 7 days: {total_forecast}")

    # Plot the forecast with outliers highlighted
    plt.plot(daily_spend.index, daily_spend.values, label='Actual')
    plt.plot(forecast_df['transaction_date'], forecast_df['amount'], label='Forecast')
    plt.xlabel('Date')
    plt.ylabel('Spend')
    plt.title(f'Daily Spend Forecast for User {id}')
    plt.legend()

    # Annotate data points with date and spend amount
    for x, y in zip(daily_spend.index, daily_spend.values):
        plt.text(x, y, f'${y:.2f}', ha='center', va='bottom', fontsize=8)
    for x, y in zip(forecast_df['transaction_date'], forecast_df['amount']):
        plt.text(x, y, f'${y:.2f}', ha='center', va='bottom', fontsize=8)

    # Highlight outliers on the plot if there are any
    if not outliers.empty:
        plt.scatter(outliers['transaction_date'], outliers['amount'], color='red', label='Outliers')
        plt.legend()

    plt.tight_layout()
    plt.show()


data = Forcaste("X:/jaytech/TransactionData - Sheet1.csv", "1001")
