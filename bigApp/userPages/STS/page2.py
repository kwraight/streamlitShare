### standard
import streamlit as st
from core.ThemePage import Page
### custom

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Some Sorts", "Zeroth Page", ['nothing to report'])

    def main(self):
        super().main()

        #pageDict=st.session_state[self.name]

        st.write("## Hello from STS")
