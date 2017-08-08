import os, sys
from modules import common, p1_path_reader, path_stats, path_plotter

'''
========================
Main function.
'''    
def main() :
    
    common.print_help(
        "Pikmin 1 path tool\n"
        "  This program reads Pikmin 1 paths in a file\n"
        "  and either plots them on output.png or returns\n"
        "  interesting statistics.\n"
        "  You need to create the files yourself; they should\n"
        "  start with the first \"point\" block, and end with\n"
        "  the last \"link\" block. Keep the indentation. The last\n"
        "  line should be an empty line. You can obtain these blocks\n"
        "  from .mod files in /courses/*/*.mod\n"
    )
    
    nodes = []
    bg_img_name = "";
    for a in sys.argv :
        if(a[0] == "-") : break
        
        if a.find(".png") != -1 :
            bg_img_name = a
        else :
            input_file = open(a, "rb")
            nodes.extend(p1_path_reader.read_path(input_file))

    print "Found " + str(len(nodes)) + " path nodes."

    if common.find_arg("-s") :
        path_stats.get_stats(nodes)
        
    else :
        md = common.Metadata()
        #md.scale = p1_constants.scale
        md.scale = 0.8
        
        if common.find_arg("-p") : md.view_mode = 1
        if common.find_arg("-x") : md.offset_x = float(common.find_arg("-x"))
        if common.find_arg("-y") : md.offset_y = float(common.find_arg("-y"))
        if common.find_arg("-w") : md.img_w = int(common.find_arg("-w"))
        if common.find_arg("-h") : md.img_h = int(common.find_arg("-h"))
        
        path_plotter.plot(nodes, (common.find_arg("-hi") or ""), md, bg_img_name)


'''
========================
'''
if __name__=="__main__":
    main()

