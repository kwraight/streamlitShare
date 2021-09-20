### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### Standard
import os

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Music", "Zeroth Page", ['nothing to report'])

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ### pass code?

        ### set tune directory
        #st.write(os.getcwd())
        if 'tuneDir' not in pageDict.keys():
            pageDict['tuneDir']="/code/userPages/music/tunes/"
        if st.session_state.debug:
            infra.TextBox(pageDict,'tuneDir','directory for tunes')
        if pageDict['tuneDir'][-1]!="/":
            pageDict['tuneDir']+="/"

        st.write("checking:",pageDict['tuneDir'])
        try:
            for file in os.listdir(pageDict['tuneDir']):
                #st.write(os.path.join(pageDict['tuneDir'], file))
                if file.endswith(".mp3"):
                    name=os.path.join(pageDict['tuneDir'], file)
                    st.write(name)
                    st.audio(name)
        except FileNotFoundError:
            st.write("no such thing")
            st.stop()
