### standard
import streamlit as st
from core.Page import Page
### custom

#####################
### main part
#####################

class Page0(Page):
    def __init__(self):
        super().__init__("Welcome", ":christmas_tree: Joyous Christmas webApp", ['nuffin to say'])

    def main(self):
        super().main()

        #pageDict=st.session_state[self.name]

        st.write(":bell: By popular demand, here's yer Christmas night-oot app.")
        st.write(":bell: Simply go to the _Night Out_ page and make your dreams come true!")
