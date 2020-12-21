import streamlit as st
import stInfrastructure as infra
### data manipulation
import pandas as pd
import json
### general
import os
import sys
import re

#####################
### Next page
#####################

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
    st.write("## Choose your dish")
    if state.debug:
        st.write("  * display list")
        st.write("  * select from list")
        st.write("  * display recipe")
    else:
        st.write(" * toggle debug for details")
    st.write("---")
    ###

    # debug check
    if state.debug:
        st.write("### Debug is on")

    ## select from list
    sel_name=st.selectbox("Choose a recipe set", ["Mags","Kenny"])

    sel_filt=infra.selectbox_with_default("filter by type",["sweet","savoury"],"Any type")
    ## get list of recipes and display
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
    sel_rec=st.selectbox("Choose a recipe", list(df_list.values), format_func=lambda x: x[0])

    # ## display recipe: ingredients section and method section
    repDict= GetRepiceDict(myDir+"/"+sel_rec[1])
    if state.debug: st.write(repDict)
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
    infra.DisplayWithOption(df_ing,"2")
    st.write("### method")
    for c,m in enumerate(repDict['method'],1):
        st.write(str(c)+". "+m)
