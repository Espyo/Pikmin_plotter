import os, sys
import hashlib
from common import *

'''
========================
Analyzes all objects and print out interesting facts.
'''
def get_stats(objects) :
    
    print "Analyzing and gathering info..."
    
    avg = [0, 0, 0]
    farthest_objs_from_avg = []
    overlapping_objs = []
    
    max_y = -99999
    min_y = 99999
    max_y_obj = None
    min_y_obj = None
    
    for obj in objects :
        y = obj.pos[1]
        
        avg = obj.pos
        
        if y > max_y :
            max_y = y
            max_y_obj = obj
        if y < min_y :
            min_y = y
            min_y_obj = obj
    
    for obj in objects :
        d = dist(obj.pos[0], obj.pos[2], avg[0], avg[2])
        
        add_to_top_list(farthest_objs_from_avg, 5, True, obj, d)
        
        for obj2 in objects :
            if obj == obj2 : continue
            if(
                obj.pos[0] - 4 <= obj2.pos[0] and
                obj.pos[0] + 4 >= obj2.pos[0] and
                obj.pos[2] - 4 <= obj2.pos[2] and
                obj.pos[2] + 4 >= obj2.pos[2]
            ) :
                #Check if this pair already exists.
                valid = True
                for pair in overlapping_objs :
                    if pair == [obj2, obj] :
                        valid = False
                        break
                
                if valid :
                    overlapping_objs.append([obj, obj2])

    
    print "Done. Results:"
    print " "
    print "Farthest objects from average (" + coords_to_str(avg) + "):"
    
    for f in farthest_objs_from_avg :
        print "  " + get_spaced_name(f[0].name) + " " + coords_to_str(f[0].pos)
    
    print "Highest and lowest vertically:"
    print "  " + get_spaced_name(max_y_obj.name) + " " + coords_to_str(max_y_obj.pos)
    print "  " + get_spaced_name(min_y_obj.name) + " " + coords_to_str(min_y_obj.pos)
    
    print "Overlapping objects:"
    
    for o in overlapping_objs :
        print "  " + get_spaced_name(o[0].name) + " " + coords_to_str(o[0].pos)
        print "  " + get_spaced_name(o[1].name) + " " + coords_to_str(o[1].pos)


'''
========================
Returns the name of an object in a size apt for printing alignment.
'''
def get_spaced_name(name) :
    name = name[:16]
    while len(name) < 16 :
        name += " "
    return name
