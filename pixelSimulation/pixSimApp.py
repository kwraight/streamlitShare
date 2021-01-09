### streamlit stuff
import streamlit as st
### general stuff
import datetime
import os
import sys
###session stuff
cwd = os.getcwd()
sys.path.insert(1, cwd)
import stInfrastructure as infra
### other
cwd = os.getcwd()
sys.path.insert(1, cwd+"/code")
import pixelSim
### pages
import page_top
import page_setup
import page_plot
#import page_add
import page_debug



#####################
### main
#####################

### format datetime
def DateFormat(dt):
    return str("{0:02}-{1:02}-{2:04}".format(dt.day,dt.month,dt.year))+" at "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))


def RunSimulation(state):
    settings={'numPix':state.numPix,'chargeSharing':state.chargeSharing,'beamWidth':state.beamWidth,'chipMode':state.chipMode,'threshold':state.threshold}
    simResults=[]
    for px in range(0,state.numPix,1):
        simResults.append(pixelSim.RunPixSim(npx=state.numPix, px_idx=px, cs=state.chargeSharing, bw=state.beamWidth, mode=state.chipMode, thl=state.threshold))
    try:
        state.simResults.append({'name':state.name,'pix_data':simResults,'settings':settings})
    except AttributeError:
        state.simResults=[{'name':state.name,'pix_data':simResults,'settings':settings}]
    return "Simulation complete: "+DateFormat(datetime.datetime.now())


def main():
    ### get state variable
    state = infra.get()

    ### define pages dictionary
    pages = {
        "Top Page": page_top.main_part,
        "Set Parameters": page_setup.main_part,
        "Plotting": page_plot.main_part,
        # "Add Recipe": page_add.main_part,
        "Broom cupboard": page_debug.main_part,
    }

    ### sidebar
    st.sidebar.title(":telescope: Run Simple Pixel Simulation")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Select your page:", tuple(pages.keys()))


    st.sidebar.markdown("### Simulation status")
    try:
        if state.ready:
            if st.sidebar.button("Run Simulation!"):
                outVal=RunSimulation(state)
                st.sidebar.markdown(outVal)
    except AttributeError:
        st.sidebar.markdown("Simulation not ready")
    st.sidebar.markdown("### Results")
    try:
        st.sidebar.markdown("Got results :"+str(len(state.simResults)))
    except AttributeError:
        st.sidebar.markdown("No results yet")


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
