import pandas as pd
import numpy as np
import datetime
### streamlit stuff
import streamlit as st
### plotly
import plotly.express as px
import plotly.graph_objects as go
### altair
import altair as alt
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
        return q.points
    elif "< PICK A VALUE >" in ans:
        return -1
    else:
        return 0

def RoundSummary(score, num):
    st.balloons()
    st.write(" --- ")
    st.write("## End of round "+str(num))
    results=[v for k,v in score.items() if "r"+str(num) in k]
    st.write("### Round score:",sum(results))
    st.write("### each result:",*results)


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
        "Round 1: TBC": page_one,
        "Round 2: TBC": page_two,
        "Round 3: TBC": page_three,
        "Round 4: TBC": page_four,
        "Results": page_results,
        "Broom cupboard": page_debug,
    }

    ### sidebar
    st.sidebar.title(":smile: Quiz WebApp")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Select your page:", tuple(pages.keys()))

    ### mini-state summary
    # if st.sidebar.button("State Summary"):
    #     try:
    #         st.sidebar.markdown("data set size: "+str(len(state.allData.index)))
    #     except:
    #         st.sidebar.markdown("No data yet selected")

    ### debug toggle
    st.sidebar.markdown("---")
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
    st.title(":wrench: Broom cupboard")
    st.write("---")
    st.write("Bits and bobs for maintainance:")
    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        state.clear()


#####################
### Top page
#####################
def page_top(state):
    nowTime = datetime.datetime.now()
    st.write("""## :fireworks: Welcome to **The Great *Ritchie T* Quiz ** :fireworks: """)
    st.write("""**NB** Satisfaction is not supported in the current version.""")
    st.write("""### :calendar: ("""+DateFormat(nowTime)+""")""")
    st.write(" --- ")
    ###

    st.write("Four rounds of questions to measure your post-lockdown concentration.")
    for r,c in zip(["one", "two", "three", "four"],["r1","r2","r3","r4"]):
        st.write("  * Round "+r+": "+str(len([q for q in bigList if c in q.code]))+" questions")

    if st.button("Ready?"):
        state.score={}
        st.write("Then move *yer arse*")

    if state.debug:
        st.write("score:",sum(state.score.values()))
        st.write("score per question:",*state.score.values())

#####################
### First round
#####################
def page_one(state):
    st.title(":question: Round 1")
    st.write("---")
    st.write("## Instructions")
    st.write("  * answer them questions")
    st.write("---")
    ###

    ### check score exists
    try:
        len(state.score.values())
    except:
        state.score={}
    ### questions
    count=0
    endOfRound=False
    qList=[q for q in bigList if "r1" in q.code.lower()]
    if len(qList)>0:
        points=GetResult(qList[count],count+1)
        while points>-1:
            state.score[qList[count].code]=points
            if state.debug: st.write("""### points: """+str(points))
            count+=1
            if count>=len(qList):
                endOfRound=True
                break
            points=GetResult(qList[count],count+1)
        #st.write("debug:",count)
    else:
        st.write("No questions here.")

    ### sign off
    if endOfRound:
        RoundSummary(state.score,1)


#####################
### Second round
#####################
def page_two(state):
    st.title(":question: Round 2")
    st.write("---")
    st.write("## Instructions")
    st.write("  * answer them questions")
    st.write("---")
    ###

    ### check score exists
    try:
        len(state.score.values())
    except:
        state.score={}
    ### questions
    count=0
    endOfRound=False
    qList=[q for q in bigList if "r2" in q.code.lower()]
    if len(qList)>0:
        points=GetResult(qList[count],count+1)
        while points>-1:
            state.score[qList[count].code]=points
            if state.debug: st.write("""### points: """+str(points))
            count+=1
            if count>=len(qList):
                endOfRound=True
                break
            points=GetResult(qList[count],count+1)
        #st.write("debug:",count)
    else:
        st.write("No questions here.")

    ### sign off
    if endOfRound:
        RoundSummary(state.score,2)

#####################
### Third round
#####################
def page_three(state):
    st.title(":question: Round 3")
    st.write("---")
    st.write("## Instructions")
    st.write("  * answer them questions")
    st.write("---")
    ###

    ### check score exists
    try:
        len(state.score.values())
    except:
        state.score={}
    ### questions
    count=0
    endOfRound=False
    qList=[q for q in bigList if "r3" in q.code.lower()]
    if len(qList)>0:
        points=GetResult(qList[count],count+1)
        while points>-1:
            state.score[qList[count].code]=points
            if state.debug: st.write("""### points: """+str(points))
            count+=1
            if count>=len(qList):
                endOfRound=True
                break
            points=GetResult(qList[count],count+1)
        #st.write("debug:",count)
    else:
        st.write("No questions here.")

    ### sign off
    if endOfRound:
        RoundSummary(state.score,3)

#####################
### Fourth round
#####################
def page_four(state):
    st.title(":question: Round 4")
    st.write("---")
    st.write("## Instructions")
    st.write("  * answer them questions")
    st.write("---")
    ###

    ### check score exists
    try:
        len(state.score.values())
    except:
        state.score={}
    ### questions
    count=0
    endOfRound=False
    qList=[q for q in bigList if "r4" in q.code.lower()]
    if len(qList)>0:
        points=GetResult(qList[count],count+1)
        while points>-1:
            state.score[qList[count].code]=points
            if state.debug: st.write("""### points: """+str(points))
            count+=1
            if count>=len(qList):
                endOfRound=True
                break
            points=GetResult(qList[count],count+1)
        #st.write("debug:",count)
    else:
        st.write("No questions here.")

    ### sign off
    if endOfRound:
        RoundSummary(state.score,4)

#####################
### Results page
#####################
def page_results(state):
    st.title(":bar_chart: Results")
    st.write("---")
    st.write("## Visual data delights :cake:")
    st.write("---")
    ###

    ### check score exists
    try:
        len(state.score.values())
    except:
        state.score={}
    ### make dataframe from results
    df_results=pd.DataFrame(state.score.items(), columns=["code","points"])
    roundDict={"r1":"one","r2":"two"}
    # define rounds
    df_results['round']=df_results['code'].apply(lambda x:roundDict[str(x)[0:2]])
    st.write(df_results)
    ### bar chart of results per round
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
