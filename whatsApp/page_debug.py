import streamlit as st

#####################
### Check state page
#####################
def display_state_values(state):

    st.write("## Internal")
    st.write("Debug setting:", state.debug)

    st.write("cwd:",state.cwd)

    st.write("### requirements")
    try:
        with open(state.cwd+'/requirements.txt', 'r') as file:
            data = file.read().replace('\n', ', ')
        st.write(data)
    except FileNotFoundError:
        st.write("No requirements found")

    st.write("### Data")
    try:
        st.write("last entries of dataframe:")
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
