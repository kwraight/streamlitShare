import pandas as pd
import numpy as np
from datetime import datetime
### streamlit stuff
import streamlit as st
### plotly
import plotly.express as px
import plotly.graph_objects as go
### datapane
import datapane as dp
### infrastructure
import infrastructure

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
        "Debug": page_debug,
    }

    ### sidebar
    st.sidebar.title(":smile: Basic WebApp")
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
        st.dataframe(state.allData.tail())
        st.write("data set size:",len(state.allData.index))
    except AttributeError:
        st.write("No data selected")

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
    st.title(":dragon: Overview page")
    st.write("---")
    st.write("## Instructions")
    st.write("---")
    ###

    if state.debug:
        st.write("debug is on")


#####################
### First page
#####################
def page_first(state):
    st.title(":question: first page")
    st.write("---")
    st.write("## Instruction")
    st.write("---")
    ###

    if state.debug:
        st.write("debug is on")


#####################
### Second page
#####################
def page_second(state):
    st.title(":question: second page")
    st.write("---")
    st.write("## Instruction")
    st.write("---")
    ###

    if state.debug:
        st.write("debug is on")


#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
