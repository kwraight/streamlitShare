import pandas as pd
import numpy as np
import datetime
### streamlit stuff
import streamlit as st
### plotly
import plotly.express as px
import plotly.graph_objects as go
### datapane
import altair as alt
### infrastructure
import infrastructure
# particular
import infrastructure as infra
import questions

################
### Useful functions
################
### set selection default value
DEFAULT = '< PICK A VALUE >'
def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
    func = st.sidebar.selectbox if sidebar else st.selectbox
    return func(text, np.insert(np.array(values, object), 0, default))

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))

def GetResult(q,num):
    st.write("### Q."+str(num)+" "+q.text)
    ans=selectbox_with_default("", q.options)
    #st.write("debug:",ans)
    if ans in q.options[q.index]:
        st.write("### Correct :smile: "+str(q.points)+" points")
        return True
    else:
        st.write("### Incorrect. Try again")
        return False

################
### Set quiz dictionaries
################
bigList= []
for q in questions.quizList:
    bigList.append(infra.Question(**q))

#####################
### main
#####################
def main():
    ### get state variable
    state = infrastructure._get_state()

    ### define pages dictionary
    pages = {
        "Top Page": page_top,
        "First": page_first,
        "Second": page_second,
        "Results": page_results,
        "Debug": page_debug,
    }

    ### sidebar
    st.sidebar.title(":smile: Quiz WebApp")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    ### mini-state summary
    # if st.sidebar.button("State Summary"):
    #     try:
    #         st.sidebar.markdown("data set size: "+str(len(state.allData.index)))
    #     except:
    #         st.sidebar.markdown("No data yet selected")

    ### debug toggle
    debug = st.sidebar.checkbox("Toggle debug")
    if debug:
        state.debug=True
    else: state.debug=False

    ### display  selected page using state variable
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


#####################
### Check state page
#####################
def display_state_values(state):

    st.write("## All data")
    st.write("Debug setting:", state.debug)
    try:
        st.write(state.score)
        df_results=pd.DataFrame(state.score.items(), columns=["code","points"])
        st.write(df_results)
    except AttributeError:
        st.write("No data available")

def page_debug(state):
    st.title(":clipboard: Checking page")
    st.write("---")
    st.write("This is the values retained in the state data:")
    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        state.clear()


#####################
### Top page
#####################
def page_top(state):
    nowTime = datetime.datetime.now()
    st.write("""## Welcome to the **Great \'Ritchie T\'** Quiz """)
    st.write("""### ("""+DateFormat(nowTime)+""")""")
    st.write(" --- ")
    ###

    st.write("Total questions:",len(bigList))

    if st.button("Ready"):
        state.score={}

    if state.debug:
        st.write("score:",sum(state.score.values()))
        st.write("score per question:",*state.score.values())

#####################
### First page
#####################
def page_first(state):
    st.title(":question: Round 1")
    st.write("---")
    st.write("## Instruction")
    st.write("  * answer them questions")
    st.write("---")
    ###

    ### questions
    count=0

    endOfRound=False
    qList=[q for q in bigList if "r1" in q.code.lower()]
    while GetResult(qList[count],count+1):
        if state.debug: st.write("question code:",qList[count].code)
        state.score[qList[count].code]=qList[count].points
        count+=1
        if count>=len(qList):
            endOfRound=True
            break
    #st.write("debug:",count)

    ### sign off
    if endOfRound:
        st.balloons()
        st.write(" --- ")
        st.write("## End of round 1")
        results=[v for k,v in state.score.items() if "r1" in k]
        st.write("### Round score:",sum(results))
        st.write("### each result:",*results)


#####################
### Second page
#####################
def page_second(state):
    st.title(":question: Round 2")
    st.write("---")
    st.write("## Instruction")
    st.write("  * answer them questions")
    st.write("---")
    ###

    ### questions
    count=0

    endOfRound=False
    qList=[q for q in bigList if "r2" in q.code.lower()]
    while GetResult(qList[count],count+1):
        state.score[qList[count].code]=qList[count].points
        count+=1
        if count>=len(qList):
            endOfRound=True
            break
    #st.write("debug:",count)

    ### sign off
    if endOfRound:
        st.balloons()
        st.write(" --- ")
        st.write("## End of round 2")
        results=[v for k,v in state.score.items() if "r2" in k]
        st.write("### Round score:",sum(results))
        st.write("### each result:",*results)


#####################
### Results page
#####################
def page_results(state):
    st.title(":smile: Results")
    st.write("---")
    st.write("## Instruction")
    st.write("---")
    ###

    df_results=pd.DataFrame(state.score.items(), columns=["code","points"])
    roundDict={"r1":"one","r2":"two"}
    df_results['round']=df_results['code'].apply(lambda x:roundDict[str(x)[0:2]])
    st.write(df_results)
    resBar=alt.Chart(df_results).mark_bar().encode(
    x='round:O',
    y='sum(points):Q',
    color='round:N'
    ).properties(
    width=600,
    height=400
    )
    st.write(resBar)

#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
