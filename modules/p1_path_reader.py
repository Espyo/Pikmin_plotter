import os, sys
import hashlib
from common import *

'''
========================
Goes through a Pikmin 1 path file and
returns all nodes found.
'''
def read_path(input_file) :
    nodes = []
    line_nr = 0
    state = 0
    '''
    State info:
      0: looking for "point {" or "link {"
      1: looking for state
      2: looking for position
      3: looking for width
    '''
    next_state_line = 0

    cur_node = None

    for line in input_file:

        line_nr = line_nr + 1

        if len(line) == 0: continue

        if state == 0:
            #A "point {" is a good way to find the start of a new node
            #and a "link {" is a good way to find a link
            if line.find("point {") != -1 :
            
                if cur_node is not None :
                    #Add the current node to the list.
                    nodes.append(cur_node)
                    del cur_node
                
                cur_node = PathNodeData()
                cur_node.id_nr = len(nodes)
                
                next_state_line = line_nr + 2
                state = 1
                
            elif line.find("link {") != -1 :
                
                if cur_node is not None :
                    #Add the current node to the list.
                    nodes.append(cur_node)
                    del cur_node
                    cur_node = None
                    
                trimmed = line[8:]
                trimmed = trimmed[:-2]
                link_parts = trimmed.split(" ")
                
                l = PathLinkData()
                l.id_nr = int(link_parts[1])
                l.unk1 = 0
                l.unk2 = 0
                l.unk3 = 0
                nodes[int(link_parts[0])].links.append(l)
                del l
                
            else :
                continue
                
        elif state == 1:
            
            #State information.
            if line_nr != next_state_line : continue
            
            #Nothing to do, really, since it's not known what the state does.
            state = 2
        
        elif state == 2:
            
            #Position information.
            cur_node.pos = []
            
            trimmed = line[5:]
            pos_data = trimmed.split(" ")
            for p in xrange(0, 3) :
                cur_node.pos.append(float(pos_data[p]))
            
            state = 3
            
        elif state == 3:
            #Width.
            
            trimmed = line[8:]
            cur_node.radius = float(trimmed) / 2
            
            state = 0
        
    return nodes
