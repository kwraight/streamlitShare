import streamlit as st
###session stuff
import stInfrastructure as infra
### pages
import page_top
import page_personal
import page_combined
import page_debug

#####################
### main
#####################
def main():
    ### get state variable
    state = infra.get()
    pages = {
        "Selection": page_top.main_part,
        "Dashboard (personal)": page_personal.main_part,
        "Dashboard (combined)": page_combined.main_part,
        "Broom cupboard": page_debug.main_part,
    }

    st.sidebar.title(":joy: WhatsApp Data")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    ### debug toggle
    st.sidebar.markdown("---")
    debug = st.sidebar.checkbox("Toggle debug")
    if debug:
        state.debug=True
    else: state.debug=False

    # Display the selected page with the session state
    pages[page](state)


#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
