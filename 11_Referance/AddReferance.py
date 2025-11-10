from pxr import Usd, UsdGeom, Gf

# --- 첫 번째 파일 (cube.usda) 생성 ---
file_path = "_assets/cube.usda"
stage = Usd.Stage.CreateNew(file_path)

# '/Cube' 경로에 정육면체(Cube) 생성
cube = UsdGeom.Cube.Define(stage, "/Cube")

# 이 파일의 기본(Default) Prim을 '/Cube'로 설정
# (다른 파일에서 이 파일을 참조할 때 기본적으로 불러와질 Prim)
stage.SetDefaultPrim(cube.GetPrim())
stage.Save()

# --- 두 번째 파일 (shapes.usda) 생성 ---
second_file_path = "_assets/shapes.usda"
stage = Usd.Stage.CreateNew(second_file_path)

# '/World' 그룹(Xform) 생성
world = UsdGeom.Xform.Define(stage, "/World")
# '/World/Sphere' 경로에 구(Sphere) 생성
UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# --- 참조(Reference) 추가 ---
# '/World/Cube_Ref'라는 빈 Prim 생성 (참조를 담을 그릇)
reference_prim = stage.DefinePrim(world.GetPath().AppendPath("Cube_Ref"))

# 이 Prim에 방금 만든 'cube.usda' 파일을 참조로 추가
# (cube.usda의 Default Prim인 '/Cube'가 이 위치로 불러와짐)
reference_prim.GetReferences().AddReference("./cube.usda")

# 참조된 큐브를 X축으로 5만큼 이동 (원점의 구와 겹치지 않게)
UsdGeom.XformCommonAPI(reference_prim).SetTranslate(Gf.Vec3d(5, 0, 0))

stage.Save()

print("정상 작동")