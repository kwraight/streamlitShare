### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### this page
import altair as alt
import pandas as pd

#####################
### main part
#####################

class Page3(Page):
    def __init__(self):
        super().__init__("Setup", ":microscope: Select Simulation Parameters", instructions)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        doWork=False
        try:
            st.write("Got results :"+str(len(st.session_state.simResults)))
            doWork=True
            if state.debug: st.write(st.session_state.simResults)
        except AttributeError:
            st.write("No results yet")

        if doWork:
            ## select results
            st.write("## Select data")
            results=st.selectbox("select results by name", st.session_state.simResults, index=0, format_func=lambda x: x['name'])

            ## settings for selected dataset
            st.write("### Settings of selected dataset")
            st.write(results['settings'])

            ## plotting
            ### collect pixel info.
            pix_xs = [p for p in range(0,len(results['pix_data'][0]),1)]
            pix_deps = [x for x in results['pix_data'][0]]
            pix_idxs = [0 for p in range(0,len(results['pix_data'][0]),1)]
            for i in range(1,results['settings']['numPix'],1):
                pix_xs.extend([p for p in range(0,len(results['pix_data'][i]),1)])
                pix_deps.extend([x for x in results['pix_data'][i]])
                pix_idxs.extend([i for p in range(0,len(results['pix_data'][i]),1)])

            ### put info. in dataframe
            pixel_data = pd.DataFrame({
              'x': pix_xs,
              'y': pix_deps,
              'px': pix_idxs
            })
            if st.session_state.debug:
                st.dataframe(pixel_data)

            ### plot dataframe
            yTitle="Counts"
            if results['settings']['chipMode']=="tpx":
                yTitle="Charge deposited"
            myPlot=alt.Chart(pixel_data).mark_line().encode(
                x=alt.X('x', axis=alt.Axis(title="Arbitrary units")),
                y=alt.Y('y', axis=alt.Axis(title=yTitle)),
                color=alt.Color('px:O', scale=alt.Scale(scheme='dark2'), legend=alt.Legend(title="Pixel"))
            ).interactive()
            ### mark pixel limits
            line_data = pd.DataFrame({'a': [x*55.0 for x in range(0,results['settings']['numPix']+1,1) ]})
            pix_lines=alt.Chart(line_data).mark_rule(strokeDash=[1,1],size=3).encode(
                x=alt.X('a:Q', axis=alt.Axis(labels=False))
            )

            combPlot=myPlot+pix_lines
            st.altair_chart(combPlot, use_container_width=True)
