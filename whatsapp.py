import pandas as pd
from datetime import datetime
### streamlit stuff
import streamlit as st
from streamlit.ReportThread import get_report_ctx
from streamlit.hashing import _CodeHasher
from streamlit.server.Server import Server
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
### main
#####################
def main():
    state = _get_state()
    pages = {
        "Selection": page_selection,
        "Dashboard (PP)": page_perPerson,
        "Dashboard (All)": page_allPersons,
        "Check State": page_checking,
    }

    st.sidebar.title(":joy: WhatsApp Data")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


#####################
### Check state page
#####################
def display_state_values(state):
    st.write("file:", state.file)
    st.write("last entries of dataframe:")
    try:
        st.dataframe(state.df.tail())
    except AttributeError:
        st.write("No data selected")

def page_checking(state):
    st.title(":clipboard: Checking page")
    st.write("---")
    st.write("This is current data:")
    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        state.clear()

#####################
### Select data page
#####################
def startsWithDateAndTime(s):
    # regex pattern for date.(Works only for android. IOS Whatsapp export format is different. Will update the code soon
    ## old pattern
    #pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (AM|PM) -'
    ## apple pattern or android (default)
    patType="and"
    pattern="NYS"
    if len(s)>0 and s[0]=="[":
        patType="app"
    if "app" in patType: # apple
        #st.write("Detect Apple origin")
        pattern = '^\[([0-9]+)(\/)([0-9]+)(\/)([0-9]+[0-9]+), ([0-9]+):([0-9][0-9]):([0-9][0-9])\]'
    else: # android
        #st.write("Detect Android origin")
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+[0-9]+), ([0-9]+):([0-9][0-9]) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

# Finds username of any given format.
def FindAuthor(s):
    patterns = [
        '([\w]+.[\w]+.[\w]+)',             # My Name
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
        '([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
        '([\w]+)[\u263a-\U0001f999]+:',    # Name and Emoji
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

def getDataPoint(line):
    ## apple pattern or android (default)
    patType="and"
    if len(line)>0 and line[0]=="[":
        patType="app"
    splitLine=[]
    if "app" in patType: # apple
        splitLine = line[1:].split('] ')
    else:
        splitLine = line.split(' - ')
    dateTime = splitLine[0]
    date, time = dateTime.split(', ')
    message = ' '.join(splitLine[1:])
    if FindAuthor(message):
        splitMessage = message.split(': ')
        author = splitMessage[0]
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message

st.cache(allow_output_mutation=True)
def GetDataByPath(filename):
    parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
    # Upload your file here
    count=0
    with open(filename, encoding="utf-8") as fp:
        fp.readline() # Skipping first line of the file because contains information related to something about end-to-end encryption
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            #print("line("+str(count)+"):\n"+line)
            #count+=1
            #if count>10: break
            if not line:
                break
            line = line.strip()
            if startsWithDateAndTime(line):
                #print("in timing")
                if len(messageBuffer) > 0:
                    parsedData.append([date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDataPoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)

    return pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.

#st.cache(allow_output_mutation=True)
def GetDataByIO(fileIO):
    parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
    # Upload your file here
    count=0

    fileIO.readline() # Skipping first line of the file because contains information related to something about end-to-end encryption
    messageBuffer = []
    date, time, author = None, None, None
    while True:
        line = fileIO.readline()
        #print("line("+str(count)+"):\n"+line)
        #count+=1
        #if count>10: break
        if not line:
            break
        line = line.strip()
        if startsWithDateAndTime(line):
            #print("in timing")
            if len(messageBuffer) > 0:
                parsedData.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message = getDataPoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

    return pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.

def split_count(text):

    emoji_list = []
    #data = re.findall(r'\\X', text)
    data=text
    #print(data)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list

def page_selection(state):
    st.title(":question: Selection page")
    st.write("---")
    ###
    st.markdown("## Get WhatsApp statistics!")
    st.markdown(" 1. Export file from WhatsApp chat")
    st.markdown(" 2. Drop/Select file in box below")
    st.markdown("  - For *iPhones*, you'll need to unzip the file to get the *txt* inside")
    st.markdown(" 3. View the result (select pages from LHS sidebar):")
    st.markdown("  a. Per person statisics in *Dashboard (PP)* ")
    st.markdown("  b. Total chat statisics in *Dashboard (All)* ")
    st.markdown(" *NB* No data is retained ")

    ## drag and drop method
    state.file = st.file_uploader("Upload a file", type=["txt","zip"])
    #st.write(state.file)

    #dataSel = GetData(join(state.selectDir, state.selectFile))
    if state.file != None:
        dataSel = GetDataByIO(state.file)

        ### total dataSet
        st.write('## Most recent data')
        st.dataframe(dataSel.tail())

        end_df=dataSel.tail(1)
        end_df["Date"]=pd.to_datetime(end_df["Date"], format='%d/%m/%Y')
        st.markdown(f'### Stats up to {end_df.iloc[0]["Date"].day:02}/{end_df.iloc[0]["Date"].month:02}/{end_df.iloc[0]["Date"].year:04}, {end_df.iloc[0]["Time"]}')

        state.df=dataSel

    else:
        st.write("No data yet found")


#####################
### Dashboard per person
#####################
def page_perPerson(state):
    st.title(":chart_with_upwards_trend: Per Person Plots")
    st.write("---")
    ###
    st.markdown(" 1. Contribution chart")
    st.markdown(" 2. Select person")
    st.markdown(" 3. Personal Statistics")
    st.markdown(" 4. Emoji chart")
    st.markdown(" 5. Word cloud")

    if state.df is not None:
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

    else:
        st.write("No data selected")

#####################
### Dashboard all persons
#####################
def page_allPersons(state):
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
        wcImg = wordcloud.WordCloud(stopwords=stopwords, background_color="white").generate(text)
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

#####################
### state functions
#####################
class _SessionState:

    def __init__(self, session):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state():
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session)

    return session._custom_session_state


if __name__ == "__main__":
    main()
