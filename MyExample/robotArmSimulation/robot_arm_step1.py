from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.CreateNew('robot_arm_step1.usda')

world_prim = UsdGeom.Xform.Define(stage, "/World")

robot_prim = UsdGeom.Xform.Define(stage, "/World/RobotArm")

base_prim = UsdGeom.Xform.Define(stage,"/World/RobotArm/Base")

arm1_prim = UsdGeom.Xform.Define(stage,"/World/RobotArm/Base/Arm1")
arm2_prim = UsdGeom.Xform.Define(stage,"/World/RobotArm/Base/Arm1/Arm2")
gripper_prim = UsdGeom.Xform.Define(stage,"/World/RobotArm/Base/Arm1/Arm2/Gripper")

UsdGeom.XformCommonAPI(arm1_prim).SetTranslate(Gf.Vec3d(0, 2, 0))
UsdGeom.XformCommonAPI(arm2_prim).SetTranslate(Gf.Vec3d(0, 5, 0))
UsdGeom.XformCommonAPI(gripper_prim).SetTranslate(Gf.Vec3d(0, 3, 0))

stage.GetRootLayer().Save()
print("robot_arm_step1.usda 생성완료")