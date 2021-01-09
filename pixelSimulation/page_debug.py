import streamlit as st
import stInfrastructure as infra
###
from urllib import request
import json
from annotated_text import annotated_text, annotation

#####################
### Check state page
#####################
def display_state_values(state):
    st.write("## All data")
    st.write("Debug setting:", state.debug)
    st.write("---")

    ## state
    st.write("## state")
    try:
        st.write(vars(state))
    except:
        st.write("No state defined")

    try:
        st.write("#dataSets:",len(state.simResults))
        for sr in state.simResults:
            st.write(sr)
        remSel = st.selectbox("Select dataset index for removal?", [x for x in range(0,len(state.simResults),1)])
        if st.button("Remove dataset"):
            del state.simResults[remSel]
    except AttributeError:
        st.write("no simulation results")


### get API response from endpoint
def GetResponse(endStr):
    api_endpoint = endStr
    api_response = json.load(request.urlopen(api_endpoint))
    return api_response


def EasterEgg(state):
    ### wee bit of fun
    if state.debug:
        st.write(":egg: Easter Egg")
        if st.button("Get a quote"):
            quote=GetResponse("https://favqs.com/api/qotd")
            if quote:
                annotated_text(
                (quote['quote']['body'],"","#8ef"),
                "\n",
                (quote['quote']['author'],"","#afa"),
                )


def main_part(state):
    st.title(":wrench: Broom cupboard")
    st.write("---")
    st.write("## Bits and bobs for maintainance")
    st.write("---")

    if state.debug:
        st.error("Debug is on")

    display_state_values(state)

    # st.write("## :exclamation: Clear all state settings")
    # if st.button("Clear state"):
    #     state = infra.get()

    EasterEgg(state)
