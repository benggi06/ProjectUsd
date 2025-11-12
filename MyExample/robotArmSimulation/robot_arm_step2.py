from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.Open("_assets/robot_arm_step1_visual.usda")
if not stage:
    raise RuntimeError("생성된 스테이지가 없습니다.")

stage.SetStartTimeCode(0)
stage.SetEndTimeCode(100) 

print("애니메이션 시간 설정 완료")

arm1_prim_path = "/World/RobotArm/Base/Arm1"
arm2_prim_path = "/World/RobotArm/Base/Arm1/Arm2"

arm1_prim = stage.GetPrimAtPath(arm1_prim_path)
arm2_prim = stage.GetPrimAtPath(arm2_prim_path)

if not arm1_prim:
    raise RuntimeError(f"Prim을 찾을 수 없습니다: {arm1_prim_path}")
if not arm2_prim:
    raise RuntimeError(f"Prim을 찾을 수 없습니다: {arm2_prim_path}")

print("Arm1, Arm2 Prim 찾기 성공.")

# --- Arm1 (Y축 회전) 애니메이션 ---
arm1_xform = UsdGeom.Xformable(arm1_prim)
rotateY_op = arm1_xform.AddRotateYOp()
rotateY_attr = rotateY_op.GetAttr()

print("Arm1 (Y축 회전) 키프레임 설정 중...")
rotateY_attr.Set(0.0, time=0)
rotateY_attr.Set(180.0, time=50)  
rotateY_attr.Set(0.0, time=100)

# --- Arm2 (X축 회전) 애니메이션 ---
arm2_xform = UsdGeom.Xformable(arm2_prim)
rotateX_op = arm2_xform.AddRotateXOp() 
rotateX_attr = rotateX_op.GetAttr()

print("Arm2 (X축 회전) 키프레임 설정 중...")
rotateX_attr.Set(0.0, time=0)
rotateX_attr.Set(-45.0, time=25) 
rotateX_attr.Set(-45.0, time=75)
rotateX_attr.Set(0.0, time=100)

# 4. [수정됨] SaveAs -> Export 로 변경
output_path = "robot_arm_step2.usda"
stage.GetRootLayer().Export(output_path) # <- Export

print(f"'{output_path}' 생성완료")
print("usdview로 열어서 확인해 보세요.")