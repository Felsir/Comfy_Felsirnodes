from .AspectRatioNode import *
from .LatentAspectRatioNode import *
from .FocalRescaleNode import *
from .RescaleMaintainAspectNode import *
from .FocalPointFromSegsNode import *

NODE_CLASS_MAPPINGS = { "Aspect from Image" : AspectRatioNode,
                       "Latent Aspect": LatentAspectRatioNode, 
                       "Focal Rescale": FocalRescaleNode,
                       "Rescale Maintain Aspect": RescaleMaintainAspectNode,
                       "Focalpoint from SEGS" : FocalPointFromSegsNode, }

NODE_DISPLAY_NAME_MAPPINGS = { "Aspect from Image" : "AspectRatio",
                               "Aspect for Latent" : "LatentAspectRatio",
                               "Focalpoint Rescale": "FocalRescale",
                               "Rescale Maintain Aspect": "RescaleMaintainAspect",
                               "Focalpoint from SEGS": "FocalpointFromSegs",
                               }
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']