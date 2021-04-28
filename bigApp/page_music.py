### streamlit stuff
import streamlit as st
### general stuff
import os
import sys
from datetime import datetime
### this page
import json
import pandas as pd
#
import stInfrastructure as infra

#####################
### useful functions
#####################



#####################
### main part
#####################

def main_part(state):
    st.title(":globe_with_meridians: music page")
    st.write("## Kené's pages")
    st.write("---")
    if state.debug:
        st.write("## Instructions")
        st.write("1. Input data (formatted *json*)")
        st.write(" * select file --> all data will be shown in dataframe")
        st.write(" * click *Add dataSet*")
        st.write("---")
    else:
        st.write(" * toggle debug for details")
        st.write("---")
    ###

    # check page info. defined
    if "music" in [i for i in state.__dict__.keys() if i[:1] != '_']:
        if state.debug: st.write("state.music defined")
    else:
        state.music={}

    infra.TextBox(state.music, "passcode", "Enter passcode", True)

    try:
        if state.music['passcode']!="tickles":
            st.write("Passcode incorrect")
            st.stop()
    except KeyError:
        st.write("awaiting passcode")
        st.stop()

    st.write("Passcode correct!")
    st.balloons()

    audioPath="/Users/kwraight/Music/GarageBand/mp3_versions"
    _, _, filenames = next(os.walk(audioPath))
    if len(filenames)<1:
        st.write("no files found")
        st.stop()
    #st.write(os.path.isfile(audioFile))
    for f in filenames:
        if ".mp3" not in f: continue
        st.write("Here's a tune...",f)
        st.audio(audioPath+"/"+f)
