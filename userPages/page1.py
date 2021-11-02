### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### this page
import os
import json
import pandas as pd
import plotly.express as px
import altair as alt
from st_aggrid import AgGrid
import datetime

import random

#####################
### useful functions
#####################

thePeople={
"Sandy":{'init':"SW",'bants':"Your name is Alexander Hamilton!"},
"Hunter":{'init':"IH",'bants':"Staunch!"},
"McCall":{'init':"IM",'bants':"True Dat."},
"Ritchie":{'init':"RT",'bants':"Ritchie T, he tell _no_ lies."},
"Roscoe":{'init':"CR",'bants':""},
"Tony":{'init':"TB",'bants':"Salve Centurion!"},
"Andy":{'init':"AS",'bants':""},
"Gerry":{'init':"GC",'bants':""},
"Kenny":{'init':"KW",'bants':"It's me!"},
"Gilmour":{'init':"SG",'bants':""},
"Dima":{'init':"DM",'bants':"Bastard!"},
"Williams":{'init':"IW",'bants':""},

}

def GetInitials(name):
    return thePeople[name]['init']

def GetDay(name):
    initMap={"Monday":"MON","Tuesday":"TUE","Wednesday":"WED","Thursday":"THU","Friday":"FRI","Saturday":"SAT","Sunday":"SUN"}
    return initMap[name]

instructions=["  * choose your name",
        "  * choose name of who you are submitting for",
        "   * select date",
        "   * select time range",
        "  * add submission string to set",
        "   * copy set and send to Sandy"]

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Build It", ":raised_hands: Build you submission here!", instructions)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        st.write("### :question: Who?")

        nameList=list(thePeople.keys())
        dayList=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        ### set name
        infra.SelectBox(pageDict,'name',nameList,'Select your name:')

        st.write(thePeople[pageDict['name']]['bants'])

        if "nameDay" not in pageDict.keys():
            pageDict['nameDay']=random.choice(dayList)
        st.write("Your submission day this week is:",pageDict['nameDay'])

        behalfList=[x for x in nameList if x!=pageDict['name']]
        infra.SelectBox(pageDict,'behalf',behalfList,'Select who you are submitting for:')

        if "behalfDay" not in pageDict.keys():
            pageDict['behalfDay']=random.choice(dayList)

        st.write(pageDict['behalf']+"\'s submission day this week is:",pageDict['behalfDay'])

        st.write("### :date: When?")

        date = st.date_input('Available date:', datetime.date(2021,12,1))
        time = st.slider("Available times:", value=(datetime.time(12, 00), datetime.time(23, 59)))
        pref = st.selectbox('Preference level:',dayList)


        st.write("### :construction: Build submission...")

        if "subStr" not in pageDict.keys():
            pageDict['subStr']=[]
        # add submitter info.
        thisSub=GetInitials(pageDict['name'])+"."+GetDay(pageDict['nameDay'])
        # add behalf info.
        thisSub+="["+GetInitials(pageDict['behalf'])+"."+GetDay(pageDict['behalfDay'])+"]"
        # add availablity
        thisSub+="."+time[0].strftime("%H.%M")+"-"+time[1].strftime("%H.%M")+"."+GetDay(pref)
        st.write(thisSub)

        if st.button("add this info."):
            st.balloons()
            pageDict['subStr'].append(thisSub)

        st.write("### :point_right: Full submistion")

        if len(pageDict['subStr'])<1:
            st.write("nothing added yet")
        else:
            #st.write("Please copy and send to Sandy when you're done")
            for ss in pageDict['subStr']:
                st.write(ss)
            if st.button("Send to Sandy via whatsapp"):
                st.write("## Of course this doesn't work!")
                st.write("use the bloody doodle poll")
