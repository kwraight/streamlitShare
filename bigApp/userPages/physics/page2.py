### standard
import streamlit as st
from core.ThemePage import Page
### this page
import os
import json
import pandas as pd
import plotly.express as px
import altair as alt
import core.stInfrastructure as infra

#####################
### useful functions
#####################

def MapCol(csvName):
    if "accel" in csvName:
        return "Laboratory"
    elif  "exp" in csvName:
        return "Machine"
    elif "labo" in csvName:
        return "Location"
    return None

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Listory", "Timelines of HEP Technology", ['nothing to report'])

    def main(self):
        pageDict=super().main()

        st.write("### Select data")
        file_path = os.path.realpath(__file__)
        data_path = "/".join(file_path.replace('userPages','data').split("/")[:-1])
        data_path += "/listory"
        st.write("data path:",data_path)

        csvFiles = [f for f in os.listdir(data_path)] # if os.path.isfile(os.path.join(data_path, f))]

        if st.session_state.debug:
            st.write("**DEBUG** csv files")
            st.write(csvFiles)

        infra.SelectBox(pageDict,'csv',csvFiles,"Select data file:")

        df_new=pd.read_csv(data_path+"/"+pageDict['csv'])

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


        df_new['Begin'] = df_new['Begin'].astype('Int64')
        df_new['Begin'].loc[df_new['Begin']=='nan']
        df_new.drop(df_new.loc[df_new['Begin']=="TBC"].index, inplace=True)
        df_new = df_new[df_new.Name != 'MIT-Bates Linac']

        df_new['Lifetime']=df_new['End'].astype('int')-df_new['Begin'].astype('int')

        df_new=df_new.sort_values(by=['Begin'])
        df_new['Begin']=pd.to_datetime(df_new['Begin'], format='%Y')
        df_new['End']=pd.to_datetime(df_new['End'], format='%Y')

        df_new.loc[df_new[colName]=="--",colName]="N/A"
        df_new.loc[df_new[colName]=="",colName]="N/A"
        df_new.loc[df_new[colName]==" ",colName]="N/A"


        df_new['Begin'] = df_new['Begin'].astype('datetime64')
        df_new['End'] = df_new['End'].astype('datetime64')


        orders = list(df_new[colName])
        fig = px.timeline(df_new
                          , x_start="Begin"
                          , x_end="End"
                          , y=colName
                          , hover_name=colName
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
                          , color=colName
                          , title ="<b>"+colName+"</b>"
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
                title= ""
                ,autorange="reversed"
                ,automargin=True
        #         ,anchor="free"
                ,ticklen=10
                ,showgrid=True
                ,showticklabels=True
                ,tickfont=dict(
                    family='Old Standard TT, serif', size=16, color='gray'))

            ,legend=dict(
                orientation="h"
                ,yanchor="bottom"
                ,y=1.1
                ,title=""
                ,xanchor="right"
                ,x=1
                ,font=dict(
                    family="Arial"
                    ,size=14
                    ,color="darkgray"))
        )
        fig.update_traces( #marker_color='rgb(158,202,225)'
                           marker_line_color='rgb(8,48,107)'
                          , marker_line_width=1.5, opacity=0.95)
        fig.update_layout(
            title="<b>"+colName+"</b>",
            xaxis_title="",
        #     margin_l=400,
            yaxis_title=colName,
        #     legend_title="Dimension: ",
            font=dict(
                family="Arial",
                size=24,
                color="darkgray"
            )
        )
        # fig.show()
        st.plotly_chart(fig)
