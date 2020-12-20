import streamlit as st
import stInfrastructure as infra
### data manipulation
import pandas as pd
import json
### general
import os
import sys

#####################
### Next page
#####################

### main part
def main_part(state):
    st.title(":microscope: Conversions")
    st.write("---")
    st.write("## Get the measure of your measure")
    if state.debug:
        st.write("  * select from")
        st.write("  * select to")
        st.write("  * scaling")
    else:
        st.write(" * toggle debug for details")
    st.write("---")
    ###

    # debug check
    if state.debug:
        st.write("### Debug is on")
