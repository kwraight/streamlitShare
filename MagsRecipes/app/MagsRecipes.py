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
from measurement.measures import Weight, Volume
### pages
import page_top
import page_choose
#import page_conv
#import page_add
import page_debug


#####################
### main
#####################

def GetConvWeight(inVal,inUnit,outUnit):
    val=None
    if inUnit=="kg": val=Weight(kg=inVal)
    elif inUnit=="lb": val=Weight(lb=inVal)
    elif inUnit=="g": val=Weight(g=inVal)
    elif inUnit=="oz": val=Weight(oz=inVal)
    else: return "Weight conversion issue: check in units"
    if outUnit=="kg": return val.kg
    elif outUnit=="lb": return val.lb
    elif outUnit=="g": return val.g
    elif outUnit=="oz": return val.oz
    else: return "Weight conversion issue: check out units"

def GetConvVolume():
    val=None
    if inUnit=="pint": val=Volume(imperial_pint=inVal)
    elif inUnit=="floz": val=Volume(imperial_oz=inVal)
    elif inUnit=="l": val=Volume(l=inVal)
    elif inUnit=="ml": val=Volume(l=inVal*0.001)
    else: "Volume conversion issue: check in units"
    if outUnit=="pint": return val.imperial_pint
    elif outUnit=="floz": return val.lb
    elif outUnit=="l": return val.l
    elif outUnit=="ml": return val.l*1000
    else: return "Volume conversion issue: check out units"


def GetConv(inVal,inUnit,outUnit):
    val=None
    if inUnit in ["kg","lb","g","oz"] and outUnit in ["kg","lb","g","oz"]:
        return GetConvWeight(inVal,inUnit,outUnit)
    elif inUnit in ["pint","floz","l","ml"] and outUnit in ["pint","floz","l","ml"]:
        return GetConvVolume(inVal,inUnit,outUnit)
    else: return "Conversion mismatch issue: check units of the same type (Weight, Volume)"


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
            inUnit=st.sidebar.selectbox("from unit", ["kg","lb","oz","g"]+["pint","floz","l","ml"])
            outUnit=st.sidebar.selectbox("to unit", ["kg","lb","oz","g"]+["pint","floz","l","ml"])
            inVal=st.sidebar.number_input('amount', value=1.)
            st.sidebar.markdown("Conversion:")
            outVal=GetConv(inVal, inUnit, outUnit)
            convStr=str(inVal)+" *"+inUnit+"*"+"  -->  "+str(outVal)+" *"+outUnit+"*"
            if "issue" in outVal:
                convStr=outVal
            st.sidebar.markdown(convStr)
    except:
        pass

    state.scale = st.sidebar.radio("Select scale:", ["metric", "imperial"])

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
