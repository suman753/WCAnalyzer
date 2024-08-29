import re
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        # Total number of messages
        num_messages = df.shape[0]

        # Total number of words
        words = []
        for message in df['message']:
            words.extend(message.split())

        # Number of media messages
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

        # Number of URLs
        links = []
        for message in df['message']:
            urls = re.findall(r'(https?://\S+|www\.\S+)', message)
            links.extend(urls)

        # Return all statistics
        return num_messages, len(words), num_media_messages, len(links)

    else:
        # Filter the dataframe for the selected user
        new_df = df[df['user'] == selected_user]

        # Number of messages for the selected user
        num_messages = new_df.shape[0]

        # Total number of words for the selected user
        words = []
        for message in new_df['message']:
            words.extend(message.split())

        # Number of media messages for the selected user
        num_media_messages = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]

        # Number of URLs for the selected user
        links = []
        for message in new_df['message']:
            urls = re.findall(r'(https?://\S+|www\.\S+)', message)
            links.extend(urls)

        # Return all statistics
        return num_messages, len(words), num_media_messages, len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'Name', 'user': 'Percent'})
    return x, df

def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    

    temp = df[(df['user'] != 'group_notification') & 
              (~df['message'].str.contains('<Media omitted>', na=False))]
    def remove_stop_words(message):
        return " ".join(word for word in message.lower().split() if word not in stop_words)

    # Apply the stop words removal function to each message
    temp['message'] = temp['message'].apply(remove_stop_words)
    
    # Generate the word cloud
    wc = WordCloud(width=800, height=800, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_word(selected_user,df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & 
              (~df['message'].str.contains('<Media omitted>', na=False))]

    words = []

# Process each message in the DataFrame
    for message in temp['message']:
        if isinstance(message, str):  # Ensure the message is a string
            for word in message.lower().split():  # Split the message into words
                if word not in stop_words:  # Filter out stop words
                   words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


#emoji analysis

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    all_emojis = []

# Iterate over each message in the DataFrame
    for message in df['message']:
    # Extract emojis from the message using is_emoji
         emojis = [char for char in message if emoji.is_emoji(char)]
         all_emojis.extend(emojis)

# Count the frequency of each emoji
    emoji_counts = Counter(all_emojis)

# Convert the Counter object to a DataFrame
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])
    return emoji_df



#monthly timeline
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
       time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time

    return timeline
#daily timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


#week active date
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

#month activity map
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
    


# Activity heatmap
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heatmap=(df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0))

    return activity_heatmap