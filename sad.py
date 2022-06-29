from BOTTEL import telegram_chatbot
from nested_lookup import nested_lookup
from nested_lookup import nested_update
from urllib.request import urlopen
#from sERBV import informer
import schedule

import json
import requests
import ast
import time
from datetime import datetime
def prin():
    print("bas kar")
#updates the prev data file to todays file
def update():
    jurl = urlopen("https://api.covid19india.org/state_district_wise.json")
    thedownloadFile=json.loads(jurl.read())
    print("Updated")
    with open("prev.json", 'r+') as t:
         t.truncate()
         t.write(json.dumps(thedownloadFile))
#loads previous data from pc as rs

#rs is open as jrv json this is offline(prev)
def load_latest():
    jurl = urlopen("https://api.covid19india.org/state_district_wise.json")
    return json.loads(jurl.read())

schedule.every().day.at("23:58").do(update)


def loads():
    with open("prev.json", 'r+') as t:
        jrv = t.read()
    # print(json.loads(jrv)["State Unassigned"])
    return json.loads(jrv)



#loaded prev as rs

while True:
    rs = loads()
    schedule.run_pending()
    obj=load_latest()
    #obj is online; latest data
    prnt= ((nested_lookup("districtData",rs)))##this is list of of states data i.e [(state:dist(dict)]
    ldata=((nested_lookup("districtData",obj)))
    delta_data={}

    for (it,lit) in zip(prnt,ldata) :#this loop oterates over districts
            #print(it)
            keyd=list(it.keys())#prints list of states district(keysof data)
            acnl=nested_lookup("active",it)
            ltcnnl=nested_lookup("confirmed",lit)
            #cnnl=nested_lookup("confirmed",it)
            #print(keyd)
            #print(acnl)
            #print(cnnl)
            for (m,n,o) in zip(keyd,acnl,ltcnnl) :#m is district name
                #print(n)
                try:
                 nedat=(nested_lookup(m,obj)[0]["confirmed"])
                 delta_data[m]=nested_lookup(m,rs)[0]["confirmed"]-nedat
                 #print(nested_lookup(m,rs)[0]["confirmed"])
                except:
                 pass
    #this above code replace s by llt=informer()i.e the latest data and find delta

    with open("Delta.json","r+") as dd:
        dd.truncate()
        dd.write(json.dumps(delta_data))
    print(nested_lookup("Nicobars",rs)[0]["confirmed"])
    """with open("Delta.json","r+") as ld:
        nl=ld.read()
    DeltaDict=json.loads(nl)
    print(DeltaDict)"""
    time.sleep(14400)