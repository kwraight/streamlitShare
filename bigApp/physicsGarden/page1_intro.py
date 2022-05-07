### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### Standard
import os
### local
from .CommonCode import physicsDictList

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Intro", "Intro", ['nothing to report'])

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ### pass code?

        ### set tune directory
        st.write("## Welcome to the Physics Garden")
        st.write("An exhibition of Garden Physics")
        st.write("### Forces")
        for e,td in enumerate(physicsDictList,1):
            st.write("### "+str(e)+".",td['name'],"-",str(len(td['pics'])),"pictures")
