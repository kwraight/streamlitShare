### standard
import streamlit as st
### Standard
import os
import shutil


physicsDictList=[{'name':"Wind",
               'description':"Wind toys",
               'pics':[{'image':"rainbowFlags.jpg",'caption':"Rainbow flags"},
                       {'image':"turbine.jpg",'caption':"Turbine"},
                       {'image':"spinny.jpg",'caption':"Spinner"}
                       ]},
              # {'name':"Light",
              #  'description':"Light toys",
              #  'pics':[{'image':"flowers",'caption':"Refracting flowers"},
              {'name':"Chemical",
               'description':"Chemical toys",
               'pics':[{'image':"appleClock.jpg",'caption':"Apple clock"}
                    ]},
               {'name':"Solar",
                'description':"Solar toys",
                'pics':[{'image':"miniMill2.jpg",'caption':"Mini mill"},
                        {'image':"lightFlowers.jpg",'caption':"Light flowers"}
                        ]},
               {'name':"Lunar",
                'description':"Lunar toys",
                'pics':[{'image':"telescope.jpg",'caption':"Refracter"},
                        {'image':"halfMoon.jpg",'caption':"Half moon"}
                        ]},
               {'name':"Sonic",
                'description':"Noisy toys",
                'pics':[{'image':"chime.jpg",'caption':"Chime"}
                        ]}
             ]

# def GetTuneListThing(inStr,myKey):
#     my_item = next((item for item in tuneDictList if item['name'] == inStr), None)
#     try:
#         return my_item[myKey]
#     except KeyError:
#         return None
#     return None
#
# def FilterFiles(tuneDir, tuneDictList, suf=".mp3"):
#     retList=[]
#     for t in tuneList:
#         try:
#             for file in os.listdir(tuneDir):
#             #st.write(os.path.join(pageDict['tuneDir'], file))
#                 if file.endswith(suf):
#                     name=os.path.join(tuneDir, file)
#                     short=name.split('/')[-1].replace(suf,'')
#                     if t['match'].lower() in short.lower():
#                         retList.append({'short':t['alias'],'name':name})
#                         break
#         except FileNotFoundError:
#             st.write("No fileDir")
#             return None
#     return retList
#
# def CopyFiles(tuneDir, tuneList, suf=".mp3"):
#
#     for td in tuneDictList:
#         for e,t in enumerate(td['tunes'],1):
#             try:
#                 for file in os.listdir(tuneDir):
#                 #st.write(os.path.join(pageDict['tuneDir'], file))
#                     if file.endswith(suf):
#                         name=os.path.join(tuneDir, file)
#                         short=name.split('/')[-1].replace(suf,'')
#                         if t['match'].lower() in short.lower():
#                             #shutil.copy(src,dst)
#                             newName=name.replace(short,'/'+td['name']+'/'+('%02d' % e)+'_'+t['alias'])
#                             if not os.path.isdir(tuneDir+'/'+td['name']):
#                                 os.mkdir(tuneDir+'/'+td['name'])
#                             shutil.copy(name,newName)
#                             break
#             except FileNotFoundError:
#                 print("No fileDir")
#     return None
