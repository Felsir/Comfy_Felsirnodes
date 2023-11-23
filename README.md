# Comfy_Felsirnodes

My set of custom nodes for **Comfyui** interface mainly for interacting with images and image sizes.

## Focalpoint Rescale
This node rescales the input image while keeping a focal point inside the image. The aspect ratio of the image contents is not changed. 

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

### intended use
Use this as a source for a empty latent or scale latent node width and height. Ofcourse anything else that wold need a width or height could benefit from this node. Set this as the 'base value' for other nodes to use.

## Aspect Ratio Node
This node reads the aspect from a image input, then finds the nearest match for a SD15 or SDXL latent. The aspects chosen will be one from the table as in the Latent Aspect Node above.

### intended use
This enables you to pick a latent that is closest to the source image. Useful for creating a new latent where you want to reuse components from a source image.








