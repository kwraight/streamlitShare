import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls


df_new=pd.read_csv("data/experiments.csv")

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

df_new['Begin'] = df_new['Begin'].str.replace(' ', '')

df_new['Begin'].loc[df_new['Begin']=='nan']
df_new.drop(df_new.loc[df_new['Begin']=="TBC"].index, inplace=True)

df_new['Begin']=df_new['Begin'].astype('int64')
df_new['End']=df_new['End'].astype('int64')
df_new['Lifetime']=df_new['End']-df_new['Begin']
df_new['Place'] = df_new['Place'].str.replace('\xa0', '')

df_new=df_new.sort_values(by=['Begin'])
df_new['Begin']=pd.to_datetime(df_new['Begin'], format='%Y')
df_new['End']=pd.to_datetime(df_new['End'], format='%Y')

# df_new['Machine'] = df_new['Machine'].str.replace(' ', 'N/A')
# df_new['Machine'] = df_new['Machine'].str.replace('\xa0', 'N/A')
df_new.loc[df_new['Machine']=="--",'Machine']="N/A"
df_new.loc[df_new['Machine']=="",'Machine']="N/A"
df_new.loc[df_new['Machine']==" ",'Machine']="N/A"


df_new['Begin'] = df_new['Begin'].astype('datetime64')
df_new['End'] = df_new['End'].astype('datetime64')


orders = list(df_new['Machine'])
fig = px.timeline(df_new
                  , x_start="Begin"
                  , x_end="End"
                  , y="Experiment"
                  , hover_name="Experiment"
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
                  , color='Experiment'
                  , title ="<b>Experiments</b>"
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
    title="<b>Experiments</b>",
    xaxis_title="",
#     margin_l=400,
    yaxis_title="Experiments",
#     legend_title="Dimension: ",
    font=dict(
        family="Arial",
        size=24,
        color="darkgray"
    )
)
# fig.show()
fig.write_html("experiments.html")
go.FigureWidget(fig)
