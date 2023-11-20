import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    #user_list.remove('T🕴🏻💍💐🦅K🥀🐄🐓🐿🕊')
    user_list.sort()
    user_list.insert(0, "All_members")
    selected_user = st.sidebar.selectbox("show analysis with respect to ", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Links Shared')
            st.title(num_links)


        # finding the busiest user
        if selected_user == 'All_members':
            st.title("Most Busy Users")
            x ,new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # work cloud

        st.title("Work Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words


        most_common_df = helper.most_commom_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
            # st.dataframe(most_common_df)

            # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
            st.pyplot(fig)

        col1, col2 = st.columns(2)

        with col1:
        # daily timeline

            daily_timeline = helper.daily_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.barh(daily_timeline['only_date'], daily_timeline['message'])
            plt.xticks(rotation='vertical')
            st.title("Daily Timeline")
            st.pyplot(fig)

        with col2:
             # monthly timeline

            monthly_timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(monthly_timeline['time'], monthly_timeline['message'])
            plt.xticks(rotation='vertical')
            st.title("Monthly Timeline")
            st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




