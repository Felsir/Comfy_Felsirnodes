class LatentAspectRatioNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "modeltype": (["SD15", "SDXL"],),
                "aspect" : (["Vertical", "Photo", "Portrait","Square","Landscape","Widescreen","Cinematic"],),
                },
            
        }

    RETURN_TYPES = ("FLOAT","INT","INT")
    RETURN_NAMES = ("ratio","width","height")
    FUNCTION = "latentaspect"
    CATEGORY = "Felsir"

    def latentaspect(self, modeltype,aspect):      

        if modeltype=="SDXL":
            if aspect == "Vertical":
                return (float(9/16),768,1344)
            elif aspect =="Portrait":
                return (float(4/5),836,1254)
            elif aspect =="Square":
                return (float(1),1024,1024)
            elif aspect =="Photo":
                return (float(4/3),1152,896)
            elif aspect =="Landscape":
                return (float(3/2),1216,832)
            elif aspect =="Widescreen":
                return (float(16/9),1344,768)
            elif aspect =="Cinematic":
                return (float(21/9),1536,640)                                
            else:
                return (float(1),1024,1024)
        else:
            if aspect == "Vertical":
                return (float(2/3),512,768)
            elif aspect =="Photo":
                return (float(4/3),683,512)
            elif aspect =="Portrait":
                return (float(4/5),512,640)
            elif aspect =="Square":
                return (float(1),512,512)
            elif aspect =="Widescreen":
                return (float(16/9),910,512)
            elif aspect =="Landscape":
                return (float(16/10),819,512)
            elif aspect =="Cinematic":
                return (float(21/9),1195,512)                                
            else:
                return (1,512,512)
