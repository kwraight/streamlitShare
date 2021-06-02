### streamlit stuff
import streamlit as st
### general stuff
import os
import sys
from datetime import datetime
###session stuff
cwd = os.getcwd()
sys.path.insert(1, cwd)
import stInfrastructure as infra
import page_debug
#pagesDir=cwd+"/pages"
#sys.path.insert(1, pagesDir)
#import page_A_top
# get pages from pages directory
import importlib
## standard pages
stdDir=cwd+"/pages"
stdFiles= sorted([f for f in os.listdir(stdDir) if os.path.isfile(os.path.join(stdDir, f)) and "page_" in f and not f.endswith("~")])
sys.path.insert(1, stdDir)
stdModules= [importlib.import_module(p[:-3]) for p in stdFiles]
## content pages
physicsDir=cwd+"/pages/physics"
stsDir=cwd+"/pages/STS"
otherDir=cwd+"/pages/other"
physicsFiles= sorted([f for f in os.listdir(physicsDir) if os.path.isfile(os.path.join(physicsDir, f)) and "page_" in f and not f.endswith("~")])
stsFiles= sorted([f for f in os.listdir(stsDir) if os.path.isfile(os.path.join(stsDir, f)) and "page_" in f and not f.endswith("~")])
otherFiles= sorted([f for f in os.listdir(otherDir) if os.path.isfile(os.path.join(otherDir, f)) and "page_" in f and not f.endswith("~")])
## get modules
sys.path.insert(1, physicsDir)
physicsModules= [importlib.import_module(p[:-3]) for p in physicsFiles]
sys.path.insert(1, stsDir)
stsModules= [importlib.import_module(p[:-3]) for p in stsFiles]
sys.path.insert(1, otherDir)
otherModules= [importlib.import_module(p[:-3]) for p in otherFiles]
# #infra=importlib.import_module('stInfrastructure')
#####################
### main
#####################

def main():
    ### get state variable
    state = infra.get()

    ### define pages dictionary
    pages0 = {
        'groupName': "Welcome",
        'groupPages': dict(zip([p.split('_')[-1][:-3] for p in stdFiles],[getattr(m,"main_part") for m in stdModules]))
    }
    pages0['groupPages']['Broom cupboard']=page_debug.main_part

    pagesA = {
        'groupName': "Physics",
        'groupPages': dict(zip([p.split('_')[-1][:-3] for p in physicsFiles],[getattr(m,"main_part") for m in physicsModules]))
    }

    pagesB = {
        'groupName': "STS",
        'groupPages': dict(zip([p.split('_')[-1][:-3] for p in stsFiles],[getattr(m,"main_part") for m in stsModules]))
    }

    pagesC = {
        'groupName': "Home",
        'groupPages': dict(zip([p.split('_')[-1][:-3] for p in otherFiles],[getattr(m,"main_part") for m in otherModules]))
    }

    ##############
    # side bar
    ##############

    ### title and credits
    st.sidebar.title(":telescope: My Big Custom WebApp")

    st.sidebar.markdown("---")

    ### sidebar
    st.sidebar.title(":telescope: Kené's WebApp")
    st.sidebar.markdown("---")
    group = st.sidebar.radio("Select Group:", [pages0,pagesA,pagesB,pagesC], format_func=lambda x: x['groupName'])
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Select page:", tuple(group['groupPages'].keys()))
    st.sidebar.markdown("---")

    try:
        if state.debug:
            st.sidebar.markdown("group:"+group['groupName'])
            st.sidebar.markdown("page:"+page)
    except AttributeError:
        pass

    st.sidebar.markdown("---")

    ### debug toggle
    debug = st.sidebar.checkbox("Toggle debug")
    if debug:
        state.debug=True
    else: state.debug=False

    st.sidebar.markdown("---")

    ### small print
    st.sidebar.markdown("*small print*")
    st.sidebar.markdown("[git repository](https://gitlab.cern.ch/wraight/itkpdbtemplate)")
    st.sidebar.markdown("[docker repository](https://hub.docker.com/repository/docker/kwraight/itk-pdb-template)")

    ### display  selected page using state variable
    group['groupPages'][page](state)


#########################################################################################################

#########################################################################################################

### run
if __name__ == "__main__":
    main()
