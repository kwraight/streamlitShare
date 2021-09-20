### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### this page
import streamlit.components.v1 as components
import json
import pandas as pd
import plotly.express as px
import altair as alt
# seed the pseudorandom number generator
from random import seed
from random import randint

#####################
### main part
#####################

class Page3(Page):
    def __init__(self):
        super().__init__("Tests", "Some Scrappy Tests", ['nothing to report'])

    def main(self):
        pageDict=super().main()

        data=[]
        # seed random number generator
        seed(1)
        # generate some random numbers
        for _ in range(100):
            data.append({'alpha':"a_"+str(randint(0,10)),'beta':"b_"+str(randint(0,10)),'gamma':"g_"+str(randint(0,10))})

        df_data=pd.DataFrame(data)
        df_vc=df_data['alpha'].value_counts().reset_index()
        st.dataframe(df_vc)
        st.write(list(zip(df_vc['index'].tolist(),df_vc['alpha'].tolist())))
        valAlpha=st.radio("which?", list(zip(df_vc['index'].tolist(),df_vc['alpha'].tolist())), format_func=lambda x: "{0}:\t\t{1}".format(x[0],x[1]) )

        st.write("results for alpha=",valAlpha[0])
        df_sub=df_data.query('alpha=="'+valAlpha[0]+'"')
        st.dataframe(df_sub['beta'].value_counts().reset_index())
        df_sub_g=pd.DataFrame({'count': df_sub.groupby( ['alpha','beta'] ).size() }).reset_index()


        sun_chart = px.sunburst(df_sub_g, path=['alpha','beta'], values='count',
                      color='count', hover_data=['count'])
        st.plotly_chart(sun_chart)


        info=[[str(x),str(y)] for x,y in zip(df_vc['index'].tolist(),df_vc['alpha'].tolist())]
        colName1="index"
        colName2="alpha"
        st.table(pd.DataFrame(info,columns=[colName1,colName2]))

        components.html("""

        <script src="https://code.jquery.com/jquery-3.6.0.js"></script>
        <script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.24/css/jquery.dataTables.min.css"/>

        <table id="comptypes" class="display" width=" 100%% "></table>

        <script type="text/javascript">

        var dataSet = %(info)s;

        $(document).ready(function() {
        $('#comptypes').DataTable( {
        iDisplayLength: 10,
        data: dataSet,
        columns: [
        { title: '%(colName1)s' },
        { title: '%(colName2)s' }
        ]
        } );
        } );

        </script>

        """ %locals(), height = 1000, scrolling=True)
