import pandas as pd
import matplotlib.pyplot as plt
    # Forcasting the expense for next week
def cleanData(fname,user_id):
    df = pd.read_csv(fname)
    print(df.head()) 

    id = user_id
    df_user_1001 = df[df['user_id'] == id]

    print(df_user_1001)



    # Convert 'transaction_date' to datetime objects
    df_user_1001['transaction_date'] = pd.to_datetime(df_user_1001['transaction_date'])

    # Group by day and sum the spend
    daily_spend = df_user_1001.groupby(df_user_1001['transaction_date'].dt.date)['amount'].sum()

    # Create the plot
    plt.plot(daily_spend.index, daily_spend.values)
    plt.xlabel('Day')
    plt.ylabel('Spend')
    plt.title(f'Daily Spend for User {id}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


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
    
