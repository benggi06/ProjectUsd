import os
from pathlib import Path

from pxr import Usd, UsdLux, UsdShade, Sdf

working_dir = Path(__file__).parent

scenario2 = Usd.Stage.Open(str(working_dir / "scenario_02.usd"))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

class_prim = scenario2.OverridePrim("/_street_lamp_dbl")
light_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Lights/sphere_light_01"))
light = UsdLux.LightAPI(light_prim)
light.CreateColorAttr((0.5, 0.4, 0.1))
light_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Lights/sphere_light_02"))
light = UsdLux.LightAPI(light_prim)
light.CreateColorAttr((0.5, 0.4, 0.1))
shader_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Looks/light/light"))
shader = UsdShade.Shader(shader_prim)
shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set((0.5, 0.4, 0.1))

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


scenario2.Save()
