from common import *

'''
========================
Plots objects onto the image.
'''
def plot(data, highlight, metadata, bg_img_name) :
    
    o = init_plotting(data, metadata, calculate_object_bbox(data), bg_img_name)
    output = o[0]
    output_draw = o[1]
    
    fnt_ok = True
    try :
        fnt = ImageFont.truetype('font.ttf', 10)
    except :
        print "Warning: font.ttf not found. Objects will be nameless."
        fnt_ok = False
    
    if len(highlight) > 0 :
        for obj in data :
            cx = metadata.orig_x + obj.pos[0] * metadata.scale
            cy = metadata.orig_y + obj.pos[2] * metadata.scale
        
            if obj.name == highlight :
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
        
    
    for obj in data :
        cx = metadata.orig_x + obj.pos[0] * metadata.scale
        cy = metadata.orig_y + obj.pos[2] * metadata.scale
        color = "red" if fnt_ok else obj.color
        
        output_draw.ellipse([
            cx - 4,
            cy - 4,
            cx + 4,
            cy + 4],
            fill = color
        )
        
        if fnt_ok :
            short_name = ""
            if len(obj.name) <= 7 :
                short_name = obj.name
            else :
                short_name = obj.name[:3] + "." + obj.name[-3:]
            output_draw.text(
                (cx + 4, cy - 4),
                short_name,
                font = fnt,
                fill = color
            )
    
    output.save("output.png")
    print "Output successful."


'''
========================
Returns the lowest and highest X and Y of all mobs.
'''
def calculate_object_bbox(data) :
    
    ret = [99999, 99999, -99999, -99999]
    for o in data :
        ret[0] = min(ret[0], o.pos[0])
        ret[1] = min(ret[1], o.pos[2])
        ret[2] = max(ret[2], o.pos[0])
        ret[3] = max(ret[3], o.pos[2])
    return ret
