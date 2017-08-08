#TODO auto offset, rotate, and render the plots on a map; use the p2_constants and p3_constants files
#TODO figure out the flags for P3 carrying paths
#TODO warn if, with the given image metadata, some objects/paths will not be visible in the image
from PIL import Image, ImageDraw, ImageFont
import os, sys, math

'''
========================
Represents data for a game object.
'''
class ObjectData :
    def __init__(self) :
        self.pos = (0, 0, 0)
        self.name = ""
        self.color = 0xFF0000


'''
========================
Represents data for a path's node.
'''
class PathNodeData :
    def __init__(self) :
        self.id_nr = -1
        self.pos = (0, 0, 0)
        self.radius = 0
        self.links = []


'''
========================
Represents data for a path node's link.
'''
class PathLinkData :
    def __init__(self) :
        self.id_nr = -1
        self.unk1 = 0 #Pikmin 3 has three unknown values per link.
        self.unk2 = 0
        self.unk3 = 0


'''
========================
Represents parameters that control the output image.
'''
class Metadata :
    def __init__(self) :
        self.view_mode = 0 #0: real size. 1: show everything.
        self.img_w = 1024
        self.img_h = 1024
        self.img_background = None #Background image to plot on top of.
        self.img_background_rot = 0 #Degrees to rotate the background image by.
        self.scale = 0.2 #Scale for the Pikmin 3 radar textures.
        self.arrow_size = 30
        self.offset_x = 0
        self.offset_y = 0
        self.orig_x = 0 #Location of the world origin on the final image.
        self.orig_y = 0


'''
========================
Plots to the image.
data:        list of items.
metadata:    metadata for how to render the image.
bbox:        bounding box where all items fit.
bg_img_name: file name of the background image, if any.
'''
def init_plotting(data, metadata, bbox, bg_img_name) :
    
    print "Writing to image..."
    
    #Setup metadata.
    if metadata.view_mode == 0 :
        metadata.orig_x = metadata.img_w / 2
        metadata.orig_y = metadata.img_h / 2
    else :
        content_w = bbox[2] - bbox[0]
        content_h = bbox[3] - bbox[1]
        scale_x = min(1, metadata.img_w / content_w)
        scale_y = min(1, metadata.img_h / content_h)
        metadata.scale = min(scale_x, scale_y)
        metadata.orig_x = -bbox[0] * metadata.scale
        metadata.orig_y = -bbox[1] * metadata.scale
    
    metadata.orig_x = metadata.orig_x + metadata.offset_x
    metadata.orig_y = metadata.orig_y + metadata.offset_y
    
    if bg_img_name != "" :
        metadata.img_background = Image.open(bg_img_name)
        metadata.img_w = metadata.img_background.width
        metadata.img_h = metadata.img_background.height
    
    #Start the image.
    output = Image.new("RGBA", (metadata.img_w, metadata.img_h))
    output_draw = ImageDraw.Draw(output)
    
    if bg_img_name != "" :
        output.paste(metadata.img_background.rotate(metadata.img_background_rot))
    
    #Draw a cross at the origin.
    output_draw.line([
        metadata.orig_x - 8,
        metadata.orig_y,
        metadata.orig_x + 8,
        metadata.orig_y],
        fill = "green"
    )
    output_draw.line([
        metadata.orig_x,
        metadata.orig_y - 8,
        metadata.orig_x,
        metadata.orig_y + 8],
        fill = "green"
    )
    
    return [output, output_draw]


'''
========================
Loads an image from the disk.
name: File name.
'''
def load_image(name) :
    return Image.load(name)
    
   
'''
========================
Draws a purple arrow onto the image.
Points from x1,y1 to x2,y2.
'''
def draw_arrow(x1, y1, x2, y2, draw, size, color = None) :
    
    if color == None : color = "purple"

    #Let's distance the arrows from the ending point a bit.
    angle = math.atan2(y1 - y2, x1 - x2)
    
    x2 += math.cos(angle) * 2
    y2 += math.sin(angle) * 2
    
    draw.line(
        [x1, y1, x2, y2],
        fill = color
    )
    draw.polygon(
        [x2, y2,
        x2 + math.cos(angle + math.pi / 8) * size,
        y2 + math.sin(angle + math.pi / 8) * size,
        x2 + math.cos(angle - math.pi / 8) * size,
        y2 + math.sin(angle - math.pi / 8) * size],
        outline = color,
        fill = color
    )


'''
========================
Converts some coordinates to a string, for use in printing.
'''
def coords_to_str(coords) :
    
    strs = ["", "", ""]
    for i in xrange(3) :
        strs[i] = str(coords[i])
        strs[i] = strs[i][:6]
        
        while len(strs[i]) < 6 :
            strs[i] += "0"
    
    return strs[0] + " " + strs[1] + " " + strs[2]


'''
========================
Returns False if a certain argument was not passed to the program,
otherwise, returns the argument right after it ("0" if last).
'''
def find_arg(arg) :
    
    arg = arg.lower()
    for a in xrange(len(sys.argv)) :
        word = sys.argv[a].lower()
        if word == arg :
            if a == len(sys.argv) - 1 :
                return "0"
            else :
                return sys.argv[a + 1]
    return False


'''
========================
Returns the distance between two points.
'''
def dist(x1, y1, x2, y2) :
    dx = x1 - x2
    dz = y1 - y2
    return math.sqrt(dx * dx + dz * dz)


'''
========================
Adds an item to a list that stores the top values.
'''
def add_to_top_list(items, max_results, for_largest, item, value) :
    insert = 0
    
    if len(items) > 0 :
        insert = max_results
    
    for i in reversed(xrange(len(items))) :
        if (value > items[i][1] and for_largest) or (value < items[i][1] and not for_largest) :
            insert = i
    
    if insert < max_results :
        items.insert(insert, [item, value])
        if len(items) > max_results :
            del items[max_results]
    

'''
========================
Prints program help, if needed.
explanation: an explanation of what the program is.
'''
def print_help(explanation) :
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        print explanation
        print "  Usage: " + sys.argv[0] + " <input file(s)> [<background>] [<options>]"
        print "  If there's a background, the script will plot on top of it."
        print "    Alignment will be handled automatically if image name is recognized."
        print "  Option \"-s\" will return stats instead of plotting."
        print "  Option \"-hi <name>\" will highlight items with this name."
        print "  Option \"-p\" shows a not-to-scale preview of everything."
        print "  Options \"-x\" and \"-y\" offset the image."
        print "  Options \"-w\" and \"-h\" specify the image size."
        sys.exit(1)
        