### standard
import streamlit as st
from core.Page import Page
### custom
import core.stInfrastructure as infra
### this page
import os
import json
import pandas as pd
import plotly.express as px
import altair as alt
from st_aggrid import AgGrid
import datetime
import pyjokes

import random

#####################
### useful functions
#####################

thePeople={
"Sandy":{'init':"SW",'bants':":notes: Your name is _Alexander Hamilton_!"},
"Hunter":{'init':"IH",'bants':":muscle: Staunch!"},
"McCall":{'init':"IM",'bants':":guitar: True Dat."},
"Ritchie":{'init':"RT",'bants':":beers: Ritchie T - he tell _no_ lies."},
"Roscoe":{'init':"CR",'bants':":football:"},
"Tony":{'init':"TB",'bants':":hand: Salve Centurion!"},
"Andy":{'init':"AS",'bants':":notebook: Poet, Philosopher and all round good guy."},
"Gerry":{'init':"GC",'bants':":jack_o_lantern:"},
"Kenny":{'init':"KW",'bants':":space_invader: It's me!"},
"Gilmour":{'init':"SG",'bants':":wine_glass: 'Mon the Well!"},
"Dima":{'init':"DM",'bants':":ru: Bastard!"},
"Williams":{'init':"IW",'bants':":blush: Smartie's in the house!"},

}

crackerDict={
'colours':["an angry fuckin' red","blue, but not too blue", "green like a bogey",
        "orange but not staunch", "brown like a jobbie", "grey. what the fuck?! grey?"],
'toys':["little comb","uncomfortable fake moustache", "ridiculously small deck of cards",
        "never-to-be-seen-again small screwdriver set", "piece of plastic that someone claims their parents used to have",
        "jumping frog"]
}

def GetInitials(name):
    return thePeople[name]['init']

instructions=["  * choose your name",
        "  * choose name of who you are submitting for",
        "   * select date",
        "   * select time range",
        "  * add submission string to set",
        "   * copy set and send to Sandy"]

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Night out", ":raised_hands: Welcome to the Christmas App", instructions)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        st.write("## :christmas_tree: :gift: :calendar: Count down")
        today = datetime.date.today()
        xDay = datetime.date(today.year, 12, 25)
        # st.write("this year:",today.year)
        # st.write("this xDay:",xDay)
        diff = xDay - today
        st.write("### :sleeping: fuck me it's",diff.days,"sleeps to Christmas!")

        if "fixes" not in pageDict.keys():
            pageDict['fixes']=""
        st.write("### :bell: "+pageDict['fixes']+" Who ir ye? "+pageDict['fixes'])

        nameList=list(thePeople.keys())
        ### set name
        infra.SelectBox(pageDict,'name',nameList,'Select your name:')

        st.write(thePeople[pageDict['name']]['bants'])

        infra.ToggleButton(pageDict,'jumper','Are you wearing a Christmas jumper?')
        if pageDict['jumper']:
            st.write("The **magic** happens!")
            pageDict['fixes']=":sparkles:"
        else:
            pageDict['fixes']=""

        ###
        st.write("### :beers: "+pageDict['fixes']+" Whose round it is? "+pageDict['fixes'])
        if st.button("random choice"):
            st.write("It's *Roscoe's* round")

        ###
        st.write("### :bell: "+pageDict['fixes']+" Christmas controversies "+pageDict['fixes'])

        infra.Radio(pageDict,'dieHard',["don't know", "yes", "no"],"Is Die Hard a Christmas movie?")
        if pageDict['dieHard']=="yes":
            st.write(":thumbsdown: Is it fuck!")
        elif pageDict['dieHard']=="no":
            st.write(":thumbsup: Correctamundo!")

        infra.Radio(pageDict,'sprouts',["don't know", "yep", "nup"],"Sprouts?")
        if pageDict['sprouts']=="yep":
            st.write(":scream_cat: Whatever man, you can have mine")
        elif pageDict['sprouts']=="nup":
            st.write(":smile_cat: You know thems the boke")

        ###
        st.write("### :bell: "+pageDict['fixes']+" Pull a cracker? "+pageDict['fixes'])


        if st.button("Pull a cracker?"):
            st.write(":sparkles: **CRACK** :sparkles:")
            try:
                pageDict['crackNum']+=1
            except KeyError:
                pageDict['crackNum']=1
            pageDict['cracker']={'colour':random.choice(crackerDict['colours']), 'toy':random.choice(crackerDict['toys']), 'joke': str(pyjokes.get_joke(language='en', category= 'all'))}

        try:
            if pageDict['crackNum']>1 and pageDict['crackNum']<5:
                st.write("Cheeky wee multi-tug")
            elif pageDict['crackNum']>=5 and pageDict['crackNum']<10:
                st.write("that's a good few pulls right there yiv hid")
            elif pageDict['crackNum']>=10 and pageDict['crackNum']<20:
                st.write("jeezo! Calm down there Tuglas Ross")
            elif pageDict['crackNum']>=20:
                st.write("well if yer looking for a high score:",pageDict['crackNum'])
        except KeyError:
            pass

        if "cracker" in pageDict.keys():
            st.write("*This cracker*...")
            st.write("**hat colour**:",pageDict['cracker']['colour'])
            st.write("**toy**:",pageDict['cracker']['toy'])
            st.write("**joke**:",pageDict['cracker']['joke'])

        ###
        st.write("### :bell: "+pageDict['fixes']+" Playlist :notes: "+pageDict['fixes'])

        if st.button("Spotify Christmas music list"):
            st.write("**fuck the fuck off ya lazy fuck**")
            st.write("Who wipes yer arse fir ye?")
