from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

def check_new_date(data):
    
    last_date = datetime.now() + timedelta(days=2)
    time.sleep(5)
    while True :
      current_date = datetime.now() + timedelta(days=3)
      if(last_date.date != current_date.date):
          #this is just to print the exceed money
          for budget in data['daily_budget']:
              budget_date = budget['timestamp']
              if (budget_date.day == last_date.day and
                  budget_date.month == last_date.month and
                  budget_date.year == last_date.year):
                  last_date = current_date
                  exceed = budget['amount']
                  return exceed
              
          
      elif(last_date.date == current_date.date):
          print("false")
          return False
      
      time.sleep(60)
    


def spending_budget(transaction, a_month_data):
    
    trans_datetime = datetime.strptime(transaction['timestamp'], '%Y-%m-%d %H:%M:%S')

    for data in a_month_data['daily_budget']:
        
        data_datetime = data['timestamp']

        if (trans_datetime.day == data_datetime.day and
            trans_datetime.month == data_datetime.month and
            trans_datetime.year == data_datetime.year):

            # Update the daily budget amount
            data['amount'] = round(data['amount']- transaction['amount'],2)
            
            # Add transaction id to the list of transactions for the day
            if 'transaction_id' not in data:
                data['transaction_id'] = []  
            data['transaction_id'].append(transaction['transaction_id'])

            # check condition to see if the budget negative

def create_jaytech_plan(amount):
    start_saving_date = datetime.now()
    end_saving_date = datetime.now() + relativedelta(months=1)
    duration_of_saving = end_saving_date - start_saving_date

    budget = round(amount / duration_of_saving.days, 2)

    data = {
        "start_saving_date": start_saving_date,
        "end_saving_date": end_saving_date,
        "amount": amount,
        "daily_budget": [],
        "transaction_id": [],
    }
    for i in range(duration_of_saving.days + 1):
        new_dailyplan = {
            "id": i + 1,
            "timestamp": start_saving_date + timedelta(days=i),
            "amount": budget
        }
        data["daily_budget"].append(new_dailyplan)

    return data


#user scenario


# Sample transaction
spend_sample = {
    "transaction_id": "txn005",
    "user_id": "1001",
    "timestamp": "2024-10-08 09:15:00",
    "type": "purchase",
    "amount": 5.00,
    "currency": "USD",
    "payment_method": "credit_card",
    "description": "Coffee and pastry",
    "status": "completed",
    "reference_id": "ref12349",
    "account_id": "acc001",
    "tax": 0.1,
    "merchant_id": "mer001",
    "quantity": 2,
    "merchant_name": "Cafe",
    "invoice_number": "INV-005"
}
spend_sample2 = {
    "transaction_id": "txn006",
    "user_id": "1001",
    "timestamp": "2024-10-08 09:15:00",
    "type": "purchase",
    "amount": 5.00,
    "currency": "USD",
    "payment_method": "credit_card",
    "description": "Coffee and pastry",
    "status": "completed",
    "reference_id": "ref12349",
    "account_id": "acc001",
    "tax": 0.1,
    "merchant_id": "mer001",
    "quantity": 2,
    "merchant_name": "Cafe",
    "invoice_number": "INV-006"
}

#user created a budget plan within 150 for a month
daily_budget = create_jaytech_plan(150)

print("Before spending:")
for spend in daily_budget['daily_budget']:
    print(f" {spend['id']}  {spend['timestamp']}  {spend['amount']}")

print("############################################################################################")

#user spend twice today
spending_budget(spend_sample, daily_budget)
spending_budget(spend_sample2, daily_budget)

#when turn to new day, jaytech will sum the expense
print("After spending:")
for spend in daily_budget['daily_budget']:
    print(f" {spend['id']}  {spend['timestamp']}  {spend['amount']}")

#if new day we gonn sum the exceed spent
print(check_new_date(daily_budget))  
