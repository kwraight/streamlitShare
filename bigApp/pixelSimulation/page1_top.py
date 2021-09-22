### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
###
import datetime
import os
import sys

#####################
### useful functions
#####################

### format datetime
def DateFormat(dt):
return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Top", "Simple pixel detecter 1D simulation", ['In mathematics, an automorphic number (sometimes referred to as a circular number) is a natural number in a given number base b whose square "ends" in the same digits as the number itself.','(see)["https://en.wikipedia.org/wiki/Automorphic_number"]'])

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        st.write("### Select page from lefthand side bar")
        st.write("  * Top Page(here): select measurement scale")
        st.write("  * Set Parameters: Set simulation recipe: number pixels, charge sharing, beam width, threshold")
        st.write("  * Broom Cupboard: Boring debugging stuff")

        if st.session_state.debug:
            st.error("Debug is on")
            st.write("Current directory:",os.getcwd())
            st.write(os.listdir())

        ##
        st.write("### Activate simulation from sidebar")
