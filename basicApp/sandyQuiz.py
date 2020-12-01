# client of choice
import streamlit as st
import numpy as np
import datetime

################
### Set quiz dictionaries
################
quizList=[]
quizList.append({'q':"Which of these is not a fish?", 'opts':["trout","haddock","cod","ambidextrous"], 'a':3})
quizList.append({'q':"Who let the dogs out?", 'opts':["you","me","Heathcliff"], 'a':2})

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

def GetResult(q,num):
    st.write("### Q."+str(num)+" "+q['q'])
    ans=selectbox_with_default("", q['opts'])
    #st.write("debug:",ans)
    if ans==q['opts'][q['a']]:
        st.write("### Correct :smile:")
        return True
    else:
        st.write("### Incorrect. Try again")
        return False


################
### Open app.
################
### intro
nowTime = datetime.datetime.now()
st.write("""## Welcome to Sandy's Quiz on """+dateFormat(nowTime))

### questions
count=0
endOfQuiz=False
while GetResult(quizList[count],count+1):
    count+=1
    if count>=len(quizList):
        endOfQuiz=True
        break
#st.write("debug:",count)

### sign off
if endOfQuiz:
    st.balloons()
    st.write("## End of quiz")
