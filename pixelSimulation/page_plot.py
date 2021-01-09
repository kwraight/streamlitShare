import streamlit as st
import stInfrastructure as infra
import altair as alt
import pandas as pd

#####################
### Plotting page
#####################

### main part
def main_part(state):
    st.write("""## :fireworks: **Plotting Page** :fireworks: """)
    st.write(" --- ")
    ###

    if state.debug:
        st.error("Debug is on")

    doWork=False
    try:
        st.write("Got results :"+str(len(state.simResults)))
        doWork=True
        if state.debug: st.write(state.simResults)
    except AttributeError:
        st.write("No results yet")

    if doWork:
        ## select results
        st.write("## Select data")
        results=st.selectbox("select results by name", state.simResults, index=0, format_func=lambda x: x['name'])

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
        if state.debug:
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
