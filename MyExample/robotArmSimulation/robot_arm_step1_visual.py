from pxr import Usd, UsdGeom, Gf

# 1. 새 스테이지 생성 (시각화 버전)
output_filename = 'robot_arm_step1_visual.usda'
stage = Usd.Stage.CreateNew(output_filename)

# 2. /World Prim 정의
world_prim = UsdGeom.Xform.Define(stage, '/World')

# 3. 로봇 팔 계층 구조 정의
robot_prim = UsdGeom.Xform.Define(stage, '/World/RobotArm')
base_prim = UsdGeom.Xform.Define(stage, '/World/RobotArm/Base')

# --- 'Base'에 시각화 '살' 붙이기 ---
# Base 관절 위치에 짧고 넓은 캡슐을 추가합니다.
base_geom_path = '/World/RobotArm/Base/Geom'
base_capsule = UsdGeom.Capsule.Define(stage, base_geom_path)
base_capsule.GetRadiusAttr().Set(1.5)
base_capsule.GetHeightAttr().Set(1.0)
base_capsule.GetAxisAttr().Set(UsdGeom.Tokens.y) # Y축(위) 방향

# --- 'Arm1' 관절 및 '살' 붙이기 ---
# Arm1 관절(Xform) 정의
arm1_prim = UsdGeom.Xform.Define(stage, '/World/RobotArm/Base/Arm1')
# Arm1 관절의 위치 설정 (Base로부터 Y로 2만큼 위)
UsdGeom.XformCommonAPI(arm1_prim).SetTranslate(Gf.Vec3d(0, 2, 0))

# Arm1의 '살' (Capsule) 정의
arm1_geom_path = '/World/RobotArm/Base/Arm1/Geom'
arm1_capsule_prim = UsdGeom.Capsule.Define(stage, arm1_geom_path)
arm1_capsule = UsdGeom.Capsule(arm1_capsule_prim)
arm1_capsule.GetRadiusAttr().Set(0.5)
arm1_capsule.GetHeightAttr().Set(5.0) # 이 캡슐의 '길이' (다음 관절까지의 거리)
arm1_capsule.GetAxisAttr().Set(UsdGeom.Tokens.y)
# [중요] 캡슐은 중앙이 (0,0,0)입니다. 관절(Arm1) 위치에서 위로 뻗어나가도록
# 캡슐 자체를 '높이의 절반'만큼 Y축으로 이동시킵니다. (5.0 / 2 = 2.5)
UsdGeom.XformCommonAPI(arm1_capsule_prim).SetTranslate(Gf.Vec3d(0, 2.5, 0))

# --- 'Arm2' 관절 및 '살' 붙이기 ---
# Arm2 관절(Xform) 정의
arm2_prim = UsdGeom.Xform.Define(stage, '/World/RobotArm/Base/Arm1/Arm2')
# Arm2 관절의 위치 설정 (Arm1으로부터 Y로 5만큼 위)
UsdGeom.XformCommonAPI(arm2_prim).SetTranslate(Gf.Vec3d(0, 5, 0))

# Arm2의 '살' (Capsule) 정의
arm2_geom_path = '/World/RobotArm/Base/Arm1/Arm2/Geom'
arm2_capsule_prim = UsdGeom.Capsule.Define(stage, arm2_geom_path)
arm2_capsule = UsdGeom.Capsule(arm2_capsule_prim)
arm2_capsule.GetRadiusAttr().Set(0.4) # 조금 더 가늘게
arm2_capsule.GetHeightAttr().Set(3.0) # 다음 관절(Gripper)까지의 거리
arm2_capsule.GetAxisAttr().Set(UsdGeom.Tokens.y)
# 높이(3.0)의 절반(1.5)만큼 Y축 이동
UsdGeom.XformCommonAPI(arm2_capsule_prim).SetTranslate(Gf.Vec3d(0, 1.5, 0))

# --- 'Gripper' 관절 및 '살' 붙이기 ---
# Gripper 관절(Xform) 정의
gripper_prim = UsdGeom.Xform.Define(stage, '/World/RobotArm/Base/Arm1/Arm2/Gripper')
# Gripper 관절의 위치 설정 (Arm2로부터 Y로 3만큼 위)
UsdGeom.XformCommonAPI(gripper_prim).SetTranslate(Gf.Vec3d(0, 3, 0))

# Gripper의 '살' (Sphere) 정의. 집게 대신 간단한 구(Sphere)로 표현합니다.
gripper_geom_path = '/World/RobotArm/Base/Arm1/Arm2/Gripper/Geom'
gripper_sphere = UsdGeom.Sphere.Define(stage, gripper_geom_path)
gripper_sphere.GetRadiusAttr().Set(0.8)

# 4. 스테이지 저장
stage.GetRootLayer().Save()
print(f"'{output_filename}' 파일이 생성되었습니다.")
print("usdview로 이 파일을 열어보세요. 이제 로봇 팔이 보일 것입니다!")