# Importing libraries
import warnings  # to avoid streamlit warnings

import matplotlib.pyplot as plt  # graphs
import seaborn as sns  # for graphs
import streamlit as st  # website framework

import helper  # my own file
import processor  # my own file

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)
st.sidebar.title("Whatsapp Chat Analyser App")

# reading data from text file and converting it to a dataFrame
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = processor.process(data)
    df.dropna()
    # st.dataframe(df)

    # fetching users
    df.dropna()
    users_list = df["users"].unique().tolist()
    users_list.insert(0, "overall")
    users_list.sort()

    # creating sidebar
    selected_user = st.sidebar.selectbox("Show analysis wrt", users_list)
    # most common words
    most_word = helper.most_common_words(selected_user, df)
    time_line = helper.time_line(selected_user, df)  # monthly-timeline
    daily_timeline = helper.daily_timeline(selected_user, df)  # daily timeline
    weekly_time_line = helper.weekly_timeline(selected_user, df)  # weekly timeline
    if st.sidebar.button("Show Anylasis"):
        st.header("Statistical Anaylasis")
        shape, word_count, media, links = helper.stats(selected_user, df)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.header("Total Messages")
            st.title(shape)

        with c2:
            st.header("Totals Words")
            st.title(word_count)
        with c3:
            st.header("Shared Media Files")
            st.title(media)
        with c4:
            st.header("Shared Links")
            st.title(links)

        if selected_user == "overall":
            c1, c2 = st.columns(2)

            x, most_act, most_text = helper.busy_user(df)  # most busy user

            fig, ax = plt.subplots()

            with c1:
                st.header("Most Active Users")
                ax.bar(x.index, x.values)
                fig.patch.set_facecolor('lightgray')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with c2:
                st.header("Percentage")
                st.dataframe(most_act)

        st.header("Monthly Time Line")
        fig, ax = plt.subplots()
        ax.plot(time_line['time_line'], time_line['user-messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # st.dataframe(daily_timeline)
        st.header("weekly Time Line")
        fig, ax = plt.subplots()
        ax.plot(weekly_time_line['dayname'], weekly_time_line['user-messages'], color='black')
        # plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(weekly_time_line)
        st.title("Daily Time Line")
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['timelines_daily'], daily_timeline['user-messages'], color='green')
        plt.xticks(rotation='vertical')
        # Adjust the gap between ticks
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Set integer tick locations
        plt.tight_layout()  # Adjust layout for better readability
        st.pyplot(fig)

        st.header("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        c1, c2 = st.columns(2)
        with c1:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # st.dataframe(daily_timeline)
        with c2:
            st.header("Most Busy Day")
            fig, ax = plt.subplots()
            ax.bar(weekly_time_line['dayname'], weekly_time_line['user-messages'], color='red')
            # plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # word_cloud
        st.header('Word-Cloud')
        st.title("Word-cloud Image")
        img = helper.word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(img)
        st.pyplot(fig)
        # most common words
        st.header("Most Common Words")
        # st.dataframe(most_word)
        x = most_word[0]
        y = most_word[1]
        fig, ax = plt.subplots()
        ax.barh(x, y, color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        warnings.resetwarnings()


# Display copyright logo and text using HTML
st.markdown("""
    <div style="text-align: center;">
        <img src="logo.png" alt="Copyright Logo" width="50">
        <p>&copy; 2023 Matrix Inc.|| Zahoor Ahmad
            AI Developer.</p>
    </div>
""", unsafe_allow_html=True)

