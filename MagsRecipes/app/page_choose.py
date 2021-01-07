import streamlit as st
import stInfrastructure as infra
### data manipulation
import pandas as pd
import json
from measurement.measures import Weight, Volume
### general
import os
import sys
import re

#####################
### Next page
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

def GetConvVolume(inVal,inUnit,outUnit):
    val=None
    if inUnit=="pint": val=Volume(imperial_pint=inVal)
    elif inUnit=="floz": val=Volume(imperial_oz=inVal)
    elif inUnit=="l": val=Volume(l=inVal)
    elif inUnit=="ml": val=Volume(l=inVal*0.001)
    else: return "Volume conversion issue: check in units"
    if outUnit=="pint": return val.imperial_pint
    elif outUnit=="floz": return val.imperial_oz
    elif outUnit=="l": return val.l
    elif outUnit=="ml": return val.l*1000
    else: return "Volume conversion issue: check out units"


def GetScaleConv(inVal,inUnit,outUnit):
    if inUnit.lower()==outUnit.lower():
        return inVal, inUnit
    val=None
    if inUnit=="kg": val=Weight(kg=inVal)
    elif inUnit=="lb": val=Weight(lb=inVal)
    elif inUnit=="g": val=Weight(g=inVal)
    elif inUnit=="oz": val=Weight(oz=inVal)
    elif inUnit=="pint": val=Volume(imperial_pint=inVal)
    elif inUnit=="floz": val=Volume(imperial_oz=inVal)
    elif inUnit=="l": val=Volume(l=inVal)
    elif inUnit=="ml": val=Volume(l=inVal*0.001)
    else: return inVal, inUnit
    try:
        if inUnit in ["kg","lb","g","oz"]:
            if outUnit=="metric": return val.g, "g"
            elif outUnit=="imperial": return val.oz, "oz"
            else: return None, None
        elif inUnit in ["pint","floz","l","ml"]:
            if outUnit=="metric": return val.ml, "ml"
            elif outUnit=="imperial": return val.floz, "floz"
            else: return None, None
        else: return None, None
    except AttributeError:
        return None, None


def GetName(inStr):
    # split by capitals
    # join to phrase
    # capitalise all words as title
    return " ".join(re.sub( r"([A-Z])", r" \1", inStr).split()).title()

def GetString(data, begStr, endStr):
    start=data.find(begStr)+len(begStr)
    subStr= data[ start: data.find(endStr,start+1) ]
    #return subStr+"_"+str(start)+"_"+str(data.find(endStr,start+1))
    #subStr= data[55:77]
    return subStr

def GetRepiceDict(theFile):
    myDict={}
    data="NYS"
    with open(theFile, 'r') as file:
        data = file.read()
    myDict['title']= GetString(data,'title=\"','\"')
    myDict['author']= GetString(data,'author=\"','\"')
    if 'serves=\"' in data:
        myDict['serves']= GetString(data,'serves=\"','\"')
    myDict['ingredients']= [x.replace('"','').strip() for x in GetString(data,'ingredients=[',']').split(",")]
    myDict['method']= [x.replace('\n\"','').replace('\"\n','') for x in GetString(data,'method=[',']').split('\",')]
    if 'notes=[' in data:
        myDict['notes']= [x.replace('\n\"','').replace('\"\n','') for x in GetString(data,'notes=[',']').split('\",')]
    return myDict

def GetIngDict(inStr):
    # based on name:amount_unit
    outDict={}
    try:
        outDict['name']=inStr.split(':')[0]
        outDict['unit']=inStr.split('_')[1]
        outDict['amount']=inStr.split(':')[1].split('_')[0]
    except:
        print("Something went wrong with formatting!")
        pass
    return outDict

