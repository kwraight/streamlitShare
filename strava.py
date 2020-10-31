### WebApp for strava. Requires streamlit, altair, stravaio, stravalib, PIL
## run like: streamlit run strava.py
import pandas as pd
from datetime import datetime
### streamlit stuff
import streamlit as st
from streamlit.ReportThread import get_report_ctx
from streamlit.hashing import _CodeHasher
from streamlit.server.Server import Server
### altair
import altair as alt
### strava
from stravaio import strava_oauth2
from stravalib.client import Client
### import media
from PIL import Image

#####################
### main
#####################
def main():
    state = _get_state()
    pages = {
        "Selection": page_selection,
        "Dashboard": page_dashboard,
        "Check State": page_checking,
    }

    st.sidebar.title(":sweat_smile: Strava Data")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))


    if st.sidebar.button('Get time'):
        stream = os.popen('python3 timeTask.py')
        output = stream.read()
        st.sidebar.markdown(output)

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


#####################
### Check state page
#####################
def display_state_values(state):
    st.write("number:", state.userNum)
    st.write("secret:", state.userSec)
    st.write("token:", state.token)

    if st.button("Clear state"):
        state.clear()

def page_checking(state):
    st.title(":wrench: Checking page")
    st.write("---")
    st.write("This is the values retained in the state data:")
    display_state_values(state)


#####################
### Select data page
#####################
my_cols =['start_date_local',
          'name',
          'type',
          'workout_type',
          'distance',
          'average_speed',
          'elapsed_time',
          'total_elevation_gain',
          'achievement_count']

@st.cache
def SetUser(num,sec):
    return num,sec

@st.cache
def GetToken(usr="NYS", sec="NYS"):
    code=strava_oauth2(client_id=usr, client_secret=sec)
    return code['access_token']

@st.cache
def GetData(token):
    client = Client(access_token=token)
    activities = client.get_activities(limit=1000)
    global my_cols
    data= []
    for activity in activities:
        my_dict = activity.to_dict()
        data.append([my_dict.get(x) for x in my_cols])
    return data

def page_selection(state):
    st.title(":question: Selection page")
    st.write("---")
    st.markdown("## Stava analysis")
    st.markdown("### 1. Get token:")
    st.markdown(" a. Go to your **Strava** page: [strava](https://www.strava.com/dashboard)")
    st.markdown(" b. Navigate to *Settings* and *My API Application*: [api page](https://www.strava.com/settings/api)")
    st.markdown(" c. Get your *Client ID* and *Client Secret* numbers")
    st.markdown(" d. Copy into the fields below")
    st.markdown(" e. Click *Get Token* button")

    image = Image.open('StravaExample.png')
    st.image(image, caption='get info', use_column_width=True)
    #st.image(element, image, caption=None, width=None, use_column_width=False, clamp=False, channels='RGB', format='JPEG')

    st.markdown("### 2. View stats in *Dashboard* page")
    st.write("---")

    number_input = st.text_input(label='user number', value='number')
    secret_input = st.text_input(label='user secret', value='secret')

    if st.button("Get Token"):
        state.userNum,state.userSec=SetUser(number_input,secret_input)

    if state.userNum!=None and state.userSec!=None:
        state.token= GetToken(state.userNum,state.userSec)
        data = GetData(state.token)
        df= pd.DataFrame(data, columns=my_cols)
        st.dataframe(df)
        st.write("data set size:",len(df.index))
        st.write(df.dtypes)

    else:
        st.write("No token")


