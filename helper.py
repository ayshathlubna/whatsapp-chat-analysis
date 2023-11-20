
import pandas as pd
from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
import emoji
extractor = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]          # fetching no.of messages
    words = []                          # fetching no.of words
    for message in df['message']:
        words.extend(message.split())

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), len(links)

def most_busy_users(df):

    x = df.user.value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': "user"})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    words = []

    for message in df['message']:
        words.extend(message.split())

    to_delete = ['video', 'omitted', 'audio', 'image', "sticker", 'message', 'This', 'was', 'deleted.']
    new_list = [x for x in words if x not in to_delete]
    word_list = pd.DataFrame(new_list, columns=['Word'])

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    df_wc = wc.generate(word_list['Word'].str.cat(sep=" "))
    return df_wc

def most_commom_words(selected_user,df):
    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    words = []

    for message in df['message']:
        words.extend(message.split())

    to_delete = ['video', 'omitted', 'audio', 'image', "sticker", 'message', 'This', 'was', 'deleted.']
    new_list = [x for x in words if x not in to_delete]
    most_commom_df = pd.DataFrame(Counter(new_list).most_common(20))
    return most_commom_df

def emoji_helper(selected_user,df):
    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    monthly_timeline = df.groupby(["month","year"]).count()['message'].reset_index()
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['month'][i] + "-" + str(monthly_timeline['year'][i]))
    monthly_timeline["time"] = time

    return monthly_timeline

def daily_timeline(selected_user,df):

    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    df = df[df.date != "2013-09-27 00:34:38"]

    daily_timeline = df.groupby('only_date')['message'].count().reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'All_members':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


