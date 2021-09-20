### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### Standard
import os
import base64
import numpy as np
import pandas as pd
import altair as alt

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Readings", "Zeroth Page", ['In mathematics, an automorphic number (sometimes referred to as a circular number) is a natural number in a given number base b whose square "ends" in the same digits as the number itself.','(see)["https://en.wikipedia.org/wiki/Automorphic_number"]'])

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ### pass code?

        power=st.multiselect("Pick a power:",[x for x in range(1,10,1)])
        upto=st.radio("Pick range to check (up to):",[1000,10000,100000,1000000])
        plsmns=st.selectbox("Neighbours (+/-):",[x for x in range(0,10,1)])
        tallyList=[]
        if st.button("Get results!"):
            st.write("power ==",power)
            st.write("up to ==",upto)
            #tallyDict[power]={}
            for p in power:
                for y in range(plsmns*-1,plsmns+1,1):
                    #st.write("this is neighbour",y)
                    for x in range(0,upto,1):
                        if str(np.power(x,p))[-1*len(str(x))::]==str(x+y):
                            #st.write(x," : ",np.power(x,power),"...",y)
                            tallyList.append({'power':int(p),'neighbour':int(y),'n':int(x)})
                            #st.write(tallyList[-1])
        if len(tallyList)<1:
            st.stop()
        #st.write(tallyList)
        df_tally=pd.DataFrame(tallyList)
        df_tally_g=df_tally.groupby(["power","neighbour"]).count().reset_index()
        st.dataframe(df_tally_g)
        #df_tally_g=df_tally.groupby(["power","neighbour"]).count().reset_index()
        #st.dataframe(df_tally_g)
        myChart=alt.Chart(df_tally_g).mark_bar(size=20).encode(
                    x=alt.X('power:N'),
                    y=alt.Y('n'),
                    color='power:N',
                    column='neighbour:N',
                    tooltip=['power', 'neighbour', 'n']
        ).configure_legend(labelLimit= 0, symbolLimit=0)#.properties(width=800)
        st.altair_chart(myChart)
