import os, sys
import hashlib
from common import *

'''
========================
Analyzes all nodes and print out interesting facts.
'''
def get_stats(nodes) :
    
    print "Analyzing and gathering info..."
    
    avg = [0, 0, 0]
    farthest_nodes_from_avg = []
    overlapping_nodes = []
    dead_ends = []
    longest_links = []
    shortest_links = []
    
    max_y = -99999
    min_y = 99999
    max_y_node = None
    min_y_node = None
    
    for node in nodes :
        y = node.pos[1]
        
        avg = node.pos
        
        if y > max_y :
            max_y = y
            max_y_node = node
        if y < min_y :
            min_y = y
            min_y_node = node
    
    for node in nodes :
        d = dist(node.pos[0], node.pos[2], avg[0], avg[2])
        
        add_to_top_list(farthest_nodes_from_avg, 5, True, node, d)
        
        for node2 in nodes :
            if node == node2 : continue
            if(
                node.pos[0] - 4 <= node2.pos[0] and
                node.pos[0] + 4 >= node2.pos[0] and
                node.pos[2] - 4 <= node2.pos[2] and
                node.pos[2] + 4 >= node2.pos[2]
            ) :
                #Check if this pair already exists.
                valid = True
                for pair in overlapping_nodes :
                    if pair == [node2, node] :
                        valid = False
                        break
                
                if valid :
                    overlapping_nodes.append([node, node2])
        
        if len(node.links) == 0 :
            dead_ends.append(node)
        
        for link in node.links :
            node2 = nodes[link.id_nr]
            d = dist(node.pos[0], node.pos[2], node2.pos[0], node2.pos[2])
            
            add_to_top_list(longest_links, 20, True, [node, node2], d)
            add_to_top_list(shortest_links, 16, False, [node, node2], d)
                
    
    print "Done. Results:"
    print " "
    print "Farthest nodes from average (" + coords_to_str(avg) + "):"
    
    for f in farthest_nodes_from_avg :
        print "  " + get_spaced_id(f[0].id_nr) + " " + coords_to_str(f[0].pos)
    
    print "Highest and lowest vertically:"
    print "  " + get_spaced_id(max_y_node.id_nr) + " " + coords_to_str(max_y_node.pos)
    print "  " + get_spaced_id(min_y_node.id_nr) + " " + coords_to_str(min_y_node.pos)
    
    print "Overlapping nodes:"
    
    for n in overlapping_nodes :
        print "  " + get_spaced_id(n[0].id_nr) + " " + coords_to_str(n[0].pos)
        print "  " + get_spaced_id(n[1].id_nr) + " " + coords_to_str(n[1].pos)
        
    print "Dead end nodes:"
    
    for n in dead_ends :
        print "  " + get_spaced_id(n.id_nr) + " " + coords_to_str(n.pos)
    
    print "Longest links:"
    
    for l in longest_links :
        print(
            "  " + get_spaced_id(l[0][0].id_nr) + " -> " + get_spaced_id(l[0][1].id_nr) +
            " (" + str(l[1]) + ")"
        )
    
    print "Shortest links:"
    
    for l in shortest_links :
        print(
            "  " + get_spaced_id(l[0][0].id_nr) + " -> " + get_spaced_id(l[0][1].id_nr) +
            " (" + str(l[1]) + ")"
        )


'''
========================
Returns the id of a node in a size apt for printing alignment.
'''
def get_spaced_id(id_nr) :
    id_str = str(id_nr)
    while len(id_str) < 4 :
        id_str += " "
    return "#" + id_str
