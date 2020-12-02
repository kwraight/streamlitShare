import streamlit as st
import pandas as pd
### data manipulation
import re
import numpy as np
### emojis
import emoji
from collections import Counter
### plotting
import wordcloud
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

#####################
### Dashboard per person
#####################

def split_count(text):

    emoji_list = []
    #data = re.findall(r'\\X', text)
    data=text
    #print(data)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list


def main_part(state):
    st.title(":chart_with_upwards_trend: Per Person Plots")
    st.write("---")
    ###
    st.markdown(" 1. Contribution chart")
    st.markdown(" 2. Select person")
    st.markdown(" 3. Personal Statistics")
    st.markdown(" 4. Emoji chart")
    st.markdown(" 5. Word cloud")

    doStuff=False
    try:
        if state.df.empty==False:
            doStuff=True
    except AttributeError:
        st.error("No data yet defined")

    if doStuff:
        dataDash = state.df
        dataDash["Date"] = pd.to_datetime(dataDash["Date"], format='%d/%m/%Y')
        dataDash = dataDash.dropna()
        dataDash = dataDash[dataDash['Message'] != '']
        #st.dataframe(dataDash.tail())
        ## media
        total_messages = dataDash.shape[0]
        media_messages = dataDash[dataDash['Message'] == '<Media omitted>'].shape[0]
        ## emojis
        dataDash["emoji"] = dataDash["Message"].apply(split_count)
        emojis = sum(dataDash['emoji'].str.len())
        ## links
        URLPATTERN = r'(https?://\S+)'
        dataDash['urlcount'] = dataDash.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
        links = np.sum(dataDash.urlcount)

        media_messages_df = dataDash[dataDash['Message'] == '<Media omitted>']
        messages_df = dataDash.drop(media_messages_df.index)

        messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s : len(s))
        messages_df['Word_Count'] = messages_df['Message'].apply(lambda s : len(s.split(' ')))

        # Creates a list of unique Authors - ['Manikanta', 'Teja Kura', .........]
        authorsList = messages_df.Author.unique()

        authors_df= pd.DataFrame(dataDash["Author"])
        authors_df['MessageCount']=1
        authors_df= authors_df.groupby("Author").sum()
        authors_df.reset_index(inplace=True)
        #st.dataframe(authors_df)

        st.markdown('## 1. Contribution chart')
        authFig = px.pie(authors_df, values='MessageCount', names='Author')
        authFig.update_traces(textposition='inside', textinfo='percent+label')
        st.write(authFig)
        chattiest=authors_df.iloc[authors_df['MessageCount'].argmax()]['Author']
        Nchattiest=authors_df.iloc[authors_df['MessageCount'].argmax()]['MessageCount']
        st.write("### "+chattiest+" is the chattiest:",Nchattiest,"messages")

        verbosest="NYS"
        verbosity=-1
        for a in messages_df["Author"].unique():
            words_per_message = np.sum(messages_df.query('Author=="'+a+'"')['Word_Count'])/messages_df.query('Author=="'+a+'"').shape[0]
            if words_per_message > verbosity:
                verbosity=words_per_message
                verbosest=a
        st.write("### "+verbosest+" is the most wordy:",round(verbosity, 2),"words per message")

        st.markdown('## 2. Select person')
        author = st.selectbox('Select author', authorsList)

        st.markdown("## 3. Personal Statistics for "+author)
        # Filtering out messages of particular user
        req_df= messages_df[messages_df["Author"] == author]
        # req_df will contain messages of only one particular user
        st.write(f'Stats of {author}:')
        # shape will print number of rows which indirectly means the number of messages
        st.write('Messages Sent', req_df.shape[0])
        #Word_Count contains of total words in one message. Sum of all words/ Total Messages will yield words per message
        words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
        st.write('Words per message', round(words_per_message, 2))
        #media conists of media messages
        media = media_messages_df[media_messages_df['Author'] == author].shape[0]
        st.write('Media Messages Sent', media)
        # emojis conists of total emojis
        emojis = sum(req_df['emoji'].str.len())
        st.write('Emojis Sent', emojis)
        #links consist of total links
        links = sum(req_df["urlcount"])
        st.write('Links Sent', links)

        dummy_df = messages_df[messages_df['Author'] == author]
        total_emojis_list = list([a for b in dummy_df.emoji for a in b])
        if len(total_emojis_list)<1:
            st.write('No emojis for for', author,"\n")
        emoji_dict = dict(Counter(total_emojis_list))
        emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
        st.write('Emoji Distribution for', author)
        author_emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
        emoFig = px.pie(author_emoji_df, values='count', names='emoji')
        emoFig.update_traces(textposition='inside', textinfo='percent+label')
        st.markdown("## 4. Emoji chart for "+author)
        st.write(emoFig)

        text = " ".join(review for review in dummy_df.Message)
        stopwords = set(wordcloud.STOPWORDS)
        stopwords.update(["ra", "ga", "na", "ani", "em", "ki", "ah","ha","la","eh","ne","le","https","http","www","image","audio","omitted"])
        # Generate a word cloud image
        wcImg = wordcloud.WordCloud(stopwords=stopwords, background_color="white").generate(text)
        # Display the generated image:
        # the matplotlib way:

        wcFig = plt.figure( figsize=(10,5))
        plt.imshow(wcImg, interpolation='bilinear')
        plt.axis("off")
        st.markdown("## 5. World cloud for "+author)
        st.write(wcFig)
