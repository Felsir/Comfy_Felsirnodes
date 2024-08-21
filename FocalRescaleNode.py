import torch
import numpy as np
from PIL import Image

class FocalRescaleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "image_in" : ("IMAGE", {}), 
                "width": ("INT",{"default": 512, "min": 16, "max": 2048, "step": 1}),
                "height": ("INT",{"default": 512, "min": 16, "max": 2048, "step": 1}),
                "focalx": ("INT",{"default": 256, "step": 1}),
                "focaly": ("INT",{"default": 256, "step": 1}),
                },
        }

    RETURN_TYPES = ("IMAGE","INT","INT","INT","INT")
    RETURN_NAMES = ("IMAGE","rect_left","rect_top","rect_width","rect_height")

    FUNCTION = "focalrescale"
    CATEGORY = "Felsir"

    def focalrescale(self, image_in,width,height,focalx,focaly,coverage,fit_inside):      

        tensors = []
        if len(image_in) > 1:
            for img in image_in:
                image, x,y, w, h = focalrecaleimage(tensor2pil(image_in), width,height,focalx,focaly,coverage,fit_inside)
                tensors.append(pil2tensor(image,),x,y,w,h)
            tensors = torch.cat(tensors, dim=0)
        else:
            image, x,y, w, h = focalrecaleimage(tensor2pil(image_in), width,height,focalx,focaly,coverage,fit_inside)
            return (pil2tensor(image,),x,y,w,h)
           
        return (tensors,)


def focalrecaleimage(original_image,new_width,new_height,focalx,focaly):


    # Get the size of the original image
    image_width, image_height = original_image.size

    target_aspect_ratio=new_width/new_height

    # Calculate the rectangle with the target aspect ratio
    rect_left, rect_top, rect_width, rect_height = calculate_rectangle(
        image_width, image_height, target_aspect_ratio
    )


    # Position the rectangle to have the focalpoint in the center
    rect_left = focalx - rect_width//2
    rect_top = focaly - rect_height//2
    rect_right = rect_left+rect_width
    rect_bottom = rect_top+rect_height

#    # Check if the focal point is outside the calculated rectangle
#    if focalx < rect_left or focalx > rect_left + rect_width:
#        # Adjust the rectangle horizontally
#        rect_left = max(0, min(image_width - rect_width, focalx - rect_width / 2))
#
#    if focaly < rect_top or focaly > rect_top + rect_height:
#        # Adjust the rectangle vertically
#        rect_top = max(0, min(image_height - rect_height, focaly - rect_height / 2))


    # Adjust the rectangle to ensure it is entirely inside the image

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


def focalrecaleimage2(original_image,width,height,focalx,focaly):

        # Get the size of the original image
        original_width, original_height = original_image.size

        # Calculate the aspect ratio of the original image
        original_aspect_ratio = original_width / original_height

        # Calculate the aspect ratio of the target size
        target_aspect_ratio = width / height

        # Calculate the dimensions for scaling
        if original_aspect_ratio > target_aspect_ratio:
            # Scale based on width
            scaled_width = width
            scaled_height = int(width / original_aspect_ratio)
        else:
            # Scale based on height
            scaled_height = height
            scaled_width = int(height * original_aspect_ratio)

        # Resize the image to the scaled dimensions
        scaled_image = original_image.resize((scaled_width, scaled_height))

        # Calculate the cropping box around the focal point
        left = max(0, focalx - width // 2)
        top = max(0, focaly - height // 2)
        right = min(scaled_width, left + width)
        bottom = min(scaled_height, top + height)

        # Crop the image around the focal point
        cropped_image = scaled_image.crop((left, top, right, bottom))

        # Create a blank canvas with the target size
        output_image = Image.new('RGB', (width, height), (0, 0, 0))

        # Paste the cropped image onto the canvas at the original position
        output_image.paste(cropped_image, (left, top))

        # Save the result to the output path
        return output_image 
        #out_image = (pil2tensor(output_image) if original_image else image_in)

def calculate_rectangle(image_width, image_height, target_aspect_ratio):
    # Calculate the dimensions of the rectangle with the target aspect ratio
    if image_width / image_height > target_aspect_ratio:
        # Fit based on width
        rect_width = min(image_width, int(image_height * target_aspect_ratio))
        rect_height = min(image_height, int(rect_width / target_aspect_ratio))
    else:
        # Fit based on height
        rect_height = min(image_height, int(image_width / target_aspect_ratio))
        rect_width = min(image_width, int(rect_height * target_aspect_ratio))

    # Calculate the coordinates of the top-left corner of the rectangle
    rect_left = (image_width - rect_width) // 2
    rect_top = (image_height - rect_height) // 2

    return rect_left, rect_top, rect_width, rect_height
    

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)