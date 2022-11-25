#!/usr/bin/python
### short script to convert recipe dictionary json format
import json
from datetime import datetime
import os
#cwd = os.getcwd()
cwd='/Users/kwraight/playground/projects/MagsRecipes/recipes'
import sys

def Dictionise(inStr):
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

# put it together
def GetRecipe(ingredients, method):
    myRcp={"title":"Bread Recipe (machine)", "author":"Kenny"}
    myRcp['ingredients']=[Dictionise(x) for x in ingredients]
    myRcp['method']=[{c:x} for c,x in enumerate(method,1)]
    return myRcp

def Write(jsonDict, jsonName):
    ### should be just about human readable
    j = json.dumps(jsonDict, indent=4)
    f = open(jsonName, 'w')
    print(j, file=f)
    f.close()


sys.path.insert(1, cwd)
cwd
import exampleRecipe as ex
#ingred,method=ex.ReturnIngredientsAndMethod()
myRecipe=GetRecipe(ex.ingredients, ex.method)
myRecipe
## write json
fileName=cwd+"/exampleRecipe.json"
Write(myRecipe,fileName)

fileName
# NOT THIS: jsonDict=json.loads(fileName)
with open(fileName, 'r') as j:
     jsonDict = json.loads(j.read())
jsonDict
