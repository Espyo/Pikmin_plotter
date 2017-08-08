from common import *

'''
========================
Plots paths onto the image.
'''
def plot(data, highlight, metadata, bg_img_name) :
    
    o = init_plotting(data, metadata, calculate_paths_bbox(data), bg_img_name)
    output = o[0]
    output_draw = o[1]
    
    if len(highlight) > 0 :
        cx = metadata.orig_x + data[int(highlight)].pos[0] * metadata.scale
        cy = metadata.orig_y + data[int(highlight)].pos[2] * metadata.scale
        
        #Draw a cross through it.
        output_draw.line([
            0,
            cy,
            metadata.img_w,
            cy],
            fill = "cyan"
        )
        output_draw.line([
            cx,
            0,
            cx,
            metadata.img_h],
            fill = "cyan"
        )
    
    for node in data :
            
        cx = metadata.orig_x + node.pos[0] * metadata.scale
        cy = metadata.orig_y + node.pos[2] * metadata.scale
        r = node.radius * metadata.scale
        output_draw.ellipse([
            cx - r,
            cy - r,
            cx + r,
            cy + r],
            fill = "red"
        )
    
    for node in data :
        for link in node.links :
            
            cx = metadata.orig_x + node.pos[0] * metadata.scale
            cy = metadata.orig_y + node.pos[2] * metadata.scale
            linkcx = metadata.orig_x + data[link.id_nr].pos[0] * metadata.scale
            linkcy = metadata.orig_y + data[link.id_nr].pos[2] * metadata.scale
            draw_arrow(
                cx, cy, linkcx, linkcy, output_draw, metadata.arrow_size * metadata.scale,
                color = ("yellow" if link.unk2 != 0 else "purple")
            )
    
    output.save("output.png")
    print "Output successful."
    

'''
========================
Returns the lowest and highest X and Y of all path nodes.
'''
def calculate_paths_bbox(data) :
    
    ret = [99999, 99999, -99999, -99999]
    for n in data :
        ret[0] = min(ret[0], n.pos[0])
        ret[1] = min(ret[1], n.pos[2])
        ret[2] = max(ret[2], n.pos[0])
        ret[3] = max(ret[3], n.pos[2])
    return ret
