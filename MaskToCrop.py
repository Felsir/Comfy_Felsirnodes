import torch
import numpy as np
from PIL import Image

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

    FUNCTION = "maktocrop"
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
    return (0,0,0)
    

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)