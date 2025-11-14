from pxr import Usd, UsdGeom, Gf, Sdf

output_filename = 'office_layout.usda'
stage = Usd.Stage.CreateNew(output_filename)

# 1. 씬의 루트 Prim들을 정의합니다.
world_prim = UsdGeom.Xform.Define(stage, '/World')
office_prim = UsdGeom.Xform.Define(stage, '/World/Office')

print("메인 오피스 씬을 생성합니다...")

# --- 첫 번째 책상 세트 배치 ---

# 2. 첫 번째 책상을 놓을 '위치' Prim을 정의합니다.
desk1_prim_path = '/World/Office/DeskSet_01'
desk1_prim = UsdGeom.Xform.Define(stage, desk1_prim_path) 

# 3. .GetPrim()을 사용해 '참조' 추가
desk1_prim.GetPrim().GetReferences().AddReference(assetPath='./desk.usda')

# 4. 불러온 책상의 위치/회전 설정 (이건 XformAPI라 .GetPrim() 불필요)
UsdGeom.XformCommonAPI(desk1_prim).SetTranslate(Gf.Vec3d(15, 0, 10))
UsdGeom.XformCommonAPI(desk1_prim).SetRotate(Gf.Vec3f(0, 45, 0)) 

# 5. [핵심 수정] .GetPrim()을 사용해 '속성' 추가
desk1_prim.GetPrim().CreateAttribute(
    'asset:id', Sdf.ValueTypeNames.String
).Set('DESK-001')

print("DeskSet_01에 'desk.usda'를 참조하고 ID 'DESK-001'을 할당했습니다.")


# --- (선택) 의자도 배치하기 ---
# chair.usda 파일을 만드셨다면, 이 부분의 주석을 해제하고 실행하세요.

chair1_prim_path = '/World/Office/DeskSet_01/Chair' 
chair1_prim = UsdGeom.Xform.Define(stage, chair1_prim_path)
# [수정됨] .GetPrim() 추가
chair1_prim.GetPrim().GetReferences().AddReference(assetPath='./chair.usda')
UsdGeom.XformCommonAPI(chair1_prim).SetTranslate(Gf.Vec3d(0, 0, 4))
# [수정됨] .GetPrim() 추가
chair1_prim.GetPrim().CreateAttribute('asset:id', Sdf.ValueTypeNames.String).Set('CHAIR-001')
print("DeskSet_01에 'chair.usda'를 참조하고 ID 'CHAIR-001'을 할당했습니다.")


# --- 두 번째 책상 세트 배치 (복사) ---

# 6. 두 번째 책상을 놓을 위치 Prim을 정의합니다.
desk2_prim_path = '/World/Office/DeskSet_02'
desk2_prim = UsdGeom.Xform.Define(stage, desk2_prim_path)

# 7. .GetPrim()을 사용해 '참조' 추가
desk2_prim.GetPrim().GetReferences().AddReference(assetPath='./desk.usda')

# 8. 두 번째 책상의 위치를 설정합니다.
UsdGeom.XformCommonAPI(desk2_prim).SetTranslate(Gf.Vec3d(-15, 0, 10))
# [핵심 수정] .GetPrim()을 사용해 '속성' 추가
desk2_prim.GetPrim().CreateAttribute('asset:id', Sdf.ValueTypeNames.String).Set('DESK-002')

print("DeskSet_02에 'desk.usda'를 참조하고 ID 'DESK-002'를 할당했습니다.")

# 9. 저장
stage.GetRootLayer().Save()

print(f"'{output_filename}' (조립 파일)이 생성되었습니다.")