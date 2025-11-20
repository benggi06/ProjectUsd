import os
from pathlib import Path

from pxr import Usd, UsdLux, UsdShade, Sdf

working_dir = Path(__file__).parent
asset_stage = Usd.Stage.Open(str(working_dir / "street_lamp_dbl.usd"))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

class_prim = asset_stage.CreateClassPrim("/_street_lamp_dbl")
root = asset_stage.GetDefaultPrim()
root.GetInherits().AddInherit(class_prim.GetPath())

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

    
asset_stage.Save()