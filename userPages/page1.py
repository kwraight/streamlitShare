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

class Page1(Page):
    def __init__(self):
        super().__init__("Charts", ":raised_hands: Some Interactive Charts", instructions)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        if "colours" not in pageDict.keys():
            pageDict['colours']=[]
            for col in ["red","blue","green"]:
                pageDict['colours'].append({'colour':col,'count':0})

        st.write("## Buttons")

        col1, col2, col3 = st.beta_columns([1,1,1])

        with col1:
            st.write(":heart:")
            if st.button('red'):
                next(item for item in pageDict['colours'] if item['colour'] == "red")['count']+=1
        with col2:
            st.write(":blue_heart:")
            if st.button('blue'):
                next(item for item in pageDict['colours'] if item['colour'] == "blue")['count']+=1
        with col3:
            st.write(":green_heart:")
            if st.button('green'):
                next(item for item in pageDict['colours'] if item['colour'] == "green")['count']+=1


        def highlight_row(s):
            for c in ["red","blue","green"]:
                if s.colour == c:
                    return ['color: '+c]*2
            return


        df_cols=pd.DataFrame(pageDict['colours'])

        st.write(df_cols.style.apply(highlight_row, axis=1))


        st.write("## Bar Chart")

        barChart=alt.Chart(df_cols).mark_bar().encode(
        color=alt.Color('colour:N',
          scale=alt.Scale(domain=['red','blue','green'],
                      range=['red','blue','green'])),
                x='colour:N',
                y='count:Q',
                tooltip=['colour:N','count:Q']
            ).properties(width=600).interactive()
        st.altair_chart(barChart)


        st.write("## Pie Chart")

        pieChart=alt.Chart(df_cols).mark_arc().encode(
                theta=alt.Theta(field="count", type="quantitative"),
                color=alt.Color(field="colour", type="nominal",
                  scale=alt.Scale(domain=['red','blue','green'],
                              range=['red','blue','green'])),
                tooltip=['colour:N','count:Q']
                )
        st.altair_chart(pieChart)
