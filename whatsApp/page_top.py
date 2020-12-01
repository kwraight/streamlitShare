import streamlit as st
import datetime
### data manipulation
import re
### emojis
import emoji
from collections import Counter

#####################
### Select data page
#####################

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))

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

def main_part(state):
    nowTime = datetime.datetime.now()
    st.write("""## :fireworks: **Whatsapp App** :fireworks: """)
    st.write("""### :calendar: ("""+DateFormat(nowTime)+""")""")
    st.write(" --- ")
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
