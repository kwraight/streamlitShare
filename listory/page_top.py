import streamlit as st
import datetime
import os
import sys
cwd = os.getcwd()
sys.path.insert(1, cwd)
### for streamlitShare
cwd = os.getcwd()
### for laptop
#cwd = "/Users/kwraight/repositories/streamlitShare"

#####################
### Top page
#####################

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))


### main part
def main_part(state):
    nowTime = datetime.datetime.now()
    st.write("""## :fireworks: **Listory App** :fireworks: """)
    st.write("""### :calendar: ("""+DateFormat(nowTime)+""")""")
    st.write(" --- ")
    ###

    st.write("## Under construction!!!")

    state.cwd=cwd

    if state.debug:
        st.write("Debug is on")
        st.write("Current directory:",cwd)
