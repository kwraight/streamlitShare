import streamlit as st
import datetime
import os
import sys
cwd = os.getcwd()
sys.path.insert(1, cwd)
### for streamlitShare
cwd = os.getcwd()

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

    st.write("### Simple pixel detecter 1D simulation")


    st.write("### Select page from lefthand side bar")
    st.write("  * Top Page(here): select measurement scale")
    st.write("  * Set Parameters: Set simulation recipe: number pixels, charge sharing, beam width, threshold")
    st.write("  * Broom Cupboard: Boring debugging stuff")

    state.cwd=cwd
    if state.debug:
        st.error("Debug is on")
        st.write("Current directory:",cwd)
        st.write(os.listdir())

    ##
    st.write("### Activate simulation from sidebar")
