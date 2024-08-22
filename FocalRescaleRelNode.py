import torch
import numpy as np
from PIL import Image
import math

class FocalRescaleRelNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "image_in" : ("IMAGE", {}), 
                "width": ("INT",{"default": 512, "min": 16, "max": 2048, "step": 1}),
                "height": ("INT",{"default": 512, "min": 16, "max": 2048, "step": 1}),
                "focal_x": ("FLOAT",{"default": 0.5, "min": 0, "max": 1, "step": 0.05}),
                "focal_y": ("FLOAT",{"default": 0.5, "min": 0, "max": 1, "step": 0.05}),
                "coverage": ("FLOAT",{"default": 0.5, "min": 0, "max": 1, "step": 0.05}),
                "fit_inside": ("BOOLEAN",{"default": False}),
                },
        }

    RETURN_TYPES = ("IMAGE","INT","INT","INT","INT")
    RETURN_NAMES = ("IMAGE","rect_left","rect_top","rect_width","rect_height")

    FUNCTION = "focalrescalerel"
    CATEGORY = "Felsir"

    def focalrescalerel(self, image_in,width,height,focal_x,focal_y,coverage,fit_inside):      

        tensors = []
        if len(image_in) > 1:
            for img in image_in:
                image, x,y, w, h = focalrecaleimage(tensor2pil(image_in), width,height,focal_x,focal_y,coverage,fit_inside)
                tensors.append(pil2tensor(image,),x,y,w,h)
            tensors = torch.cat(tensors, dim=0)
        else:
            image, x,y, w, h = focalrecaleimage(tensor2pil(image_in), width,height,focal_x,focal_y,coverage,fit_inside)
            return (pil2tensor(image,),x,y,w,h)
           
        return (tensors,)


def focalrecaleimage(original_image,new_width,new_height,focal_x,focal_y,coverage,fit_inside):


    # Get the size of the original image
    image_width, image_height = original_image.size

    target_aspect_ratio=new_width/new_height

    # Calculate the rectangle with the target aspect ratio
    #rect_left, rect_top, rect_width, rect_height = calculate_rectangle(
    #    image_width, image_height, coverage, target_aspect_ratio
    #)
    
    if image_height < image_width:
        rect_width = coverage*image_height*target_aspect_ratio
        rect_height = coverage*image_height

    if image_height >= image_width:
        rect_width = coverage*image_width
        rect_height = coverage*image_width/target_aspect_ratio

    # Position the rectangle to have the focalpoint in the center
    rect_left = focal_x*image_width - rect_width//2
    rect_top = focal_y*image_height - rect_height//2
    rect_right = rect_left+rect_width
    rect_bottom = rect_top+rect_height

    # Adjust the rectangle to ensure it is entirely inside the image
    if fit_inside:
        if(rect_left<0):
            rect_left = 0
            rect_right = rect_width

        if(rect_right>image_width):
            rect_right = image_width
            rect_left = rect_right-rect_width

        if(rect_top<0):
            rect_top = 0
            rect_bottom = rect_height

        if(rect_bottom>image_height):
            rect_bottom = image_height
            rect_top = rect_bottom-rect_height

        rect_left = max(0, rect_left)
        rect_top = max(0, rect_top)
        rect_right = min(image_width, rect_left + rect_width)
        rect_bottom = min(image_height, rect_top + rect_height)

    # Crop the image using the adjusted rectangle
    cropped_image = original_image.crop((rect_left, rect_top, rect_right, rect_bottom))


    # Resize the cropped image to the new size
    resized_image = cropped_image.resize(size=(new_width,new_height))

    return (resized_image, rect_left, rect_top, rect_width, rect_height,)    

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)