from .AspectRatioNode import *
from .LatentAspectRatioNode import *
from .FocalRescaleNode import *
from .FocalRescaleRelNode import *
from .RescaleMaintainAspectNode import *
from .FocalPointFromSegsNode import *
from .MaskToCropNode import *

NODE_CLASS_MAPPINGS = { "Aspect from Image" : AspectRatioNode,
                       "Latent Aspect": LatentAspectRatioNode, 
                       "Focal Rescale": FocalRescaleNode,
                       "Focal Rescale Rel": FocalRescaleRelNode,
                       "Rescale Maintain Aspect": RescaleMaintainAspectNode,
                       "Focalpoint from SEGS" : FocalPointFromSegsNode, 
                       "Mask to Crop": MaskToCropNode}

NODE_DISPLAY_NAME_MAPPINGS = { "Aspect from Image" : "AspectRatio",
                               "Aspect for Latent" : "LatentAspectRatio",
                               "Focalpoint Rescale": "FocalRescale",
                               "Focalpoint Rescale Rel": "FocalRescaleRel",
                               "Rescale Maintain Aspect": "RescaleMaintainAspect",
                               "Focalpoint from SEGS": "FocalpointFromSegs",
                               "Mask to Crop": "MaskToCrop"
                               }
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']