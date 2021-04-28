import streamlit as st
###
from urllib import request
import json
from annotated_text import annotated_text, annotation
###
import stInfrastructure as infra

#####################
### Check state page
#####################
def display_state_values(state):

    st.write("## All data")
    st.write("Debug setting:", state.debug)
    st.write("---")

    # debug check
    if state.debug:
        st.write("### Debug is on")

    # check page info. defined
    if "broom" in [i for i in state.__dict__.keys() if i[:1] != '_']:
        if state.debug: st.write("state.broom defined")
    else:
        state.broom={}


    # ### register
    # st.write("**Register** information")
    # infra.ToggleButton(state.broom,'showReg',"Show *register* information")
    # if state.broom['showReg']:
    #     try:
    #         st.write(state.register)
    #     except AttributeError:
    #         st.write("No data defined")
    # ### upload
    # st.write("**Upload** information")
    # infra.ToggleButton(state.broom,'showUp',"Show *upload* information")
    # if state.broom['showUp']:
    #     try:
    #         st.write(state.upload)
    #     except AttributeError:
    #         st.write("No data defined")
    ### broom
    st.write("**Debug** information")
    infra.ToggleButton(state.broom,'showDebug',"Show *debug* information")
    if state.broom['showDebug']:
        try:
            st.write(state.broom)
        except AttributeError:
            st.write("No data defined")
    ### debug


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

    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        try:
            del state.authenticate
        except AttributeError:
            pass
        try:
            del state.register
        except AttributeError:
            pass
        try:
            del state.plot
        except AttributeError:
            pass
        try:
            del state.upload
        except AttributeError:
            pass
        try:
            del state.delete
        except AttributeError:
            pass
        try:
            del state.batch
        except AttributeError:
            pass
        try:
            del state.check
        except AttributeError:
            pass


    EasterEgg(state)
