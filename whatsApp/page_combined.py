import streamlit as st
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
### Dashboard all persons
#####################
def main_part(state):
    st.title(":bar_chart: All Persons Plots")
    st.write("---")
    ###
    st.markdown(" 1. Emoji league table")
    st.markdown(" 2. Word cloud")
    st.markdown(" 3. Timeline")
    st.markdown(" 4. Week profile")
    st.markdown(" 5. Day profile")

    if state.df is not None:
        dataDash = state.df
        dataDash["Date"] = pd.to_datetime(dataDash["Date"], format='%d/%m/%Y')
        dataDash = dataDash.dropna()
        dataDash = dataDash[dataDash['Message'] != '']
        #st.dataframe(dataDash.tail())

        dataDash["emoji"] = dataDash["Message"].apply(split_count)
        ## media
        total_emojis_list = list([a for b in dataDash.emoji for a in b])
        emoji_dict = dict(Counter(total_emojis_list))
        emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
        emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
        st.markdown("## 1. Emoji league table")
        st.dataframe(emoji_df)

        st.markdown("## 2. Word Cloud")
        media_messages_df = dataDash[dataDash['Message'] == '<Media omitted>']
        dataDash = dataDash.drop(media_messages_df.index)

        #st.write(dataDash.Message)
        #st.write("size:",len(dataDash.Message))
        text = " ".join(review for review in dataDash.Message)

        textSplit = text.split()
        #st.write("length:",len(textSplit))
        textFreq = {}
        for txt in textSplit:
            t=txt.replace('.','').replace(',','').replace(' ','')
            if len(txt)<2:
                continue
            if t.isnumeric():
                continue
            if t in textFreq.keys():
                continue
            textFreq[t]=text.count(t)

        stopwords = set(wordcloud.STOPWORDS)
        stopwords.update(["wa","ra", "ga", "na", "ani", "em", "ki", "ah","ha","la","eh","ne","le","https","http","www","image","audio","omitted"])
        #st.write([x for x in dataDash['Author'].unique()])
        stopwords.update([x for x in dataDash['Author'].unique()])
        df_textFreq=pd.DataFrame(textFreq.items(),columns=["text","freq"])
        df_textFreq = df_textFreq[~df_textFreq['text'].isin(stopwords)]
        #st.write(df_textFreq.nlargest(25, ['freq']) )
        addWord = st.text_input(label='Add word to ignore', value='')
        if st.button("Add to ignore words"):
            try:
                state.wordFilters.append(addWord)
            except AttributeError:
                state.wordFilters=[addWord]

        if st.button("Clear query filters"):
            state.wordFilters=[]

        st.write("filters:")
        st.write(state.wordFilters)

        if st.button("Apply filters"):
            try:
                stopwords.update(state.wordFilters)
            except:
                st.write("No filters set yet")

        #st.write(stopwords)
        # Generate a word cloud image
        wcImg = wordcloud.WordCloud(stopwords=stopwords, background_color="white",collocations=False).generate(text)
        # Display the generated image:
        # the matplotlib way:

        wcFig = plt.figure( figsize=(10,5))
        plt.imshow(wcImg, interpolation='bilinear')
        plt.axis("off")
        st.write(wcFig)

        ### Week Profile
        date_df = dataDash
        date_df['MessageCount']=1
        date_df['Date'] = pd.to_datetime(dataDash["Date"], format='%d/%m/%Y')
        date_df.sort_values(by='Date')
        date_df = date_df.groupby("Date").sum()
        date_df.reset_index(inplace=True)
        #st.dataframe(date_df.tail())
        timeFig = px.line(date_df, x="Date", y="MessageCount", title='Number of Messages as time moves on.')
        timeFig.update_xaxes(nticks=20)
        st.markdown("## 3. Timeline")
        st.write(timeFig)

        def dayofweek(i):
            l = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            return l[i]
        day_df=pd.DataFrame(dataDash["Message"])
        day_df['day_of_date'] = dataDash['Date'].dt.weekday
        day_df["messagecount"] = 1
        day = day_df.groupby("day_of_date").sum()
        day.reset_index(inplace=True)
        day['day_of_date'] = day["day_of_date"].apply(dayofweek)
        st.markdown("## 4. Week Profile")
        #st.dataframe(day)

        dayFig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
        dayFig.update_traces(fill='toself')
        dayFig.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0,1.1*day['messagecount'].max()]
            )),
          showlegend=False
        )
        st.write(dayFig)

        ### Day Profile
        def timeofday(i):
            l = [str(x)+"->"+str(x+1) for x in range(0,24,1)]
            return l[i]
        hour_df=pd.DataFrame(dataDash["Message"])
        hour_df["Time"] = pd.to_datetime(dataDash["Time"])
        hour_df['hour_of_day'] = hour_df['Time'].dt.hour
        hour_df["messagecount"] = 1
        hour = hour_df.groupby("hour_of_day").sum()
        hour.reset_index(inplace=True)
        hour['hour_of_day'] = hour["hour_of_day"].apply(timeofday)
        st.markdown("## 5. Day Profile")
        #st.dataframe(hour)

        hourFig = px.line_polar(hour, r='messagecount', theta='hour_of_day', line_close=True)
        hourFig.update_traces(fill='toself')
        hourFig.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0,1.1*hour['messagecount'].max()]
            )),
          showlegend=False
        )
        st.write(hourFig)

    else:
        st.write("No data selected")