#####################
### Dashboard page
#####################
def page_dashboard(state):
    st.title(":chart_with_upwards_trend: Plots")
    st.write("---")
    st.markdown("1. Distances checked in over time")
    st.markdown(" a. select subset of data")
    st.markdown("2. Comparisons for selected subset")
    st.markdown(" a. Speed vs. climb")
    st.markdown(" b. Speed vs. distance")
    st.write("---")

    data = GetData(state.token)
    df= pd.DataFrame(data, columns=my_cols)
    #st.dataframe(df)

    df_when=pd.DataFrame(df,columns=["workout_type","average_speed","distance","type"])
    df_when['Date']=pd.to_datetime(df['start_date_local'], format='%Y-%m-%d', errors='ignore')
    df_when['Month']=pd.DatetimeIndex(df_when['Date']).month
    workDict={"1":"first one","2":"long run","3":"workout run","4":"other run","5":"another run","None":"None"}
    df_when['workout_name']=df_when['workout_type'].apply(lambda x:workDict[str(x)])
    df_when.loc[df_when['workout_name'] == 'None', 'workout_name'] = df_when.loc[df_when['workout_name'] == 'None', 'type']
    dayDict={"morning":[x for x in range(6,12)],"afternoon":[x for x in range(12,19)],"evening":[x for x in range(19,24)],"night":[x for x in range(0,6)]}
    df_when['Time']=pd.to_datetime(df['start_date_local'], format='%H-%M-%S', errors='ignore')
    df_when['daytime']=pd.DatetimeIndex(df_when['Time']).hour
    df_when['daytime']=df_when['daytime'].apply(lambda x: "".join([k for k,v in dayDict.items() if x in v]))
    #st.write(df_when)

    st.write('## Monthly check-ins')

    check_types=alt.Chart(df_when).mark_bar().encode(
    x='count(Month):Q',
    y='Month:O',
    color='workout_name:N'
    )
    st.write(check_types)

    distance=alt.Chart(df_when).mark_bar().encode(
    x='sum(distance):Q',
    y='Month:O',
    color='workout_name:N'
    )
    st.write(distance)

    grouping=["Month"]
    df_when=df_when.sort_values(by=['Month'], ignore_index=True)
    df_when_g=pd.DataFrame({'runs' : df_when.groupby( grouping )['Date'].count(), 'aveSpeedMin' : df_when.groupby( grouping )['average_speed'].min(), 'aveSpeedMax' : df_when.groupby( grouping )['average_speed'].max() }).reset_index()
    df_when_g_3=pd.DataFrame({'runs_3' : df_when[df['workout_type']=='3'].groupby( grouping )['Date'].count(), 'aveSpeedMin_3' : df_when[df['workout_type']=='3'].groupby( grouping )['average_speed'].min(), 'aveSpeedMax_3' : df_when[df['workout_type']=='3'].groupby( grouping )['average_speed'].max() }).reset_index()
    df_when_g = pd.concat([df_when_g, df_when_g_3[["runs_3", "aveSpeedMin_3","aveSpeedMax_3"]]], axis=1, sort=False)
    df_when_g=df_when_g.sort_values(by=['Month'], ignore_index=True)
    #df_when_g=df_when_g.set_index("Month")
    #st.write(df_when_g)
    #st.write("data set size:",len(df_when_g.index))
    #st.write(df_when_g.dtypes)


    base = alt.Chart(df_when_g).encode(
        alt.X('Month:O',
              axis=alt.Axis(
                  labelAngle=-45,
                  title='Month'
              )
        )
    ).properties(
        title='Max/min average speed per month',
        width=800,
        height=300
    )

    rule = base.mark_rule(color='blue', opacity=0.3).encode(
        alt.Y(
            'aveSpeedMin:Q',
            title='average_speed',
            scale=alt.Scale(zero=False),
        ),
        alt.Y2('aveSpeedMax:Q')
    )

    bar = base.mark_bar(color='orange',opacity=0.3).encode(
        alt.Y('aveSpeedMin_3:Q'),
        alt.Y2('aveSpeedMax_3:Q')
    )

    st.write(rule + bar)


    st.write('## Time of day check-ins')
    check_types=alt.Chart(df_when).mark_bar().encode(
    x='count(daytime):Q',
    y='daytime:O',
    color='workout_name:N'
    )
    st.write(check_types)
    grouping=["daytime"]
    df_day_g=pd.DataFrame({'runs' : df_when.groupby( grouping )['Date'].count(), 'aveSpeedMin' : df_when.groupby( grouping )['average_speed'].min(), 'aveSpeedMax' : df_when.groupby( grouping )['average_speed'].max(), 'aveSpeedMean' : df_when.groupby( grouping )['average_speed'].mean() }).reset_index()
    st.write(df_day_g)

    state.activities=st.multiselect('Select activities', df['type'].unique())

    ## walks have no workout type
    df=df[df['type'].isin(state.activities)]
    st.write('## Overall (inc. '+", ".join(state.activities)+' )')
    df['workout_name']=df['workout_type'].apply(lambda x:workDict[str(x)])
    df.loc[df['workout_name'] == 'None', 'workout_name'] = df.loc[df['workout_name'] == 'None', 'type']
    interval = alt.selection_interval()
    plot_time = alt.Chart(df).mark_circle().encode(
        x='start_date_local:T',
        y='distance',
        color=alt.condition(interval, 'workout_name', alt.value('lightgray')),
        size=alt.Size('achievement_count',
            #scale=alt.Scale(range=[0, 100]),
            legend=alt.Legend(title='achievements')
            ),
        tooltip=['name', 'distance', 'start_date_local']
    ).properties(
        title='All Check-ins',
        width=800,
        height=300,
        selection=interval
    )
    plot_comp_one = alt.Chart(df).mark_point().encode(
                    x = alt.X('total_elevation_gain', scale=alt.Scale(zero=False), axis = alt.Axis(title = 'climb')),
                    y = alt.Y('average_speed', scale=alt.Scale(zero=False), axis = alt.Axis(title = 'speed')),
                    color='workout_name',
                    tooltip=['name', 'total_elevation_gain', 'average_speed']
                ).properties(
                    title='Selected Comparison A',
                    width=600
                ).transform_filter(
                    interval
                ).interactive()
    text = plot_comp_one.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text='name'
    )
    plot_comp_two = alt.Chart(df).mark_point().encode(
                    x = alt.X('distance', scale=alt.Scale(zero=False), axis = alt.Axis(title = 'distance')),
                    y = alt.Y('average_speed', scale=alt.Scale(zero=False), axis = alt.Axis(title = 'speed')),
                    color='workout_name',
                    tooltip=['name', 'distance', 'average_speed']
                ).properties(
                    title='Selected Comparison B',
                    width=600
                ).transform_filter(
                    interval
                ).interactive()
    text = plot_comp_two.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text='name'
    )


    st.write(plot_time & plot_comp_one & plot_comp_two)


#####################
### state functions
#####################
class _SessionState:

    def __init__(self, session):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state():
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session)

    return session._custom_session_state


if __name__ == "__main__":
    main()
