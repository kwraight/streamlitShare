### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### data manipulation
import pandas as pd
import json
from measurement.measures import Weight, Volume
### general
import os
import sys
import re

instructions=[" * set number of pixels",
            " * set relative beam width",
            " * set relative charge sharing",
            " * set relative THL",
            " * set chip mode"]

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Setup", ":microscope: Select Simulation Parameters", instructions)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        # debug check
        if st.session_state.debug:
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
        if st.session_state.debug:
            st.write({'numPix':numPix,'beamWidth':beamWidth,'chargeSharing':chargeSharing,'threshold':threshold,'chipMode':chipMode,'name':name})
        if st.button("set ready"):
            page['ready']=True
            page['numPix']=numPix
            page['beamWidth']=beamWidth
            page['chargeSharing']=chargeSharing
            page['threshold']=threshold
            page['chipMode=']chipMode
            page['name']=name
        try:
            if st.session_state.ready==False:
                st.write("Simulation is not set ready")
            else:
                st.write("Simulation is ready. Run from sidebar")
        except KeyError:
            page['ready']=False