### main part
def main_part(state):
    st.title(":microscope: Select Recipe")
    st.write("---")
    if state.debug:
        st.write("  * select recipe set")
        st.write("  * filter type of dish (if preferred)")
        st.write("  * display list")
        st.write("  * select from list")
        st.write("  * display recipe")
    else:
        st.write(" * toggle debug (LHS) for details")
    st.write("---")
    ###

    # debug check
    if state.debug:
        st.error("Debug is on")
    ## decimal places
    pd.options.display.float_format = "{:,.2f}".format

    ## select from list
    st.write("## Select recipe set")
    sel_name=st.selectbox("Choose a recipe set", ["Mags","Kenny"])

    ## filter recipe type: sweet, savoury
    st.write("## Select type of recipes")
    sel_filt=infra.selectbox_with_default("filter by type",["sweet","savoury"],"Any type")

    ## get list of recipes and display
    st.write("## List of available recipes")
    recipeFiles=[]
    myDir="MagsRecipes/recipes/"+sel_name
    for file in os.listdir(myDir):
        if file.endswith(".rpy") or file.endswith(".xpy"):
            recipeFiles.append(file)
    st.write("Total recipes available:",len(recipeFiles))

    # format dataframe
    df_list=pd.DataFrame(zip(recipeFiles, recipeFiles), columns=["name","file"])
    df_list['name']=df_list['name'].apply(lambda x: GetName(x.replace(".rpy","").replace(".xpy","")) )
    typeMap={".xpy":"sweet",".rpy":"savoury"}
    df_list['type']=df_list['file'].apply(lambda x: typeMap[x[-4::]]  )
    df_list=df_list.sort_values("name")
    if sel_filt!="Any type":
        df_list=df_list.query("type=='"+sel_filt+"'")
    infra.DisplayWithOption(df_list[['name','type']],"1")

    ## select from list
    st.write("## Select recipe")
    sel_rec=st.selectbox("Choose a recipe", list(df_list.values), format_func=lambda x: x[0])

    # ## display recipe: ingredients section and method section
    repDict= GetRepiceDict(myDir+"/"+sel_rec[1])
    if state.debug: st.write(repDict)
    st.write("## Recipe details")
    st.write("### Recipe for **",repDict['title'],"** by *",repDict['author'],"*")
    try:
        st.write("serves:",repDict['serves'])
    except KeyError:
        pass
    try:
        st.write("### notes")
        for n in repDict['notes']:
            st.write(n)
    except KeyError:
        st.write("none")
    st.write("### ingredients")
    df_ing=pd.DataFrame([GetIngDict(x) for x in repDict['ingredients']])
    def ScaleMap(inStr):
        if inStr.lower() in ["kg", "g", "l", "ml"]:
            return "metric"
        elif inStr.lower() in ["lb", "oz", "fl.oz", "pint"]:
            return "imperial"
        else: return "other"
    # original input
    if state.debug:
        st.write("original input:")
        st.dataframe(df_ing)

    # scaling
    df_ing['scale']=df_ing['unit'].apply(lambda x: ScaleMap(x)  )
    df_ing['amount']=df_ing['amount'].astype(float, errors="ignore")
    if state.scale=="imperial":
        #st.write(df_ing.query("scale=='metric'"))
        df_ing['scaleAmount'],df_ing['scaleUnit']=zip( *df_ing.apply(lambda x: GetScaleConv(x['amount'], x['unit'], state.scale), axis=1) )
    elif state.scale=="metric":
        #st.write(df_ing.query("scale=='imperial'"))
        df_ing['scaleAmount'],df_ing['scaleUnit']=zip( *df_ing.apply(lambda x: GetScaleConv(x['amount'], x['unit'], state.scale), axis=1) )
        #st.write(df_ing.query("scale=='imperial'"))
    else:
        if state.debug: st.write("no conversion necessary")

    # display scaled values
    infra.DisplayWithOption(df_ing[["name","scaleAmount","scaleUnit"]],"2")
    st.write("### method")
    for c,m in enumerate(repDict['method'],1):
        st.write(str(c)+". "+m)
