import streamlit as st
import pandas as pd
import altair as alt

#####################
### Accelerators
#####################
def main_part(state):
    st.title(":boom: Accelerators")
    st.write("---")
    st.write("## Information")
    st.write("  * Non-comprehensive list of PP experiments")
    st.write("---")
    ###

    df_new=pd.read_csv(state.cwd+"/listory/data/accelerators.csv")

    df_new=df_new.rename(columns=lambda x: x.strip())
    df_new=df_new.rename(columns={"Location": "Laboratory"})
    st.write(df_new)
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

    df_new.loc[df_new['Laboratory']=="--",'Laboratory']="N/A"
    df_new.loc[df_new['Laboratory']=="",'Laboratory']="N/A"
    df_new.loc[df_new['Laboratory']==" ",'Laboratory']="N/A"
    if state.debug: st.write(list(df_new['Laboratory'].unique()))

    st.dataframe(df_new)
    if state.debug:
        st.write(list(df_new.columns))
        st.write(df_new.dtypes)

    timePlot=alt.Chart(df_new).mark_bar().encode(
    x=alt.X('Begin',scale=alt.Scale(zero=False), title='When'),
    x2='End',
    y=alt.Y('Name',sort='-x',title='Who'),
    color='Laboratory',
    #column='Place',
    tooltip=['Lifetime', 'Laboratory']
    ).properties(width=800)

    st.altair_chart(timePlot)
