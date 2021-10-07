### standard
import streamlit as st
from core.Page import Page
### custom

#####################
### main part
#####################

class Page0(Page):
    def __init__(self):
        super().__init__("Welcome", "Simple webApp", ['nothing to report'])

    def main(self):
        super().main()

        #pageDict=st.session_state[self.name]

        st.write("Plots of some physics information")
