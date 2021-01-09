import streamlit as st
import stInfrastructure as infra
### data manipulation
import pandas as pd
import json
from measurement.measures import Weight, Volume
### general
import os
import sys
import re

#####################
### Next page
#####################

### main part
def main_part(state):
    st.title(":microscope: Select Simulation Parameters")
    st.write("---")
    if state.debug:
        st.write(" * set number of pixels")
        st.write(" * set relative beam width")
        st.write(" * set relative charge sharing")
        st.write(" * set relative THL")
        st.write(" * set chip mode")
    else:
        st.write(" * toggle debug (LHS) for details")
    st.write("---")
    ###

    # debug check
    if state.debug:
        st.error("Debug is on")

    st.write("## Standards")
    st.write("All sizes relative to pixel length: 1 unit")

    # Number of pixels
    st.write("## Select number of Pixels")
    numPix=st.slider("Number of pixels", min_value=1, max_value=5, value=3, step=1)

    ## select beam width
    st.write("## Beam sigma (relative to pixel width)")
    beamWidth=st.slider("Width of beam", min_value=0.01, max_value=1.0, value=0.09, step=0.01)

    ## select charge sharing
    st.write("## Charge sharing (relative to pixel width)")
    chargeSharing=st.slider("Charge sharing", min_value=0.01, max_value=1.0, value=0.18, step=0.01)

    ## select threshold
    st.write("## Threshold (relative to input charge)")
    threshold=st.slider("Threshold", min_value=0.01, max_value=1.0, value=0.5, step=0.01)

    ## select chip mode
    st.write("## chip mode")
    st.write("* mpx: medipix like mode (hit counting)")
    st.write("* tpx: timepix like mode (charge integrating)")
    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    chipMode=st.radio("chip mode", ["mpx","tpx"], index=0)

    ## set output name
    st.write("## Output name")
    try:
        if name[-3:]=="mpx" and chipMode=="tpx":
            name=name[:-3]+"tpx"
        if name[-3:]=="tpx" and chipMode=="mpx":
            name=name[:-3]+"mpx"
        name=st.text_input("Output name", value=name, max_chars=20)
    except:
        name=st.text_input("Output name", value='simOut_Npix'+str(numPix)+'_'+chipMode, max_chars=20)

    ## ready
    st.write("### Set Ready")
    if state.debug:
        st.write({'numPix':numPix,'beamWidth':beamWidth,'chargeSharing':chargeSharing,'threshold':threshold,'chipMode':chipMode,'name':name})
    if st.button("set ready"):
        state.ready=True
        state.numPix=numPix
        state.beamWidth=beamWidth
        state.chargeSharing=chargeSharing
        state.threshold=threshold
        state.chipMode=chipMode
        state.name=name
    try:
        if state.ready==False:
            st.write("Simulation is not set ready")
        else:
            st.write("Simulation is ready. Run from sidebar")
    except AttributeError:
        state.ready=False
