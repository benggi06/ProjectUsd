import os
from pathlib import Path

from pxr import Usd, UsdGeom, Sdf


working_dir = Path(__file__).parent
scenario2 = Usd.Stage.Open(str(working_dir / "scenario_02.usd"))

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

class_prim = scenario2.OverridePrim("/_osm_street_data")
max_speed_attr = class_prim.CreateAttribute("osm:street:maxspeed", Sdf.ValueTypeNames.Int, custom=True)
max_speed_attr.Set(40)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

scenario2.Save()
