import torch
import numpy as np
from PIL import Image

class RescaleMaintainAspectNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "image_in" : ("IMAGE", {}), 
                "width": ("INT",{"default": 512, "min": 16, "max": 2048, "step": 1}),
                "height": ("INT",{"default": 512, "min": 16, "max": 2048, "step": 1}),
                "halign" : (["center", "left", "right"],),
                "valign" : (["center", "top", "bottom"],),
                "fillcolor" : (["black", "white", "transparent"],),
                },
        }

    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "rescalemaintainaspect"
    CATEGORY = "Felsir"

    def rescalemaintainaspect(self, image_in,width,height,halign,valign,fillcolor):      

        tensors = []
        if len(image_in) > 1:
            for img in image_in:
                tensors.append(pil2tensor(recaleimage(tensor2pil(img), width,height,halign,valign,fillcolor)))
            tensors = torch.cat(tensors, dim=0)
        else:
            return (pil2tensor(recaleimage(tensor2pil(image_in), width,height,halign,valign,fillcolor)),)
           
        return (tensors,)


def recaleimage(original_image,new_width,new_height,h_alignment,v_alignment,fillcolor):

    # Calculate the new dimensions while maintaining the aspect ratio
    aspect_ratio = original_image.width / original_image.height
    target_aspect_ratio = new_width / new_height
    
    # Calculate the new dimensions while maintaining the aspect ratio
    if aspect_ratio > target_aspect_ratio:
        # Fit based on width
        result_width = new_width
        result_height = int(new_width / aspect_ratio)
    else:
        # Fit based on height
        result_height = new_height
        result_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_image = original_image.resize((result_width, result_height))

    # Create a new image with the specified dimensions
    result_image = Image.new("RGB", (new_width, new_height), (255, 255, 255))


    # Create a new image with the specified dimensions
    if fillcolor=="black":
        result_image = Image.new("RGB", (new_width, new_height), (0, 0, 0))
    elif fillcolor=="transparent":
        result_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    else:
        result_image = Image.new("RGB", (new_width, new_height), (255, 255, 255))

    # Calculate the position based on the chosen alignment
    if h_alignment == 'center':
        h_position = (new_width - resized_image.width) // 2
    elif h_alignment == 'left':
        h_position = 0
    elif h_alignment == 'right':
        h_position = new_width - resized_image.width
    else:
        raise ValueError("Invalid horizontal alignment. Use 'center', 'left', or 'right'.")

    if v_alignment == 'center':
        v_position = (new_height - resized_image.height) // 2
    elif v_alignment == 'top':
        v_position = 0
    elif v_alignment == 'bottom':
        v_position = new_height - resized_image.height
    else:
        raise ValueError("Invalid vertical alignment. Use 'center', 'top', or 'bottom'.")

    # Paste the resized image onto the new image at the calculated position
    result_image.paste(resized_image, (h_position, v_position))

    # Create a mask
    #mask = Image.new("L", (new_width, new_height), 0)
    #draw = ImageDraw.Draw(mask)
    #draw.rectangle((h_position, v_position, h_position + resized_image.width, v_position + resized_image.height), fill=255)


    return result_image

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)