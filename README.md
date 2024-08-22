# Comfy_Felsirnodes

My set of custom nodes for **Comfyui** interface mainly for interacting with images and image sizes.

1. A set of nodes to create base latent spaces with the max dimensions for SD15 and SDXL.
2. A set of nodes for cropping and resizing images with the best aspect ratios
3. Focal point rescaling using SEGS data to determine the best focal point.

Note; these nodes do not use Stable Diffusion for imagescaling, but regular image scaling. This is intended as pre- or post processing of images.

## Installation

1. Open a terminal or command line interface.
2. Navigate to the `ComfyUI/custom_nodes/` directory.
3. Run the following command:
```git clone https://github.com/Felsir/Comfy_Felsirnodes.git```
4. Restart ComfyUI.

This command clones the repository into your `ComfyUI/custom_nodes/` directory. You should now be able to access and use the nodes from this repository.

## Use
You can find the nodes under the `Add Node` submenu `Felsir`. *This might change in the future, to have the nodes (likely) under the image submenu.* 

## Focalpoint Rescale
This node rescales the input image in a new width/height, while keeping a focal point inside the image. The aspect ratio of the image contents is not changed. 
The process is as follows; the target aspect ratio is determined based on the new width and height- next the maximum rectangle is determined to fit inside the original image with the found aspect ratio. 
Next the rectangle is moved to have the focalpoint in the center. If that pushes the edges of the rectangle outside of the image bounds, the rectangle is moved inside the image.
Finally that rectangle is cropped and scaled to the new width and height.

### Examples
Scale the image, while keeping the moon inside the frame. The moon is located at 600,100 in the original image.

Scale the image to a new size of 800x200:
![Horzontal focal point rescale](https://github.com/Felsir/Comfy_Felsirnodes/blob/main/examples/focalpoint-horizontal.png)

Scale the image to a new size of 512x768: 
![Vertcial focal point rescale](https://github.com/Felsir/Comfy_Felsirnodes/blob/main/examples/focalpoint-vertical.png)

### Intended use
Normal scaling between aspects either distorts the image or crops the image unintentionally. The focal point method provides an easy way to control the cropping and getting the maximum out of the source image.

## Focalpoint Rescale Relative
This node crop a rectangular sub-window in the target image, ensuring the generated image has a fixed height and width.  
It is possible to specify via `fit_inside` what to do in case the sub-window is not fully covered by the original image.  

The coordinates of the focal point are specified relative to height and width.  
Coverage determines the radius of the circle built around the rectangular sub-window. Its scale is either the height or the width of the original image, whichever is smaller.

### Intended use
This node can be used standalone as an alternative to `Focalpoint Rescale` with more control over the cropping process.  
It is also meant to work alongside `MaskToCrop` to perform batch cropping automatically.

## Focalpoint from SEGS Node
This node determines the focalpoint based on SEGS input by averaging the centerpoints of each detected node.

### Example
The source image is fed into a face detection node, the output of this node is used to create a new image and :
![Detecting focal point from image with faces](https://github.com/Felsir/Comfy_Felsirnodes/blob/main/examples/focalpoint-segsaverage.png)

### Intended use
By detecting the face and feeding this in the focalpoint rescale node, you can automatically detect the focalpoint and generate images in the aspect ratios of your choice.

## Mask to Crop
Use the mask information of an image to crop the relevant portion of space from the original image.

## Rescale Maintain Aspect Node
This node rescales an image while keeping the source node aspect ratio in tact. It finds the maximum size for the source image within the new width/height and fills the empty space with either black or white.

### Example
The source controlnet image is rescaled to match the intended imagesize. In order to keep the proportions the node is used. The stick figure is aligned to the bottom, any space is filled in with a black color:
![Rescaling a image filling the remaining area black](https://github.com/Felsir/Comfy_Felsirnodes/blob/main/examples/rescalemaintainaspect.png)

### Intended use
Often a rescale means distortion of the source material. This node works great for depthmaps or controlnet nodes by keeping the aspect ratio of the source and fitting it as best as possible in the new space.

## Latent Aspect Node
This node outputs the ratio, width and height for a given model (SD1.5 or SDXL) as in the following table:

|Name|Aspect|SD15|SDXL|
|-|-|-|-|
|Vertical|9:16|512x768|768x1344|
|Photo|4:3|683x512|1152x896|
|Portrait|4:5|512x640|836x1254|
|Square|1:1|512x512|1024x1024|
|Landscape|3:2|819x512|1216x832|
|Widescreen|16:9|910x512|1344x768|
|Cinematic|21:9|1195x512|1536x640|

### Intended use
Use this as a source for a empty latent or scale latent node width and height. Ofcourse anything else that wold need a width or height could benefit from this node. Set this as the 'base value' for other nodes to use.

## Aspect Ratio Node
This node reads the aspect from a image input, then finds the nearest match for a SD15 or SDXL latent. The aspects chosen will be one from the table as in the Latent Aspect Node above.

### Example
Create a latent for SDXL with the aspect close to the source image:
![Aspect from image](https://github.com/Felsir/Comfy_Felsirnodes/blob/main/examples/aspectrationfromimage.png)
The endresult will be a latent that utilizes the maximum usable area.

### Intended use
This enables you to pick a latent that is closest to the source image. Useful for creating a new latent where you want to reuse components from a source image.








