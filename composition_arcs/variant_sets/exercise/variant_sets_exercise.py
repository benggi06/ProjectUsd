import os
from pathlib import Path

from pxr import Usd, UsdLux, UsdShade, Sdf


def toggle_lights(on: bool):
    if on:
        intensity = 100.0
        emissive_color = (1.0, 1.0, 1.0)
    else:
        intensity = 0.0
        emissive_color = (0.0, 0.0, 0.0)
    
    lights_scope = stage.GetPrimAtPath("/World/Lights")
    for prim in Usd.PrimRange(lights_scope):
        if prim.HasAPI(UsdLux.LightAPI):
            light_api = UsdLux.LightAPI(prim)
            light_api.GetIntensityAttr().Set(intensity)
    
    prim = stage.GetPrimAtPath("/World/Looks/light/light")
    shader = UsdShade.Shader(prim)
    shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set(emissive_color)



working_dir = Path(__file__).parent
stage = Usd.Stage.Open(str(working_dir / "street_lamp_dbl.usd"))


root = stage.GetDefaultPrim()

# PART 1
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

vset: Usd.VariantSet = root.GetVariantSets().AddVariantSet("lights")
vset.AddVariant("on")
vset.AddVariant("off")

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE




# PART 2
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

vset.SetVariantSelection("on")
with vset.GetVariantEditContext():
    toggle_lights(True)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE




# PART 3
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

vset.SetVariantSelection("off")
with vset.GetVariantEditContext():
    toggle_lights(False)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
    


# Make sure you select the variant you intend to select for this layer.
# Alternatively, you can use Usd.VariantSet.ClearVariantSelection()
# if you would prefer to not make a selection in the current EditTarget.
vset.SetVariantSelection("off")

stage.GetRootLayer().Export(str(working_dir / "street_lamp_dbl_vset.usda"))

