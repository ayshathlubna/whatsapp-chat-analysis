import re
import pandas as pd

def preprocess(data):
    pattern = '\[\d{2}\/\d{2}\/\d{4}, \d{1,2}:\d{2}:\d{2} [APap][Mm]\] '
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='[%d/%m/%Y, %I:%M:%S %p] ')
    df['only_date'] = pd.to_datetime(df['date'], format='[%d/%m/%Y, %I:%M:%S %p] ')
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        users.append(entry[1])
        messages.append(entry[2])

    df['user'] = users
    df['message'] = messages
    df['message'] = df['message'].str.replace('\u200e','')
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df["date"].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df


