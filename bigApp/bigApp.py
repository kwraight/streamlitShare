### streamlit stuff
import streamlit as st
### general stuff
import os
import sys
from datetime import datetime
###session stuff
cwd = os.getcwd()
sys.path.insert(1, cwd)
import stInfrastructure as infra
### pages
# welcome
import page_top
import page_test
import page_debug
# physics
import page_topPhysics
# STS
import page_topSTS
# home
import page_topHome
import page_music

#####################
### main
#####################

def main():
    ### get state variable
    state = infra.get()

    ### define pages dictionary
    pages0 = {
        'groupName': "Welcome",
        'groupPages': {
            "Intro": page_top.main_part,
            "test": page_test.main_part,
            "Broom cupboard": page_debug.main_part,
            }
    }

    pagesA = {
        'groupName': "Physics",
        'groupPages': {
            "Welcome A": page_topPhysics.main_part,
            }
    }

    ### define pages dictionary
    pagesB = {
        'groupName': "STS",
        'groupPages': {
            "Welcome B": page_topSTS.main_part,
            }
    }

    ### define pages dictionary
    pagesC = {
        'groupName': "Home",
        'groupPages': {
            "Welcome C": page_topHome.main_part,
            "music": page_music.main_part,
            }
    }

    ### sidebar
    st.sidebar.title(":telescope: Kené's WebApp")
    st.sidebar.markdown("---")
    group = st.sidebar.radio("Select Group:", [pages0,pagesA,pagesB,pagesC], format_func=lambda x: x['groupName'])
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Select page:", tuple(group['groupPages'].keys()))
    st.sidebar.markdown("---")

    try:
        if state.debug:
            st.sidebar.markdown("group:"+group['groupName'])
            st.sidebar.markdown("page:"+page)
    except AttributeError:
        pass

    # ### mini-state summary
    # if st.sidebar.button("State Summary"):
    #     st.sidebar.markdown("---")
    #     ### token
    #     try:
    #         st.sidebar.markdown("Got "+state.authenticate['user']['firstName']+"'s token")
    #     except AttributeError:
    #         st.sidebar.markdown("No token defined")


    ### debug toggle
    st.sidebar.markdown("---")
    debug = st.sidebar.checkbox("Toggle debug")
    if debug:
        state.debug=True
    else: state.debug=False

    ### display  selected page using state variable
    group['groupPages'][page](state)


#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
