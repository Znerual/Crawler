import bge
import math
import mathutils
import os
import aud
import random
con =""
obj = ""
poi_data = []
added_data = {}
debug = False
def init(self):
    bge.logic.globalDict['points'] = {}
    bge.logic.globalDict['added_data'] = {}
    bge.logic.globalDict['current_pos'] = (10.0,0.0)
    bge.logic.globalDict['handle'] = ""
    bge.logic.globalDict['deco_count'] = 0
    #bge.logic.globalDict['start'] = [-1.0,-1.0,1.0]
    #bge.logic.globalDict['end'] = [1.0,1.0,1.0]
    print("Init")
    print(os.getcwd())
    try:
        stream = open("D://Blends/2D Game/map.dat","r")
        poi_data = stream.readlines()
        stream.close()
    except IOError as e:
        print("Error")
    print("Read data file")
    for poi in poi_data:
        header = poi.split("|")
        content = header[1].split(";")
        #print(content)
        event = header[0].split(";")
        event_list = []
        bge.logic.getCurrentScene().objects['spawn'].worldPosition = mathutils.Vector((float(event[0]),float(event[1]),0.01))
        bge.logic.getCurrentScene().addObject('groundmark_switch','spawn',0)
        for value_pair in content:
            key_pair = value_pair.split(",")
            #print(key_pair)
            event_list.append(((int(key_pair[0]),int(key_pair[1])), int(key_pair[2])))
        bge.logic.globalDict['points'][(int(event[0]), int(event[1]))] = event_list
        if debug == False:
             bge.logic.getCurrentScene().objects['x']['Text']=""
             bge.logic.getCurrentScene().objects['y']['Text']=""
        bge.logic.globalDict['init'] = False
        bge.logic.getCurrentScene().objects['Camera'].playAction('levelStart',0,120)
        print("Generated data points")
def main(self):
    if 'init'in bge.logic.globalDict:
        
        con = self
        obj = con.owner
        scene = bge.logic.getCurrentScene()
        pos = getPosition(obj)
        if bge.logic.globalDict['init'] == False:
            if scene.objects['Camera'].getDistanceTo(scene.objects['loading']) > 20.0:
                scene.objects['loading'].endObject()
                bge.logic.globalDict['init'] = True
        if debug == True:
            scene.objects['x']['Text'] = str(pos[0]) + ";" + str(pos[1])
        
        bge.logic.globalDict['deco_count'] += random.randint(1,5)
        if bge.logic.globalDict['deco_count'] >= 2500:
            showDecoration(scene)
            bge.logic.globalDict['deco_count'] = 0
        if pos != bge.logic.globalDict['current_pos']:
            bge.logic.globalDict['current_pos'] = pos
            if pos in bge.logic.globalDict['points']:        
                print("trigger")
                
                for event in bge.logic.globalDict['points'][pos]:
                    loc = event[0]
                    if event[1] == 1:
                        if not (loc[0],loc[1]) in bge.logic.globalDict['added_data']:
                            x = loc[0]
                            y = loc[1]
                            
                            scene.objects["spawn"].worldPosition = mathutils.Vector((x,y,-1))
                            added_obj = scene.addObject("add","spawn",0)
                            bge.logic.globalDict['added_data'][(loc[0],loc[1])] = added_obj
                            added_obj.children[0].playAction('appear',0,20)
                            added_obj.worldPosition = mathutils.Vector((x,y,1))
                            
                            #bge.logic.globalDict['handle'] = playSound("electriczap.wav")
                            
                           # bge.logic.globalDict['start'] = [x - 40, y , 1]
                            #bge.logic.globalDict['end'] = [x + 40, y , 1]
                            
                    elif event[1] == -1:
                        print("delete")
                        if (loc[0],loc[1]) in bge.logic.globalDict['added_data']:
                            showDecoration(scene)
                            bge.logic.globalDict['added_data'][(loc[0],loc[1])].endObject()
                            del(bge.logic.globalDict['added_data'][(loc[0],loc[1])])                     
                            #bge.logic.globalDict['handle'] = playSound("electricladder.wav")
def getPosition(obj):
    return (int(round(obj.worldPosition.x)),int(round(obj.worldPosition.y)))
def playSound(sound):
    if bge.logic.globalDict['handle'] != "" and bge.logic.globalDict['handle'].status ==  aud.AUD_STATUS_PLAYING:
        return bge.logic.globalDict['handle']
    device = aud.device()
    factory = aud.Factory.buffer(aud.Factory(bge.logic.expandPath("//") + sound))
    handle = device.play(factory)
    handle.volume = 0.4
    return handle
def showDecoration(scene):
    adder = scene.objects['spawn_dec']
    oldLocX = adder.worldPosition.x
    dx = random.randint(-40,40)
    dz = random.randint(-2,2)
    if debug == True:
        scene.objects['y']['Text'] = str(dx) + ":" + str(dz)
    loc = mathutils.Vector((adder.worldPosition.x +dx ,adder.worldPosition.y ,adder.worldPosition.z + dz))
    adder.worldPosition = loc
    added_obj = scene.addObject("decoration", adder,400)
    added_obj.children[0].playAction("flyIn",0,400)
    adder.worldPosition.x = oldLocX