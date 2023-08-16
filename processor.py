import pandas as pd
import re


def process(data):
    # Print the content as a single string
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APap][Mm]\s'
    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    dic = {
        'chat-date': date,
        'messages': messages

    }
    dataframe = pd.DataFrame(dic)
    dataframe.dropna()
    users_name = []
    user_messages = []

    for i in dataframe['messages']:
        entity = re.split(":\s", i, maxsplit=1)
        if len(entity) == 2:
            users_name.append(entity[0])
            user_messages.append(entity[1])
        else:
            users_name.append(None)
            user_messages.append(None)

    dataframe['users'] = users_name
    dataframe['user-messages'] = user_messages

    dataframe.drop("messages", axis=1, inplace=True)
    dataframe['chat-date'] = pd.to_datetime(dataframe['chat-date'])
    dataframe['year'] = dataframe['chat-date'].dt.year
    dataframe['month'] = dataframe['chat-date'].dt.month_name()
    dataframe['day'] = dataframe['chat-date'].dt.day
    dataframe['Hours'] = dataframe['chat-date'].dt.hour
    dataframe['dayname'] = dataframe['chat-date'].dt.strftime('%A')
    dataframe['minute'] = dataframe['chat-date'].dt.minute

    period = []
    for hour in dataframe[['dayname', 'Hours']]['Hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    dataframe['period'] = period
    dataframe.dropna(inplace=True)
    return dataframe
