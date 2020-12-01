import streamlit as st

#####################
### Check state page
#####################
def display_state_values(state):
    st.write("file:", state.file)
    st.write("last entries of dataframe:")
    try:
        st.dataframe(state.df.tail())
    except AttributeError:
        st.write("No data selected")

def main_part(state):
    st.title(":clipboard: Checking page")
    st.write("---")
    st.write("This is current data:")
    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        state.clear()
