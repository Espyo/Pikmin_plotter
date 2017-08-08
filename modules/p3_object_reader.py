import os, sys
import hashlib
from common import *

'''
========================
Goes through a Pikmin 3 object generator
file and returns all objects found.
'''
def read_objects(input_file) :
    objects = []
    line_nr = 0
    state = 0
    '''
    State info:
      0: looking for #
      1: looking for object name
      2: looking for "mPos"
      3: looking for position info
    '''
    next_state_line = 0
    cur_object = None

    for line in input_file:

        line_nr = line_nr + 1

        if len(line) == 0: continue

        if state == 0:
            #A pound at the start is an easy way to identify the next object.
            if line[0] != "#": continue
            
            if line_nr == 1: next_state_line = line_nr + 2
            else: next_state_line = line_nr + 1
            
            state = 1
            
        elif state == 1:
            #After a pound comes the name of the object...eventually.
            if line_nr != next_state_line: continue
            
            line = line.strip()
            
            cur_object = ObjectData()
            
            cur_object.name = line[1 : len(line) - 3] #The last three characters don't matter
            md5hex = hashlib.md5(cur_object.name).hexdigest()
            md5int = int(md5hex, 16)
            md5int = md5int % pow(2, 24)
            b = (md5int & 0xff0000) >> 16
            g = (md5int & 0x00ff00) >> 8
            r = (md5int & 0x0000ff)
            cur_object.color = (r, g, b)
            
            state = 2
            
        elif state == 2:
            #Now that we know the name, find mPos.
            
            line = line.strip()
            if line != '"mPos"': continue
            
            next_state_line = line_nr + 2
            state = 3
            
        elif state == 3:
            #Find the coordinates.
            if line_nr != next_state_line: continue
            
            line = line.strip()
            line_parts = line.split(" ")
            cur_object.pos = []
            for p in line_parts :
                cur_object.pos.append(float(p))
            
            #Add the object to the list
            objects.append(cur_object)
            
            del cur_object
            
            state = 0
        
    return objects
