import re
import pandas as pd

def preprocess(data):
    pattern='\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm|AM|PM)\s-\s'

    messages=re.split(pattern, data)[1:]

    dates=re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Convert message_date type with coercion
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ', errors='coerce')

# Check for any NaT values and try alternative format
    df['message_date'] = df['message_date'].fillna(pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce'))

# Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)


    #separate users and messages
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:#user name
          users.append(entry[1])
          messages.append(entry[2])
        else:
          users.append('group_notification')
          messages.append(entry[0])
    df['user']= users
    df['message']= messages
    df.drop(columns=['user_message'], inplace=True)

    df['year']=df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['only_date']=df['date'].dt.date
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute



    period = []

    for hour in df['hour']:
       if hour == 23:
            period.append(f"{hour:02}-00")
       elif hour == 0:
            period.append(f"00-{hour+1:02}")
       else:
            period.append(f"{hour:02}-{hour+1:02}")
    df['period'] = period




    return df
