### standard
import streamlit as st
from core.ThemePage import Page
### custom

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Page1", "Zeroth Page", ['nothing to report'])

    def main(self):
        super().main()

        #pageDict=st.session_state[self.name]

        st.write("Content to be added xxx")