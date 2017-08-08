import os, sys
import hashlib
from common import *

'''
========================
Goes through a Pikmin 2 object generator
file and returns all objects found.
'''
def read_objects(input_file) :
    
    objects = []
    line_nr = 0
    state = 0
    '''
    State info:
      0: looking for # reserved
      1: looking for position
      2: looking for object ID
    '''
    next_state_line = 0
    cur_object = None

    for line in input_file:

        line_nr = line_nr + 1

        if len(line) == 0: continue

        if state == 0:
            #All objects seem to have a "# reserved" in their data, so let's search for that
            if line.find("# reserved") == -1: continue
            
            next_state_line = line_nr + 3
            
            state = 1
            
        elif state == 1:
            #Three lines after the "# reserved" is the position info.
            if line_nr != next_state_line: continue
            
            line = line.strip()
            line_parts = line.split(" ")
            
            cur_object = ObjectData()
            
            cur_object.pos = []
            cur_object.pos.append(float(line_parts[0]))
            cur_object.pos.append(float(line_parts[1]))
            cur_object.pos.append(float(line_parts[2]))
            
            next_state_line = line_nr + 2
            state = 2
            
        elif state == 2:
            #Now that we know the position, find the name.
            if line_nr != next_state_line: continue
            
            line = line.strip()
            cur_object.name = line.split("\t")[0].strip()
            
            md5hex = hashlib.md5(cur_object.name).hexdigest()
            md5int = int(md5hex, 16)
            md5int = md5int % pow(2, 24)
            b = (md5int & 0xff0000) >> 16
            g = (md5int & 0x00ff00) >> 8
            r = (md5int & 0x0000ff)
            cur_object.color = (r, g, b)
            
            #Add the object to the list
            objects.append(cur_object)
            
            del cur_object
            
            state = 0
        
    return objects