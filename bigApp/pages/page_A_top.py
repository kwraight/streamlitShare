### streamlit stuff
import streamlit as st
### general stuff
import os
import sys
from datetime import datetime
### this page
import json
import pandas as pd
import plotly.express as px
###session stuff
cwd = os.getcwd()
sys.path.insert(1, cwd)
import stInfrastructure as infra

#####################
### useful functions
#####################



#####################
### main part
#####################

def main_part(state):
    ### get page name
    pageName=__file__.split('_')[-1].replace('.py','')
    ### title and (optional) instructions
    st.title(":globe_with_meridians: Welcome page")
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

    # debug check
    if state.debug:
        st.write("### Debug is on")

    ### add page attrubute to state
    # st.write([i for i in state.__dict__.keys() if i[:1] != '_'])
    if pageName in [i for i in state.__dict__.keys() if i[:1] != '_']:
        if state.debug: st.write("state."+pageName+" defined")
    else:
        state.__setattr__(pageName,{})
    # st.write([i for i in state.__dict__.keys() if i[:1] != '_'])

    ### getting attribute
    pageDict=state.__getattribute__(pageName)

    st.write("## Hello from top")
