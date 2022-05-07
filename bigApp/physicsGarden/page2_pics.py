### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### Standard
import os
### local
# from .CommonCode import GetTuneListThing
# from .CommonCode import FilterFiles
from .CommonCode import physicsDictList

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Gallery", "Gallery Page", ['nothing to report'])

    def main(self):
        super().main()

        pageDict=st.session_state[self.name]

        pageDict['imgDir']="/somePics/"
        if st.session_state.debug:
            infra.TextBox(pageDict,'imgDir',"Name of image directory:")

        #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        infra.Radio(pageDict,'selName',[x['name'] for x in physicsDictList],"Select source:")
        ### pass code?

        selDict=next(item for item in physicsDictList if item['name'] == pageDict['selName'])
        st.write("### ",selDict['description'])

        for pic in selDict['pics']:
            st.image(pageDict['imgDir']+pic['image'], caption=pic['caption']) #, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
