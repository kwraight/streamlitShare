# client of choice
import streamlit as st
import numpy as np
import datetime

################
### Set quiz dictionaries
################
quizList=[]
quizList.append({'q':"Which of these is not a fish?", 'opts':["trout","haddock","cod","ambidextrous"], 'a':3})
#quizList.append({'q':"Who let the dogs out?", 'opts':["you","me","other"], 'a':2})

################
### Useful functions
################
### set selection default value
DEFAULT = '< PICK A VALUE >'
def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
    func = st.sidebar.selectbox if sidebar else st.selectbox
    return func(text, np.insert(np.array(values, object), 0, default))

### format datetime
def dateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))

################
### Open app.
################
nowTime = datetime.datetime.now()
st.write("""## Welcome to Sandy's Quiz on """+dateFormat(nowTime))

for q in quizList:
    ans=selectbox_with_default(q['q'], q['opts'])
    #st.write("debug:",ans)
    if ans==q['opts'][q['a']]:
        st.balloons()
        st.write("Correct!")
    else:
        st.write("Incorrect!")
