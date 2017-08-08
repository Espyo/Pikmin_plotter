import os, sys
import hashlib
from modules import common, p2_object_reader, p2_constants, object_stats, object_plotter

'''
========================
Main function.
'''    
def main() :
    
    common.print_help(
        "Pikmin 2 object tool\n"
        "  This program reads Pikmin 2 area objects in a file\n"
        "  and either plots them on output.png or returns\n"
        "  interesting statistics.\n"
        "  The files can be found in /user/Abe/map.\n"
    )
    
    objects = []
    bg_img_name = "";
    for a in sys.argv :
        if(a[0] == "-") : break
        
        if a.find(".png") != -1 :
            bg_img_name = a
        else :
            input_file = open(a, "rb")
            objects.extend(p2_object_reader.read_objects(input_file))

    print "Found " + str(len(objects)) + " objects."

    if common.find_arg("-s") :
        object_stats.get_stats(objects)
        
    else :
        md = common.Metadata()
        md.scale = p2_constants.scale
        
        if common.find_arg("-p") : md.view_mode = 1
        if common.find_arg("-x") : md.offset_x = float(common.find_arg("-x"))
        if common.find_arg("-y") : md.offset_y = float(common.find_arg("-y"))
        if common.find_arg("-w") : md.img_w = int(common.find_arg("-w"))
        if common.find_arg("-h") : md.img_h = int(common.find_arg("-h"))
        
        img_recognized = False
        if bg_img_name != "" :
            for n in p2_constants.alignments :
                if bg_img_name.find(n) != -1 :
                    print "Recognized image " + bg_img_name + ". Will align automatically."
                    img_recognized = True
                    md.offset_x = p2_constants.alignments[n].x
                    md.offset_y = p2_constants.alignments[n].y
                    md.img_background_rot = p2_constants.alignments[n].r
                    break
            
            if not img_recognized :
                print "Note: image " + bg_img_name + " is not recognized. No automatic alignment will be made."
        
        object_plotter.plot(objects, (common.find_arg("-hi") or ""), md, bg_img_name)


'''
========================
'''
if __name__=="__main__":
    main()

