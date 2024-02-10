from collections import namedtuple

class FocalPointFromSegsNode:
    
    SEG = namedtuple("SEG",
                 ['cropped_image', 'cropped_mask', 'confidence', 'crop_region', 'bbox', 'label', 'control_net_wrapper'],
                 defaults=[None])
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "segs" : ("SEGS", {}), 
                },
        }

    RETURN_TYPES = ("INT","INT","INT","INT","INT","INT","INT","INT")
    RETURN_NAMES = ("X","Y","MinX","MaxX","MinY","MaxY","Width","Height")

    FUNCTION = "focalpointfromsegs"
    CATEGORY = "Felsir"

    def focalpointfromsegs(self, segs):      

        #initialize:
        x=0
        y=0
        c=0
        minx=9999
        miny=9999
        maxx=0
        maxy=0

        # Loop through each SEGS object
        for seg in segs[1]:
            #Add all X and Y coordinates
            x += (seg.crop_region[0]+seg.crop_region[2])
            y += (seg.crop_region[1]+seg.crop_region[3])
            #Keep track of the number we've seen
            c += 2

            if(seg.crop_region[0]<minx):
                minx=seg.crop_region[0]

            if(seg.crop_region[2]>maxx):
                maxx=seg.crop_region[2]

            if(seg.crop_region[1]<miny):
                miny=seg.crop_region[1]

            if(seg.crop_region[3]>maxy):
                maxy=seg.crop_region[3]

            #print(seg.crop_region[0],";",seg.crop_region[1],"-",seg.crop_region[1],";",seg.crop_region[3])

        #if there was at least one SEGS model, average the x and y coordinates:   
        if(c>0):
            x = x//c
            y = y//c

        #print(x)
        #print(y)

        return (x,y,minx,maxx,miny,maxy,maxx-minx,maxy-miny)
