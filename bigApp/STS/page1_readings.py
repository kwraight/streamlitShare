### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### Standard
import os
import base64

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Readings", "Zeroth Page", ['nothing to report'])

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ### set papers directory
        #st.write(os.getcwd())
        if 'readDir' not in pageDict.keys():
            pageDict['readDir']="/code/userPages/STS/readings/"
        if st.session_state.debug:
            infra.TextBox(pageDict,'readDir','directory for papers')
        if pageDict['readDir'][-1]!="/":
            pageDict['readDir']+="/"

        st.write("checking:",pageDict['readDir'])
        readDict={}
        try:
            for file in os.listdir(pageDict['readDir']):
                #st.write(os.path.join(pageDict['readDir'], file))
                if file.endswith(".pdf"):
                    name=os.path.join(pageDict['readDir'], file)
                    readDict[file]=name
                    #st.write(name)
        except FileNotFoundError:
            st.write("no such thing")
            st.stop()
        infra.SelectBox(pageDict,'pdfPick',list(readDict.keys()),'Select pdf')
        st.write("Picked:",pageDict['pdfPick'])
        if st.button("Show pdf"):
            with open(readDict[pageDict['pdfPick']],"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        try:
            st.markdown(pdf_display, unsafe_allow_html=True)
        except UnboundLocalError:
            st.write("no pdf set")
