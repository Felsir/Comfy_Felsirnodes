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

    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("X","Y")

    FUNCTION = "focalpointfromsegs"
    CATEGORY = "Felsir"

    def focalpointfromsegs(self, segs):      

        x=0
        y=0
        c=0

        for seg in segs[1]:
            x += (seg.crop_region[0]+seg.crop_region[2])
            y += (seg.crop_region[1]+seg.crop_region[3])
            c += 2
            print(seg.crop_region[0],";",seg.crop_region[1],"-",seg.crop_region[1],";",seg.crop_region[3])
           
        if(c>0):
            x = x//c
            y = y//c

        print(x)
        print(y)

        return (x,y)
