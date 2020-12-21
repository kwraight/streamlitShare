### streamlit stuff
import streamlit as st
### general stuff
import os
import sys
###session stuff
cwd = os.getcwd()
sys.path.insert(1, cwd)
import stInfrastructure as infra
### other
from measurement.measures import Weight
### pages
import page_top
import page_choose
#import page_conv
#import page_add
import page_debug


#####################
### main
#####################

def main():
    ### get state variable
    state = infra.get()

    ### define pages dictionary
    pages = {
        "Top Page": page_top.main_part,
        "Choose Recipe": page_choose.main_part,
        # "Conversions": page_conv.main_part,
        # "Add Recipe": page_add.main_part,
        "Broom cupboard": page_debug.main_part,
    }

    ### sidebar
    st.sidebar.title(":telescope: Mags' Recipes WebApp")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Select your page:", tuple(pages.keys()))

    ### mini converter
    if st.sidebar.button("mini converter"):
        try:
            state.miniCon = not state.miniCon
        except AttributeError:
            state.miniCon = True

    try:
        if state.miniCon:
            st.sidebar.markdown("### mini converter")
            st.sidebar.selectbox("from unit", ["kg","lb","oz","g"])
            st.sidebar.selectbox("to unit", ["kg","lb","oz","g"])
    except:
        pass

    ### debug toggle
    st.sidebar.markdown("---")
    debug = st.sidebar.checkbox("Toggle debug")
    if debug:
        state.debug=True
    else: state.debug=False

    ### display  selected page using state variable
    pages[page](state)


#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
