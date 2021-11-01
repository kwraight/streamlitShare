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

        st.write("By popular demand, here's a helpful app to build your Christmas schedule submission.")
        st.write("Simply go to the _Build It_ page and make your dreams come true!")
