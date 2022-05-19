### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### this page
import os
import json
import pandas as pd
import plotly.express as px
import altair as alt
from st_aggrid import AgGrid
import datetime

import random

#####################
### useful functions
#####################

instructions=[]

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Number Blocks", ":raised_hands: Some Maths Stuff", instructions)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        st.write("## to-do")
