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

#####################
### useful functions
#####################

def MapCol(csvName):
    if "accel" in csvName:
        return {'yTitle':"Accelerator",'legTitle':"Laboratory"}
    elif  "exp" in csvName:
        return {'yTitle':"Experiment",'legTitle':"Machine"}
    elif "labo" in csvName:
        return {'yTitle':"Laboratory",'legTitle':"Location"}
    return None,None

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Listory", "Timelines of HEP Technology", ['nothing to report'])

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ### set data directory
        #st.write(os.getcwd())
        if 'dataDir' not in pageDict.keys():
            pageDict['dataDir']=os.getcwd()+"/data/"
        if st.session_state.debug:
            infra.TextBox(pageDict,'dataDir','directory for data')
        if pageDict['dataDir'][-1]!="/":
            pageDict['dataDir']+="/"

        csvFiles = [f for f in os.listdir(pageDict['dataDir'])] # if os.path.isfile(os.path.join(pageDict['dataDir'], f))]

        if st.session_state.debug:
            st.write("**DEBUG** csv files")
            st.write(csvFiles)

        infra.Radio(pageDict,'csv',csvFiles,"Select data file:")

        df_new=pd.read_csv(pageDict['dataDir']+"/"+pageDict['csv'])

        if st.session_state.debug:
            st.dataframe(df_new)

        ### map column of interest to fileName
        colName=MapCol(pageDict['csv'])

        df_new=df_new.rename(columns=lambda x: x.strip())
        for c in list(df_new.columns):
            try:
                df_new[c]=df_new[c].str.strip()
            except:
                pass

        df_new['End'] = df_new['End'].str.replace(' ', '')
        df_new['End'] = df_new['End'].str.replace('\xa0', '')
        df_new.loc[df_new['End']=="--",'End']="2020"
        df_new.loc[df_new['End']=="",'End']="2020"
        df_new['End']=df_new['End'].fillna(2020)


        df_new.drop(df_new.loc[df_new['Begin']=="TBC"].index, inplace=True)
        df_new['Begin'] = df_new['Begin'].astype('float').astype('Int32') #.astype('Int64')
        df_new['Begin'].loc[df_new['Begin']=='nan']
        df_new = df_new[df_new.Name != 'MIT-Bates Linac']

        df_new['Lifetime']=df_new['End'].astype('int')-df_new['Begin'].astype('int')

        df_new=df_new.sort_values(by=['Begin'])
        df_new['Begin']=pd.to_datetime(df_new['Begin'], format='%Y')
        df_new['End']=pd.to_datetime(df_new['End'], format='%Y')

        df_new.loc[df_new[colName['legTitle']]=="--",colName['legTitle']]="N/A"
        df_new.loc[df_new[colName['legTitle']]=="",colName['legTitle']]="N/A"
        df_new.loc[df_new[colName['legTitle']]==" ",colName['legTitle']]="N/A"


        df_new['Begin'] = df_new['Begin'].astype('datetime64')
        df_new['End'] = df_new['End'].astype('datetime64')

        AgGrid(df_new)
        #st.dataframe(df_new)

        orders = list(df_new[colName['legTitle']])
        fig = px.timeline(df_new
                          , x_start="Begin"
                          , x_end="End"
                          , y="Name"
                          , hover_name=colName['legTitle']
        #                   , facet_col="Dimension"
        #                   , facet_col_wrap=40
        #                   , facet_col_spacing=.99
        #                   , color_discrete_sequence=['green']*len(df)
                          , color_discrete_sequence=px.colors.qualitative.Prism
                          , opacity=.7
        #                   , text="Task"
                          , range_x=None
                          , range_y=None
                          , template='plotly_white'
                          , height=1200
        #                   , width=1500
                          , color=colName['legTitle']
                          #, title ="<b>"+colName['legTitle']+"</b>"
        #                   , color=colors
                         )
        fig.update_layout(
            bargap=0.5
            ,bargroupgap=0.1
            ,xaxis_range=[df_new.Begin.min(), df_new.End.max()]
            ,xaxis = dict(
                showgrid=True
                ,rangeslider_visible=True
                ,side ="top"
                ,tickmode = 'array'
                ,dtick="M1"
                ,tickformat="%Y \n"
                ,ticklabelmode="period"
                ,ticks="outside"
                ,tickson="boundaries"
                ,tickwidth=.1
                ,layer='below traces'
                ,ticklen=20
                ,tickfont=dict(
                    family='Old Standard TT, serif',size=24,color='gray')
                ,rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                    ,x=.37
                    ,y=-.05
                    ,font=dict(
                        family="Arial",
                        size=14,
                        color="darkgray"
            )))

            ,yaxis = dict(
                title= colName['yTitle']
                # ,autorange="reversed"
                ,automargin=True
                # ,anchor="free"
                ,ticklen=10
                ,showgrid=True
                ,showticklabels=True
                ,tickfont=dict(
                    family='Old Standard TT, serif', size=12, color='gray'))

            ,legend=dict(
                orientation="h"
                ,yanchor="bottom"
                ,y=-1
                ,title= colName['legTitle']
                ,xanchor="right"
                ,x=1.5
                ,font=dict(
                    family="Arial"
                    ,size=14
                    ,color="darkgray"))
        )
        fig.update_traces( #marker_color='rgb(158,202,225)'
                           marker_line_color='rgb(8,48,107)'
                          , marker_line_width=1.5, opacity=0.95)
        fig.update_layout(
            #title="<b>"+colName['legTitle']+"</b>",
            xaxis_title="",
        #     margin_l=400,
            yaxis_title=colName['yTitle'],
        #     legend_title="Dimension: ",
            font=dict(
                family="Arial",
                size=24,
                color="darkgray"
            ),
            width=int(1000),
            height=int(2000)
        )
        # fig.show()
        st.plotly_chart(fig)
