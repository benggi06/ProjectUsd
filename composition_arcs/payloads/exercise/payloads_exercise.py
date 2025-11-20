import os
from pathlib import Path

from pxr import Usd, UsdGeom, Gf

working_dir = Path(__file__).parent
stage = Usd.Stage.CreateNew(str(working_dir / "city.usda"))
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

UsdGeom.Xform.Define(stage, "/World")

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_01")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_02")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform_api = UsdGeom.XformCommonAPI(xform)
xform_api.SetTranslate(Gf.Vec3d(180, 0, 0))
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_03")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform_api = UsdGeom.XformCommonAPI(xform)
xform_api.SetTranslate(Gf.Vec3d(340, 0, 0))

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


stage.Save()
