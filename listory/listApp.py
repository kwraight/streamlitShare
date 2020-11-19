import pandas as pd
import numpy as np
import datetime
### streamlit stuff
import streamlit as st
### altair
import altair as alt
# particular
import infrastructure as infra
import os
cwd = os.getcwd()

################
### Useful functions
################
### set selection default value
DEFAULT = '< PICK A VALUE >'
def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
    func = st.sidebar.selectbox if sidebar else st.selectbox
    return func(text, np.insert(np.array(values, object), 0, default))

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))


#####################
### main
#####################
def main():
    ### get state variable
    state = infra._get_state()

    ### define pages dictionary
    pages = {
        "Top Page": page_top,
        "Experiments": page_exp,
        "Accelerators": page_acc,
        "Laboratories": page_lab,
        "Broom cupboard": page_debug,
    }

    ### sidebar
    st.sidebar.title(":telescope: Listory WebApp")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Select your page:", tuple(pages.keys()))

    ### mini-state summary
    # if st.sidebar.button("State Summary"):
    #     try:
    #         st.sidebar.markdown("data set size: "+str(len(state.allData.index)))
    #     except:
    #         st.sidebar.markdown("No data yet selected")

    ### debug toggle
    st.sidebar.markdown("---")
    debug = st.sidebar.checkbox("Toggle debug")
    if debug:
        state.debug=True
    else: state.debug=False

    ### display  selected page using state variable
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


#####################
### Check state page
#####################
def display_state_values(state):

    st.write("## All data")
    st.write("Debug setting:", state.debug)
    # try:
    #     st.write(state.score)
    #     df_results=pd.DataFrame(state.score.items(), columns=["code","points"])
    #     st.write(df_results)
    # except AttributeError:
    #     st.write("No data available")

def page_debug(state):
    st.title(":wrench: Broom cupboard")
    st.write("---")
    st.write("Bits and bobs for maintainance:")
    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        state.clear()


#####################
### Top page
#####################
def page_top(state):
    nowTime = datetime.datetime.now()
    st.write("""## :fireworks: **Listory App** :fireworks: """)
    st.write("""### :calendar: ("""+DateFormat(nowTime)+""")""")
    st.write(" --- ")
    ###

    st.write("TBC: select files")

    if state.debug:
        st.write("Debug is on")
        st.write("Current directory:",cwd)


#####################
### Experiments
#####################
def page_exp(state):
    st.title(":boom: Experiments")
    st.write("---")
    st.write("## Information")
    st.write("  * Non-comprehensive list of PP experiments")
    st.write("---")
    ###

    df_new=pd.read_csv(cwd+"/data/experiments.csv")

    df_new['End'] = df_new['End'].str.replace(' ', '')
    df_new['End'] = df_new['End'].str.replace('\xa0', '')
    df_new.loc[df_new['End']=="--",'End']="2020"
    df_new.loc[df_new['End']=="",'End']="2020"
    if state.debug: st.write(df_new['End'].unique())

    df_new['Begin'] = df_new['Begin'].str.replace(' ', '')
    if state.debug: st.write(df_new['Begin'].unique())

    df_new['Begin'].loc[df_new['Begin']=='nan']
    df_new.drop(df_new.loc[df_new['Begin']=="TBC"].index, inplace=True)

    df_new['Begin']=df_new['Begin'].astype('int64')
    df_new['End']=df_new['End'].astype('int64')
    df_new['Lifetime']=df_new['End']-df_new['Begin']
    df_new['Place'] = df_new['Place'].str.replace('\xa0', '')

    df_new=df_new.sort_values(by=['Begin'])
    df_new['Begin']=pd.to_datetime(df_new['Begin'], format='%Y')
    df_new['End']=pd.to_datetime(df_new['End'], format='%Y')

    st.dataframe(df_new)

    timePlot=alt.Chart(df_new).mark_bar().encode(
    x=alt.X('Begin',scale=alt.Scale(zero=False), title='When'),
    x2='End',
    y=alt.Y('Experiment',sort='-x',title='Who'),
    color='Place',
    #column='Place'
    ).properties(width=800)

    st.write(timePlot)

#####################
### Accelerators
#####################
def page_acc(state):
    st.title(":boom: Accelerators")
    st.write("---")
    st.write("## Information")
    st.write("  * Non-comprehensive list of PP experiments")
    st.write("---")
    ###

    df_new=pd.read_csv(cwd+"/data/accelerators.csv")

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

    st.dataframe(df_new)

    timePlot=alt.Chart(df_new).mark_bar().encode(
    x=alt.X('Begin',scale=alt.Scale(zero=False), title='When'),
    x2='End',
    y=alt.Y('Name',sort='-x',title='Who'),
    color='Location',
    #column='Place'
    ).properties(width=800)

    st.write(timePlot)

#####################
### Laboratories
#####################
def page_lab(state):
    st.title(":boom: Laboratories")
    st.write("---")
    st.write("## Information")
    st.write("  * Non-comprehensive list of PP experiments")
    st.write("---")
    ###

    df_new=pd.read_csv(cwd+"/data/laboratories.csv")

    df_new['End'] = df_new['End'].str.replace(' ', '')
    df_new['End'] = df_new['End'].str.replace('\xa0', '')
    df_new.loc[df_new['End']=="--",'End']="2020"
    df_new.loc[df_new['End']=="",'End']="2020"
    df_new['End']=df_new['End'].fillna(2020)

    df_new['Begin'] = df_new['Begin'].astype('Int64')
    df_new.drop(df_new.loc[df_new['Begin']=="TBC"].index, inplace=True)
    df_new['Begin']=df_new['Begin'].astype('int64')
    df_new['End']=df_new['End'].astype('int64')

    df_new['Lifetime']=df_new['End'].astype('int')-df_new['Begin'].astype('int')

    df_new=df_new.sort_values(by=['Begin'])
    df_new['Begin']=pd.to_datetime(df_new['Begin'], format='%Y')
    df_new['End']=pd.to_datetime(df_new['End'], format='%Y')

    st.dataframe(df_new)

    timePlot=alt.Chart(df_new).mark_bar().encode(
    x=alt.X('Begin',scale=alt.Scale(zero=False), title='When'),
    x2='End',
    y=alt.Y('Lab',sort='-x',title='Who'),
    color='Location',
    #column='Place'
    ).properties(width=800)

    st.write(timePlot)

#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
