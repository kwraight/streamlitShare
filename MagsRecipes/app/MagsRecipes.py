### streamlit stuff
import streamlit as st
### general stuff
import os
import sys
###session stuff
cwd = os.getcwd()
sys.path.insert(1, cwd)
import stInfrastructure as infra
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

    # ### mini-state summary
    # if st.sidebar.button("State Summary"):
    #     ### token
    #     try:
    #         if len(state.myToken)>0:
    #             st.sidebar.markdown("Got token")
    #         else:
    #             st.sidebar.markdown("No token found")
    #     except AttributeError:
    #         st.sidebar.markdown("No token defined")
    #     ### component IDs
    #     try:
    #         st.sidebar.markdown("Component IDs defined: "+str(len(state.ids)))
    #     except AttributeError:
    #         st.sidebar.markdown("No components defined")

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
