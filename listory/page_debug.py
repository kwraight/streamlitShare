import streamlit as st

#####################
### Check state page
#####################
def display_state_values(state):

    st.write("## All data")
    st.write("Debug setting:", state.debug)

    st.write("cwd:",state.cwd)
    # try:
    #     st.write(state.score)
    #     df_results=pd.DataFrame(state.score.items(), columns=["code","points"])
    #     st.write(df_results)
    # except AttributeError:
    #     st.write("No data available")

def main_part(state):
    st.title(":wrench: Broom cupboard")
    st.write("---")
    st.write("Bits and bobs for maintainance:")
    display_state_values(state)

    st.write("## :exclamation: Clear all state settings")
    if st.button("Clear state"):
        state.clear()
