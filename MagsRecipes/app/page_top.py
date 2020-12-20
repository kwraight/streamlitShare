import streamlit as st
import datetime
import os
import sys
import json
import subprocess
import ast
### PDB stuff

#####################
### Top page
#####################

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))


### main part
def main_part(state):
    nowTime = datetime.datetime.now()
    st.write("""## :fireworks: **Top Page** :fireworks: """)
    st.write("""### :calendar: ("""+DateFormat(nowTime)+""")""")
    st.write(" --- ")
    ###

    # debug check
    if state.debug:
        st.write("### Debug is on")
