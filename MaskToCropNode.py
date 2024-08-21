import torch
import numpy as np
from PIL import Image
import math
from .FocalRescaleRelNode import *

class MaskToCropNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "image_in" : ("IMAGE", {}),
                "mask_in" : ("MASK", {}),
                "resolution": ("INT",{"default": 512, "min": 16, "max": 2048, "step": 1}),
                "fit_inside": ("BOOLEAN",{"default": False}),
                "force_square": ("BOOLEAN",{"default": True}),
                "padding": ("INT",{"default": 0, "min": 0, "step": 1}),
                },
        }

    RETURN_TYPES = ("IMAGE","INT","INT","INT","INT")
    RETURN_NAMES = ("IMAGE","rect_left","rect_top","rect_width","rect_height")

    FUNCTION = "masktocrop"
    CATEGORY = "Felsir"

    def masktocrop(self, image_in, mask_in, resolution, fit_inside, force_square, padding):      

        tensors = []
        if len(image_in) > 1:
            for idx,img in enumerate(image_in):
                image, x,y, w, h = op(tensor2pil(img),mask_in[idx] if len(mask_in)> 1 else mask_in,resolution, fit_inside, force_square, padding)
                tensors.append(pil2tensor(image,),x,y,w,h)
            tensors = torch.cat(tensors, dim=0)
        else:
            image, x,y, w, h =  op(tensor2pil(image_in),mask_in,resolution, fit_inside, force_square, padding)
            return (pil2tensor(image,),x,y,w,h)
           
        return (tensors,)


def op(original_image,mask_in, resolution, fit_inside, force_square, padding):
    width = mask_in.shape[2]
    height = mask_in.shape[1]
    center = [ np.average(indices) for indices in np.where(mask_in >= 0.5   ) ]

    limits_min = [ np.min(indices) for indices in np.where(mask_in >= 0.5   ) ]
    limits_max = [ np.max(indices) for indices in np.where(mask_in >= 0.5   ) ]
    coverage = (limits_max[2]-limits_min[2]+padding)/width if width<height else (limits_max[1]-limits_min[1]+padding)/height
    if force_square==True:
        return focalrecaleimage(original_image,resolution,resolution,center[2]/width,center[1]/height,coverage,fit_inside)

    ratio = (limits_max[2]-limits_min[2]+padding)/ (limits_max[1]-limits_min[1]+padding)
    if ratio>1:
        return focalrecaleimage(original_image,resolution,int(resolution/ratio),center[2]/width,center[1]/height,coverage,fit_inside)
    else:
        return focalrecaleimage(original_image,int(resolution/ratio),resolution,center[2]/width,center[1]/height,coverage,fit_inside)
    #variance = [ np.var(indices) for indices in np.where(mask_in >= 0.5   ) ]
    #varx = math.sqrt(variance[2]/width/width)
    #vary = math.sqrt(variance[1]/height/height)
    # Use the variance to determine an approximation of the zoom level needed.
    #return (resolution,resolution,center[2]/width,center[1]/height,coverage)
    

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)