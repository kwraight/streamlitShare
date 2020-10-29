# client of choice
import pyowm
import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

################
### Useful Functions
################
### Temperature and Humidity plotting
def TempHumPlot(df, f=1):
    ## first axis
    fig, ax1 = plt.subplots()
    color = "tab:red"
    ax1.set_xlabel("Date : Hour")
    ax1.set_ylabel("Temp. [ºC]", color=color)
    ax1.plot(df.time, df.tempC, color=color, label="tempC")
    ax1.tick_params(axis='y', labelcolor=color)
    ## x axis
    plt.xlabel("Date : Hour")
    plt.grid(True)

    ## second axis
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel("humid. [%]", color=color)  # we already handled the x-label with ax1
    ax2.plot(df.time, df.humid, color=color, label="humid")
    ax2.tick_params(axis='y', labelcolor=color)
    ## x axis
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(f))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    plt.setp( ax1.xaxis.get_majorticklabels(), rotation=60, ha="right" )
    ax2.set_yticks(np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax2.get_yticks())))
    ## legend
    ax1.legend(loc='lower left')
    ax2.legend(loc='lower right')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    return fig

################
### Weather info.
################
## set API key
owm = pyowm.OWM("a0f2bf5ef2566260b6ad12ba42f96c95")
## make manager
mgr = owm.weather_manager()
## set location
reg = owm.city_id_registry()
#list_of_tuples = reg.ids_for('london', country='GB', matching='like')
where=['Coatbridge','GB']
myLocations = reg.locations_for(where[0], country=where[1])

## one call https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#onecall
one_call = mgr.one_call(lat=myLocations[0].lat, lon=myLocations[0].lon)
## current time
nowTime = datetime.datetime.now()
## get hourly forecasts --> dictionary of lists
foreInfoHourly={'time':[], 'tempC':[], 'wind':[], 'humid':[]}
for h in range(0,48,1):
    tempC=one_call.forecast_hourly[h].temperature('celsius').get('temp',None)
    wind=one_call.forecast_hourly[h].wind().get('speed',None)
    humid=one_call.forecast_hourly[h].humidity
    nextTime = nowTime + datetime.timedelta(hours=h)
    foreInfoHourly['time'].append("{0:02}/{1:02}:{2:02}".format(nextTime.date().day,nextTime.date().month,nextTime.hour))
    foreInfoHourly['tempC'].append(tempC)
    foreInfoHourly['wind'].append(wind)
    foreInfoHourly['humid'].append(humid)

## get daily forecasts --> dictionary of lists
# what is the epoch for yesterday at this time?
foreInfoDaily={'time':[], 'tempC':[], 'wind':[], 'humid':[]}
yesterday_epoch = pyowm.utils.formatting.to_UNIXtime(pyowm.utils.timestamps.yesterday())
one_call_yesterday = mgr.one_call_history(lat=myLocations[0].lat, lon=myLocations[0].lon, dt=yesterday_epoch)

otempC = one_call_yesterday.current.temperature('celsius').get('temp',None)
owind = one_call_yesterday.current.wind().get('speed',None)
ohumid = one_call_yesterday.current.humidity
otime = nowTime + datetime.timedelta(days=-1)
foreInfoDaily['time'].append("{0:02}/{1:02}:{2:02}".format(otime.date().day,otime.date().month,otime.hour))
foreInfoDaily['tempC'].append(otempC)
foreInfoDaily['wind'].append(owind)
foreInfoDaily['humid'].append(ohumid)

one_call.forecast_daily[0].temperature('celsius').get('day',None)
for h in range(0,7,1):
    tempC=one_call.forecast_daily[h].temperature('celsius').get('day',None)
    wind=one_call.forecast_daily[h].wind().get('speed',None)
    humid=one_call.forecast_daily[h].humidity
    nextTime = nowTime + datetime.timedelta(days=h)
    foreInfoDaily['time'].append("{0:02}/{1:02}:{2:02}".format(nextTime.date().day,nextTime.date().month,nextTime.hour))
    foreInfoDaily['tempC'].append(tempC)
    foreInfoDaily['wind'].append(wind)
    foreInfoDaily['humid'].append(humid)

## make dataframe from dictionary of lists
dfHourly = pd.DataFrame(foreInfoHourly)
dfDaily = pd.DataFrame(foreInfoDaily)
#df = pd.DataFrame(list(zip(foreInfo['time'],foreInfo['tempC'],foreInfo['wind'],foreInfo['humid'])), columns = ['time','tempC','wind','humid'])


################
### Final format
################

st.write("""## Weather forecast for **"""+where[0]+"""** ***("""+where[1]+""")*** """+str("{0:02}:{1:02}".format(nowTime.hour,nowTime.minute))+""" """)
#st.line_chart(df.tempC)

st.write("""## Hourly info. (48h)""")
## make hourly plot
fig1=TempHumPlot(dfHourly,3)
st.pyplot(fig1)

st.write("""## Daily info. (7days)""")
## make daily plot
fig2=TempHumPlot(dfDaily)
st.pyplot(fig2)
