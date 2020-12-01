import streamlit as st
### general stuff
import os
import sys
###session stuff
import stInfrastructure as infra
### pages
import page_top
import page_exp
import page_acc
import page_lab
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
        "Experiments": page_exp.main_part,
        "Accelerators": page_acc.main_part,
        "Laboratories": page_lab.main_part,
        "Broom cupboard": page_debug.main_part,
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


#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
