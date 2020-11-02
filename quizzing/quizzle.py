# general
import streamlit as st
import numpy as np
import datetime
# particular
import infrastructure as infra
import questions

################
### Set quiz dictionaries
################
qList= []
for q in questions.quizList:
    qList.append(infra.Question(**q))

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
    st.write("### Q."+str(num)+" ("+q.code+") "+q.text)
    ans=selectbox_with_default("", q.options)
    #st.write("debug:",ans)
    if ans in q.options[q.index]:
        st.write("### Correct :smile: "+str(q.points)+" points")
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
score=[]
endOfQuiz=False
while GetResult(qList[count],count+1):
    score.append(qList[count].points)
    count+=1
    if count>=len(qList):
        endOfQuiz=True
        break
#st.write("debug:",count)

### sign off
if endOfQuiz:
    st.balloons()
    st.write("## End of quiz")
    st.write("### Final score:",sum(score))
    st.write("### each result:",*score)
