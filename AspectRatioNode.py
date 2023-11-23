import math
import numpy as np
from PIL import Image

class AspectRatioNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "image_in" : ("IMAGE", {}), 
                "modeltype": (["SD15", "SDXL"],),
                },
            
        }

    RETURN_TYPES = ("FLOAT","INT","INT")
    RETURN_NAMES = ("ratio","width","height")
    FUNCTION = "aspect"
    CATEGORY = "Felsir"

    def aspect(self, image_in,modeltype):      
        image_in = tensor2pil(image_in)
        if image_in.size:
            aspect=float(image_in.size[0]/image_in.size[1])
            totalpixels=1024*1024

            if modeltype=="SDXL":
                if aspect<=(float(640/1536)+float(768/1344))/2:
                    return (aspect,640,1536)
                elif aspect<=(float(768/1344)+float(832/1216))/2:
                    return (aspect,768,1344)
                elif aspect<=(float(832/1216)+float(896/1152))/2:
                    return (aspect,832,1216)
                elif aspect<=(float(896/1152)+float(1024/1024))/2:
                    return (aspect,896,1152)
                elif aspect<=(float(1024/1024)+float(1152/896))/2:
                    return (aspect,1024,1024)
                elif aspect<=(float(1152/896)+float(1216/832))/2:
                    return (aspect,1152,896)
                elif aspect<=(float(1216/832)+float(1344/768))/2:
                    return (aspect,1216,832)
                elif aspect<=(float(1344/768)+float(1536/640))/2:
                    return (aspect,1344,768)
                else:
                    return (aspect,1536,640)
            else:
# Photo	            2:3	    512 × 768
# Photo	            3:4	    512 × 683
# Social Media	    4:5	    512 × 640
# Square	        1:1	    512 × 512
# Standard Monitor	16:9	910 × 512
# Monitor	        16:10	819 × 512
# UltraWide Monitor	21:9	1195 × 512
                if aspect<=(float(512/768)+float(512/683))/2:
                    return (aspect,512,768)
                elif aspect<=(float(512/683)+float(512/640))/2:
                    return (aspect,512,683)
                elif aspect<=(float(512/640)+float(512/512))/2:
                    return (aspect,512,640)
                elif aspect<=(float(512/512)+float(768/512))/2:
                    return (aspect,512,512)
                elif aspect<=(float(640/512)+float(683/512))/2:
                    return (aspect,640,512)
                elif aspect<=(float(683/512)+float(768/512))/2:
                    return (aspect,683,512)
                elif aspect<=(float(768/512)+float(819/512))/2:
                    return (aspect,768,512)
                elif aspect<=(float(819/512)+float(910/512))/2:
                    return (aspect,819,512)
                elif aspect<=(float(910/512)+float(1195/512))/2:
                    return (aspect,910,512)
                else:
                    return (aspect,1195,512)
        else:
            return ( 1, 512, 512)        

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))