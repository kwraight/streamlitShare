### streamlit stuff
import streamlit as st
###
import base64
import pandas as pd
import json
import numpy as np
###
from urllib import request
from annotated_text import annotated_text, annotation
from quote import quote
import random

################
### Useful functions
################

### set selection default value
DEFAULT = '< PICK A VALUE >'
def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
    func = st.sidebar.selectbox if sidebar else st.selectbox
    return func(text, np.insert(np.array(values, object), 0, default))

### get csv file from dataframe
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(sep="\t", index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href

### show df with option to download
def DisplayWithOption(df, optKey=None):
    st.dataframe(df)
    if st.button("download table", key=optKey):
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

### pandas cell colouring
def ColourCells(s, df, colName, flip=False):
    thisRow = pd.Series(data=False, index=s.index)
    # vailable colours: 9*x=5
    colours=['red','blue','green','orange','purple''yellow','pink','lightblue','lightgreen']*5
    names=list(df[colName].unique())
    if flip:
        return ['background-color: %s ; color: %s'% ('white',colours[names.index(s[colName])])]*len(df.columns)
    else:
        return ['background-color: %s ; color: %s'% (colours[names.index(s[colName])],'black')]*len(df.columns)



###
### Widgets
###

def Version():
    return ("27-06-22")


def ToggleButton(myDict, myKey, txt):
    try:
        myDict[myKey] = st.checkbox(txt, value=myDict[myKey])
    except KeyError:
        myDict[myKey] = st.checkbox(txt, value=False)


def TextBox(myDict, myKey, txt, pwd=False):
    if pwd:
        try:
            myDict[myKey] = st.text_input(label=txt, type="password", value=myDict[myKey])
        except KeyError:
            myDict[myKey] = st.text_input(label=txt, type="password")
        except ValueError:
            myDict[myKey] = st.text_input(label=txt, type="password")
    else:
        try:
            myDict[myKey] = st.text_input(label=txt, value=myDict[myKey])
        except KeyError:
            myDict[myKey] = st.text_input(label=txt)
        except ValueError:
            myDict[myKey] = st.text_input(label=txt)


def SelectBox(myDict, myKey, opts, txt, lamKey=None):
    if len(opts)<1:
        st.write("No options found for "+myKey)
        st.stop()
    sortedOpts=opts
    if type(opts[0])!=type({}) and type(opts[0])!=type([]):
        sortedOpts=sorted(opts)

    if lamKey==None:
        try:
            myDict[myKey]=st.selectbox(txt, sortedOpts, index=sortedOpts.index(myDict[myKey]) )
        except KeyError:
            myDict[myKey]=st.selectbox(txt, sortedOpts )
        except ValueError:
            myDict[myKey]=st.selectbox(txt, sortedOpts )
    else:
        #st.write("for",lamKey,"and",myDict[myKey],":",opts.index(myDict[myKey]))
        if type(opts[0])==type({}):
            sortedOpts=sorted(opts, key=lambda k: k[lamKey])
        try:
            myDict[myKey]=st.selectbox(txt, sortedOpts, format_func=lambda x: x[lamKey], index=sortedOpts.index(myDict[myKey]) )
        except KeyError:
            myDict[myKey]=st.selectbox(txt, sortedOpts, format_func=lambda x: x[lamKey] )
        except ValueError:
            myDict[myKey]=st.selectbox(txt, sortedOpts, format_func=lambda x: x[lamKey] )


### pandas dataframe variation
def SelectBoxDf(myDict, myKey, df, txt, colName):
    if colName not in list(df.columns):
        st.write("No",colName,"found in dataframe")
        st.stop()
    opts=list(df[colName].unique())
    sortedOpts=sorted(opts)
    try:
        val=st.selectbox(txt, sortedOpts, index=sortedOpts.index(myDict[myKey]) )
    except KeyError:
        val=st.selectbox(txt, sortedOpts )
    except ValueError:
        val=st.selectbox(txt, sortedOpts )
    myDict[myKey]=df.query(colName+'=="'+val+'"')


def MultiSelect(myDict, myKey, opts, txt, lamKey=None):
    if len(opts)<1:
        st.write("No options found for "+myKey)
        st.stop()
    sortedOpts=opts
    if type(opts[0])!=type({}) and type(opts[0])!=type([]):
        sortedOpts=sorted(opts)

    if lamKey==None:
        try:
            myDict[myKey]=st.multiselect(txt, sortedOpts, default=myDict[myKey] )
        except KeyError:
            myDict[myKey]=st.multiselect(txt, sortedOpts )
        except ValueError:
            myDict[myKey]=st.multiselect(txt, sortedOpts )
        except st.StreamlitAPIException:
            myDict[myKey]=st.multiselect(txt, sortedOpts )
    else:
        #st.write("for",lamKey,"and",myDict[myKey],":",opts.index(myDict[myKey]))
        if type(opts[0])==type({}):
            sortedOpts=sorted(opts, key=lambda k: k[lamKey])
        try:
            myDict[myKey]=st.multiselect(txt, sortedOpts, format_func=lambda x: x[lamKey], default=myDict[myKey] )
        except KeyError:
            myDict[myKey]=st.multiselect(txt, sortedOpts, format_func=lambda x: x[lamKey] )
        except ValueError:
            myDict[myKey]=st.multiselect(txt, sortedOpts, format_func=lambda x: x[lamKey] )


def Radio(myDict, myKey, opts, txt, lamKey=None):
    if len(opts)<1:
        st.write("No options found for "+myKey)
        st.stop()
    sortedOpts=opts
    if type(opts[0])!=type({}) and type(opts[0])!=type([]):
        sortedOpts=sorted(opts)

    if lamKey==None:
        try:
            myDict[myKey]=st.radio(txt, sortedOpts, index=sortedOpts.index(myDict[myKey]))
        except KeyError:
            myDict[myKey]=st.radio(txt, sortedOpts)
        except ValueError:
            myDict[myKey]=st.radio(txt, sortedOpts)
    else:
        #st.write("for",lamKey,"and",myDict[myKey],":",opts.index(myDict[myKey]))
        if type(opts[0])==type({}):
            sortedOpts=sorted(opts, key=lambda k: k[lamKey])
        try:
            myDict[myKey]=st.radio(txt, sortedOpts, format_func=lambda x: x[lamKey], index=sortedOpts.index(myDict[myKey]) )
        except KeyError:
            myDict[myKey]=st.radio(txt, sortedOpts, format_func=lambda x: x[lamKey] )
        except ValueError:
            myDict[myKey]=st.radio(txt, sortedOpts, format_func=lambda x: x[lamKey] )


def Slider(myDict, myKey, myMin, myMax, txt):
    try:
        myDict[myKey]=st.slider(txt,min_value=myMin,max_value=myMax,value=myDict[myKey])
    except KeyError: # default min value
        myDict[myKey]=st.slider(txt,min_value=myMin,max_value=myMax,value=myMin)
    except ValueError: # default min value
        myDict[myKey]=st.slider(txt,min_value=myMin,max_value=myMax,value=myMin)

###
### EasterEggs
###

### get API response from endpoint
def GetResponse(endStr):
    api_endpoint = endStr
    api_response = json.load(request.urlopen(api_endpoint))
    return api_response

# Get a quote
def GetQOTD():
    myQuote = GetResponse("https://favqs.com/api/qotd")
    return {'body':myQuote['quote']['body'], 'suffix':myQuote['quote']['author'], 'credit':"[FavQuotes](https://favqs.com)"}
    # if myQuote:
    #     annotated_text(
    #     (myQuote['quote']['body'],"","#8ef"),
    #     "\n",
    #     (myQuote['quote']['author'],"","#afa"),
    #     )
    # st.write("credit: [FavQuotes](https://favqs.com)")

def GetQuote(names=None):
    if names==None:
        names=['imre lakatos','paul feyerabend','thomas kuhn','karl popper']
    myQuote = random.choice( quote(random.choice(names)) )
    return {'body':myQuote['quote'], 'suffix':myQuote['author'], 'credit':"[quote package](https://pypi.org/project/quote/)"}
    # if myQuote:
    #     annotated_text(
    #     (myQuote['quote'],"","#8ef"),
    #     "\n",
    #     (myQuote['author'],"","#afa"),
    #     )
    # st.write("credit: [quote package](https://pypi.org/project/quote/)")

def GetDateFact(infoType=None):
    if infoType not in ['Events','Births','Deaths']:
        infoType= random.choice(['Events','Births','Deaths'])
    myReps = GetResponse("https://history.muffinlabs.com/date")
    myRep = random.choice( myReps['data'][infoType] )
    return {'body':myRep['text'], 'suffix':myRep['year']+"("+infoType+")", 'credit':"[muffinlabs](https://history.muffinlabs.com)"}
    # if myRep:
    #     annotated_text(
    #     (myRep['text'],"","#8ef"),
    #     "\n",
    #     (infoType,"","#afa"),
    #     (myRep['year'],"","#afa"),
    #     )
    # st.write("credit: [muffinlabs](https://history.muffinlabs.com)")

def ShowInfo(infoDict):
    body='<p style="font-family:Courier; color:Blue; font-size: 16px;">'+infoDict['body']+'</p>'
    st.write(body, unsafe_allow_html=True)
    suffix='<p style="font-family:Courier; color:Green; font-size: 16px;">'+infoDict['suffix']+'</p>'
    st.write(suffix, unsafe_allow_html=True)
    st.write("credit:",infoDict['credit'])

# def ShowInfo(infoDict):
#     annotated_text( (infoDict['body'],"","#8ef"),
#     "\n",
#     (infoDict['suffix'],"","#afa") )
#     st.write("credit:",infoDict['credit'])
