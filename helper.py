from urlextract import URLExtract
import wordcloud as wc
from collections import Counter
import pandas as pd
import emoji
import matplotlib.pyplot as plt


def stats(selected_user, df):
    df.dropna(inplace=True)
    if selected_user == "overall":
        words = []
        media = []
        ur = []
        u = URLExtract()
        for i in df['user-messages']:
            if i == "<Media omitted>\n":
                media.append(i)
            ur.extend(u.find_urls(i))
            words.extend(i.split())

        return df.shape[0], len(words), len(media), len(ur)

    else:
        new_df = df[df["users"] == selected_user]
        words_new = []
        media = []
        ur = []
        u = URLExtract()
        for i in new_df['user-messages']:
            if i == "<Media omitted>\n":
                media.append(i)
            ur.extend(u.find_urls(i))
            words_new.extend(i.split())

        return new_df.shape[0], len(words_new), len(media), len(ur)


def busy_user(df):
    df.dropna(inplace=True)
    df1 = round((df['users'].value_counts() / df.shape[0] * 100), 2).reset_index().rename(
        columns={'index': 'name', 'users': 'Percentage'})
    v = df['users'].value_counts().head()
    top_5_messages = df['user-messages'].value_counts().head(5)

    return v, df1, top_5_messages


def word_cloud(selected_user, df):
    if selected_user != "overall":
        df = df[df['users'] == selected_user]

    wcloud = wc.WordCloud(width=500, height=500, max_words=100, min_font_size=5, background_color='white')
    df_cloud = wcloud.generate(df['user-messages'].str.cat(sep=" "))

    return df_cloud


def most_common_words(selected_user, df):
    df.dropna(inplace=True)
    if selected_user != "overall":
        df = df[df['users'] == selected_user]

    temp = df[df['user-messages'] != "<Media omitted>\n"]
    temp = temp[temp['user-messages'] != "group messages"]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    cleaned_word = []
    for message in temp['user-messages']:
        for word in message.split():
            word = word.lower()
            if word not in stop_words:
                cleaned_word.append(word)

    # cleaned_word
    dataf = pd.DataFrame(Counter((cleaned_word)).most_common(20))

    return dataf


def time_line(selected_user, df):
    df.dropna(inplace=True)
    if selected_user != "overall":
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year', 'month']).count()['user-messages'].reset_index()
    timelines = []
    for i in range(timeline.shape[0]):
        timelines.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time_line'] = timelines

    return timeline


def daily_timeline(selected_user, df):
    df.dropna(inplace=True)
    if selected_user != "overall":
        df = df[df['users'] == selected_user]
    df['Date'] = df['chat-date'].dt.date
    df['dayname'] = df['chat-date'].dt.strftime('%A')
    # dataframe

    daily_mess = df.groupby(['Date', 'dayname']).count()['user-messages'].reset_index()
    timelines_daily = []
    for i in range(daily_mess.shape[0]):
        timelines_daily.append(str(daily_mess['Date'][i]) + '-' + str(daily_mess['dayname'][i]))

    daily_mess['timelines_daily'] = timelines_daily

    return daily_mess


def weekly_timeline(selected_user, df):
    df.dropna(inplace=True)
    if selected_user != "overall":
        df = df[df['users'] == selected_user]

    # WEEKLY timeline on day's name
    weekly_time_line = df.groupby("dayname").count()["user-messages"].reset_index()

    return weekly_time_line


def activity_heatmap(selected_user, df):
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='dayname', columns='period', values='user-messages', aggfunc='count').fillna(0)

    return user_heatmap


def month_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()
