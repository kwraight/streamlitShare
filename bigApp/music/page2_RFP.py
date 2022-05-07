### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### Standard
import os
### local
from .CommonCode import GetTuneListThing
from .CommonCode import FilterFiles

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("RFP", "Robert Foster Project", ['nothing to report'])

    def main(self):
        super().main()

        pageDict=st.session_state[self.name]

        dictKey="RFP"
        ### pass code?
        st.write("### ",GetTuneListThing(dictKey,'description'))

        ### set tune directory
        #st.write(os.getcwd())
        if 'tuneDir' not in pageDict.keys():
            pageDict['tuneDir']="/code/userPages/music/tunes/"
        if st.session_state.debug:
            infra.TextBox(pageDict,'tuneDir','directory for tunes')
        if pageDict['tuneDir'][-1]!="/":
            pageDict['tuneDir']+="/"

        tuneList=GetTuneListThing(dictKey,'tunes')

        if st.session_state.debug:
            st.write("checking:",pageDict['tuneDir'])
            st.write("looking for",tuneList)

        fileList=FilterFiles(pageDict['tuneDir'],tuneList)

        count=1
        for e,f in enumerate(fileList,1):
            st.write("### "+str(e)+".",f['short'])
            st.audio(f['name'])
