from datetime import datetime
from dateutil.relativedelta import relativedelta
 


def create_jaytech_plan(amount):
  start_saving_date = datetime.now()
  end_saving_date = datetime.now() +  relativedelta(months=1)
  duration_of_saving = end_saving_date - start_saving_date
  
  budget = round(amount / duration_of_saving.days,2)
  
  data = {
    "start_saving_date": start_saving_date,
    "end_saving_date": end_saving_date,
    "amount": amount,
    "daiy_budget": [
      for i+1 in range(durations+1)
        {
            "id": 1,
            "date": start_saving_date + timedelta(days= i),
            "amount": budget,
        },       
    ]
}
  
  
  
create_jaytech_plan(150)