from pxr import Usd, UsdGeom, Gf

output_filename = 'desk.usda'
stage = Usd.Stage.CreateNew(output_filename)

# 1. '/Desk'라는 이름의 Xform Prim을 정의합니다.
# 이 Prim이 이 파일의 '대표(Default)'가 될 것입니다.
desk_prim = UsdGeom.Xform.Define(stage, '/Desk')

# 2. 책상 윗판 (Cube)
top_prim = UsdGeom.Cube.Define(stage, '/Desk/Geom/Top')
top_prim.GetSizeAttr().Set(10.0) # 10x10 크기
# 윗판을 얇고 넓게 만듭니다. (X, Y, Z 스케일)
UsdGeom.XformCommonAPI(top_prim).SetScale(Gf.Vec3f(1.0, 0.2, 2.0))

# 3. 책상 다리 (Cube 4개)
# 간단하게 4개의 큐브를 만들어 위치(Translate)와 크기(Scale)를 조절합니다.
leg1_prim = UsdGeom.Cube.Define(stage, '/Desk/Geom/Leg1')
UsdGeom.XformCommonAPI(leg1_prim).SetTranslate(Gf.Vec3d(4, -2.5, 8))
UsdGeom.XformCommonAPI(leg1_prim).SetScale(Gf.Vec3f(0.5, 5.0, 0.5))

leg2_prim = UsdGeom.Cube.Define(stage, '/Desk/Geom/Leg2')
UsdGeom.XformCommonAPI(leg2_prim).SetTranslate(Gf.Vec3d(-4, -2.5, 8))
UsdGeom.XformCommonAPI(leg2_prim).SetScale(Gf.Vec3f(0.5, 5.0, 0.5))

leg3_prim = UsdGeom.Cube.Define(stage, '/Desk/Geom/Leg3')
UsdGeom.XformCommonAPI(leg3_prim).SetTranslate(Gf.Vec3d(4, -2.5, -8))
UsdGeom.XformCommonAPI(leg3_prim).SetScale(Gf.Vec3f(0.5, 5.0, 0.5))

leg4_prim = UsdGeom.Cube.Define(stage, '/Desk/Geom/Leg4')
UsdGeom.XformCommonAPI(leg4_prim).SetTranslate(Gf.Vec3d(-4, -2.5, -8))
UsdGeom.XformCommonAPI(leg4_prim).SetScale(Gf.Vec3f(0.5, 5.0, 0.5))

# 4. [핵심] '/Desk' Prim을 이 파일의 DefaultPrim으로 설정
stage.SetDefaultPrim(desk_prim.GetPrim())

# 5. 저장
stage.GetRootLayer().Save()

print(f"'{output_filename}' 에셋 파일이 생성되었습니다.")