import torch
import numpy as np
from PIL import Image
import math

class MaskToCrop:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "mask_in" : ("MASK", {}),
                },
        }

    RETURN_TYPES = ("FLOAT","FLOAT","FLOAT")
    RETURN_NAMES = ("focal_x","focal_y","coverage")

    FUNCTION = "masktocrop"
    CATEGORY = "Felsir"

    def masktocrop(self, mask_in):      

        tensors = []
        if len(mask_in) > 1:
            for mask in mask_in:
                tensors.append()
            tensors = torch.cat(tensors, dim=0)
        else:
            return op(mask_in)
           
        return (tensors,)


def op(mask_in):
    width = mask_in.shape[2]
    height = mask_in.shape[1]
    center = [ np.average(indices) for indices in np.where(mask_in >= 0.5   ) ]
    variance = [ np.var(indices) for indices in np.where(mask_in >= 0.5   ) ]
    varx = math.sqrt(variance[2]/width/width)
    vary = math.sqrt(variance[1]/height/height)
    # Use the variance to determine an approximation of the zoom level needed.
    return (center[2]/width,center[1]/height,min(1,2*max(varx,vary)*max(width/height,height/width)))
    

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)