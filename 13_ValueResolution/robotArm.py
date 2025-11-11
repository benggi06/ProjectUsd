from pxr import Usd, UsdGeom, Gf

# === 1. base.usda 파일 생성 시작 (로봇 팔 모양으로) ===
print("base.usda 생성 중 (상세 버전)...")

stage_base = Usd.Stage.CreateNew('base.usda')
stage_base.SetDefaultPrim(stage_base.DefinePrim('/RobotArm', 'Xform'))
arm_prim_base = stage_base.GetPrimAtPath('/RobotArm')

# 루트 /RobotArm의 기본 위치는 여전히 (0, 0, 0)입니다.
xform_api_base = UsdGeom.XformCommonAPI(arm_prim_base)
xform_api_base.SetTranslate((0, 0, 0))

# --- 실제 "로봇 팔" 모양 만들기 ---
# (이전 큐브 1개 대신, 2개의 큐브를 조립합니다)

# 1. "상박" (UpperArm) - Y축으로 길쭉한 주황색 큐브
upper_arm_prim = UsdGeom.Cube.Define(stage_base, '/RobotArm/UpperArm')
# XformCommonAPI를 사용해 크기(scale)와 위치(translate) 조정
upper_arm_xform = UsdGeom.XformCommonAPI(upper_arm_prim.GetPrim())
upper_arm_xform.SetScale((0.5, 2.0, 0.5)) # (x, y, z) - Y축으로 길게
upper_arm_xform.SetTranslate((0, 1, 0))    # Y축으로 1만큼 올려서 바닥(0)에서 시작
# 색상 설정
upper_arm_prim.GetDisplayColorAttr().Set([Gf.Vec3f(1.0, 0.5, 0.2)]) # 주황색

# 2. "하박" (ForeArm) - Y축으로 조금 더 길쭉한 회색 큐브
fore_arm_prim = UsdGeom.Cube.Define(stage_base, '/RobotArm/ForeArm')
fore_arm_xform = UsdGeom.XformCommonAPI(fore_arm_prim.GetPrim())
fore_arm_xform.SetScale((0.4, 2.5, 0.4))   # 상박보다 약간 가늘고 길게
fore_arm_xform.SetTranslate((0, 3.25, 0)) # 상박의 끝(Y=2) 위에 배치
# 색상 설정
fore_arm_prim.GetDisplayColorAttr().Set([Gf.Vec3f(0.5, 0.5, 0.5)]) # 회색

# ------------------------------------

# 변경 사항을 파일로 저장합니다.
stage_base.Save()
print(f"'{stage_base.GetRootLayer().identifier}' 파일이 생성되었습니다.")


# === 2. anim.usda 파일 생성 시작 (이전 코드와 100% 동일) ===
print("\nanim.usda 생성 중...")

stage_anim = Usd.Stage.CreateNew('anim.usda')
stage_anim.GetRootLayer().subLayerPaths.append('./base.usda')

# /RobotArm Prim의 속성을 덮어쓰겠다고 '선언'
arm_prim_anim = stage_anim.OverridePrim('/RobotArm')

# (5,0,0)으로 값을 '덮어씁니다'.
# ★★★ 중요 ★★★
# 우리는 /RobotArm의 위치만 덮어썼습니다.
# /RobotArm/UpperArm 이나 /RobotArm/ForeArm은 건드리지 않았습니다.
xform_api_anim = UsdGeom.XformCommonAPI(arm_prim_anim)
xform_api_anim.SetTranslate((5, 0, 0))

stage_anim.Save()
print(f"'{stage_anim.GetRootLayer().identifier}' 파일이 생성되었습니다.")

print("\n모든 파일 생성이 완료되었습니다.")