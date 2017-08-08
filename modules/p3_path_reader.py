import os, sys
import hashlib
from common import *

'''
========================
Goes through a Pikmin 3 path file and
returns all nodes found.
'''
def read_path(input_file) :
    nodes = []
    line_nr = 0
    state = 0
    '''
    State info:
      0: looking for "# index"
      1: looking for position
      2: looking for radius
      3: looking for links
      4: looking for "## type"
    '''
    next_state_line = 0
    links_seen = 0

    cur_node = None

    for line in input_file:

        line_nr = line_nr + 1

        if len(line) == 0: continue

        if state == 0:
            #A "# index" is a good way to find the start of a new node
            if line.find("# index") == -1 : continue
            
            cur_node = PathNodeData()
            cur_node.id_nr = len(nodes)
            
            state = 1
            
        elif state == 1:
            #Position information.
            
            cur_node.pos = []
            
            pos_data = line.split(" ")
            for p in xrange(0, 3) :
                cur_node.pos.append(float(pos_data[p]))
            
            state = 2
            
        elif state == 2:
            #Radius.
            
            radius_data = line.split(" ")
            cur_node.radius = float(radius_data[0])
            
            next_state_line = line_nr + 12
            state = 3
            links_seen = 0
            
        elif state == 3:
            #Get the links (which are under the section commented as "incomings"...)
            if line_nr != next_state_line : continue
            
            links_seen = links_seen + 1
            
            line_parts = line.split(" ")
            i = int(line_parts[0])
            u1 = float(line_parts[1])
            u2 = int(line_parts[2])
            u3 = int(line_parts[3])
            if i != -1 :
                l = PathLinkData()
                l.id_nr = i
                l.unk1 = u1
                l.unk2 = u2
                l.unk3 = u3
                cur_node.links.append(l)
            
            if links_seen == 8 :
                state = 4
            else :
                next_state_line = line_nr + 1
        
        elif state == 4:
            #Find the end of the link list. A "# type" is a good way to know.
            if line.find("# type") == -1 : continue
            
            #Add the node to the list.
            nodes.append(cur_node)
            del cur_node
            
            state = 0

    return nodes