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

def main_part(state):
    st.title(":wrench: Broom cupboard")
    st.write("---")
    st.write("Bits and bobs for maintainance:")
    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        state.clear()
