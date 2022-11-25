import streamlit as st
###
from urllib import request
import json
from annotated_text import annotated_text, annotation
import importlib
import os
import stInfrastructure as infra

################
### Useful functions
################

def display_state_values():

    st.write("## All data")
    st.write("Debug setting:", st.session_state.debug)
    st.write("---")

    # debug check
    if st.session_state.debug:
        st.write("### Debug is on")

    # check page info. defined
    if "Broom Cupboard" in [i for i in st.session_state.keys()]:
        if st.session_state.debug: st.write("st.session_state['Broom Cupboard'] defined")
    else:
        st.session_state['Broom Cupboard']={}

    myKeys=[x for x in st.session_state.keys()]
    st.write(myKeys)
    for mk in myKeys:
        if mk=="debug": continue
        st.write(f"**{mk}** information")
        infra.ToggleButton(st.session_state['Broom Cupboard'],'show_'+mk,f"Show *{mk}* information")
        if st.session_state['Broom Cupboard']['show_'+mk]:
            st.write(st.session_state[mk])


### get API response from endpoint
def GetResponse(endStr):
    api_endpoint = endStr
    api_response = json.load(request.urlopen(api_endpoint))
    return api_response


def EasterEgg():
    ### wee bit of fun
    if st.session_state.debug:
        st.write(":egg: Easter Egg")
        if st.button("Get a quote"):
            quote=GetResponse("https://favqs.com/api/qotd")
            if quote:
                annotated_text(
                (quote['quote']['body'],"","#8ef"),
                "\n",
                (quote['quote']['author'],"","#afa"),
                )


    ## scale
    st.write("## Measurement scale")
    try:
        if state.scale=="metric":
            st.write("*Metric* is selected.")
            st.write("Vive la republic!")
        elif state.scale=="imperial":
            st.write("*Imperial* is selected.")
            st.write("Old school!")
        else:
            st.write("Awaiting a weighting")
    except AttributeError:
        st.write("Awaiting a weighting")

### get API response from endpoint
def GetResponse(endStr):
    api_endpoint = endStr
    api_response = json.load(request.urlopen(api_endpoint))
    return api_response


def EasterEgg():
    ### wee bit of fun
    if st.session_state.debug:
        st.write(":egg: Easter Egg")
        if st.button("Get a quote"):
            quote=GetResponse("https://favqs.com/api/qotd")
            if quote:
                annotated_text(
                (quote['quote']['body'],"","#8ef"),
                "\n",
                (quote['quote']['author'],"","#afa"),
                )


def ReadRequirements():
    try:
        with open(os.getcwd()+"/requirements.txt") as req:
            st.write("From requirements...")
            for line in req.readlines():
                st.write(line.strip())
    except FileNotFoundError:
        st.write("No requirements file found.")

def CheckModule(name):
    try:
        i = importlib.import_module(name)
        st.write("module '"+name+"' version:",i.__version__)
    except ModuleNotFoundError:
        st.write("module '"+name+"' not found")
    except AttributeError:
        st.write("module '"+name+"' has no version to read")


###################
### main part
###################

def main_part(state):
    st.title(":wrench: Broom cupboard")
    st.write("---")
    st.write("## Bits and bobs for maintainance")
    st.write("---")

    if st.session_state.debug:
        st.error("Debug is on")

    display_state_values()

    # st.write("## :exclamation: Clear all state settings")
    # if st.button("Clear state"):
    #     state.clear()

    EasterEgg()

    st.write("---")

    st.write("### Module checks")
    mod=st.text_input("Check module version:",value="streamlit")
    CheckModule(mod)
    if st.button("Check requirements file?"):
        ReadRequirements()
