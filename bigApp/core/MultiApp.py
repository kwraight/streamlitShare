import streamlit as st
import corePages
import userPages
###
import os
import sys
import core.stInfrastructure as infra

#####################
### useful functions
#####################

def toggle_debug():
    st.session_state.debug = not st.session_state.debug


class App:

    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.state = {}

        self.init_themes()

    def init_themes(self):
        self.themes = userPages.__all__.keys()
        return

    def init_pages(self,theme=None):
        try:
            self.pages.clear()
        except AttributeError:
            self.pages = dict()
        allPages = []
        allPages = corePages.__all__.copy()
        if theme!=None:
            allPages += userPages.__all__[theme].copy()
        # order pages if required
        #allPages.insert(0, allPages.pop([p().name for p in allPages.index("NAME")))
        allPages.append(allPages.pop([p().name for p in allPages].index("Broom Cupboard")))
        for page in allPages:
            p = page() #self.state)
            self.pages[p.name] = p
        #return {theme:[len(allPages),len(corePages.__all__),len(userPages.__all__),len(self.pages.keys())]}
        #return {theme:[p().name for p in allPages]} #self.pages.keys()}
        return [{k:[p().name for p in v]} for k,v in userPages.__all__.items()]

#####################
### main part
#####################

    def main(self):
        st.sidebar.title(self.title)

        ### sidebar
        st.sidebar.title(":telescope: Kené's WebApp")
        st.sidebar.markdown("---")
        theme = st.sidebar.radio("Select theme: ", tuple(self.themes))
        #st.sidebar.markdown(self.init_pages(theme))
        self.init_pages(theme)
        #st.sidebar.markdown("themes: \n"+",".join(self.pages.keys()))
        name = st.sidebar.radio("Select page: ", tuple(self.pages.keys()))
        st.sidebar.markdown("---")

        try:
            if st.session_state.debug:
                st.sidebar.markdown("on page: "+name)
        except AttributeError:
            pass

        ### check session state attribute, set if none
        try:
            if name in st.session_state[theme].keys():
                if st.session_state.debug: st.sidebar.markdown("session_state \'"+theme+"."+name+"\' OK")
            else:
                st.session_state[theme][name]={}
                if st.session_state.debug: st.sidebar.markdown("session_state \'"+theme+"."+name+"\' defined")
        except KeyError:
            st.session_state[theme]={name:{}}


        ### mini-state summary
        if st.sidebar.button("State Summary"):
            # st.write(dir(state))
            myKeys=[x for x in st.session_state.keys()]
            for mk in myKeys:
                if mk=="broom": continue
                st.sidebar.markdown(f"**{mk}** defined")

        ### debug toggle
        # debug = st.checkbox(label="Toggle debug", key='debug', on_change=toggle_debug)
        # st.markdown("debug: "+str(debug))
        # st.markdown("session: "+str(st.session_state.debug))
        try:
            debug = st.sidebar.checkbox("Toggle debug",value=st.session_state.debug)
        except AttributeError:
            debug = st.sidebar.checkbox("Toggle debug")
        if debug:
            st.session_state.debug=True
        else: st.session_state.debug=False


        ### small print
        st.sidebar.markdown("---")
        st.sidebar.markdown("*small print*:")
        st.sidebar.markdown("[git repository](https://github.com/kwraight/streamlitTemplate)")
        st.sidebar.markdown("[docker repository](https://hub.docker.com/repository/docker/kwraight/template-app)")
        st.sidebar.markdown("streamlitTemplate: "+infra.Version())

        ### get page
        self.pages[name].main()
