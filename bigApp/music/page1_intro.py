### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### Standard
import os
### local
from .CommonCode import tuneDictList

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
        st.write("## Welcome to the tune dump")
        st.write("A repository of audio frustrations based on [GarageBand](https://www.apple.com/uk/mac/garageband/), [Komplete Audio 6](https://www.native-instruments.com/en/products/komplete/audio-interfaces/komplete-audio-6/) and various instruments.")
        st.write("### Play List")
        for e,td in enumerate(tuneDictList,1):
            st.write("### "+str(e)+".",td['name'],"-",str(len(td['tunes'])),"tunes")
