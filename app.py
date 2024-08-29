import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar title
st.sidebar.title("WhatsApp Chat Analyzer")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read file as bytes and decode to UTF-8
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Display the dataframe
    #st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    
    # Select user for analysis
    selected_user = st.sidebar.selectbox("Show Analysis with respect to", user_list)
    
    # Show analysis button
    if st.sidebar.button("Show Analysis"):
        # Fetch statistics
        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)
        
        # Display statistics in columns
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(links)
#monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
#daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

#activity map
        
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:
          st.header('Most Busy Day !!')
          busy_day = helper.week_activity_map(selected_user, df)
          fig, ax = plt.subplots()
          ax.bar(busy_day.index, busy_day.values, color='skyblue')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

        with col2:
          st.header('Most Busy Month !!')
          busy_month = helper.month_activity_map(selected_user, df)
          fig, ax = plt.subplots()
          ax.bar(busy_month.index, busy_month.values, color='blue')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
#heatmap
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)




        # Display the busiest users if "Overall" is selected
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1,col2=st.columns(2)
            
            # Plotting the most busy users
            with col1:
               ax.bar(x.index, x.values, color='orange')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        #Wordcloud

        st.title('WordCloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        most_common_df=helper.most_common_word(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        #emoji analysis
        
        # emoji_df=helper.emoji_helper(selected_user,df)
        # st.title('Emoji Used')
        # col1,col2=st.columns(2)
        # with col1:
        #     st.dataframe(emoji_df)
        # with col2:
        #     fig, ax = plt.subplots()
        #     ax.pie(emoji_df['count'], labels=emoji_df['emoji'], autopct='%1.1f%%')
        #     st.pyplot(fig)


        emoji_df = helper.emoji_helper(selected_user, df)
        top_5_emojis = emoji_df.sort_values(by='count', ascending=False).head(5)

        
        col1, col2 = st.columns(2)

        with col1:
           st.title('Emoji Usage||')
           st.dataframe(emoji_df)
        with col2:
          st.title('||Emoji pie chart')
          fig, ax = plt.subplots()
          ax.pie(top_5_emojis['count'], labels=top_5_emojis['emoji'], autopct='%1.1f%%')
          st.pyplot(fig)

        
               

            