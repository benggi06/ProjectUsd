from pxr import Usd, UsdGeom, Gf

output_filename = 'chair.usda'
stage = Usd.Stage.CreateNew(output_filename)

# 1. '/Chair'라는 이름의 Xform Prim을 정의합니다. (이 파일의 대표)
chair_prim = UsdGeom.Xform.Define(stage, '/Chair')

# 2. 의자 시트 (앉는 부분)
seat_prim = UsdGeom.Cube.Define(stage, '/Chair/Geom/Seat')
# Y=5 높이에 (4, 0.5, 4) 크기의 큐브
UsdGeom.XformCommonAPI(seat_prim).SetTranslate(Gf.Vec3d(0, 5, 0))
UsdGeom.XformCommonAPI(seat_prim).SetScale(Gf.Vec3f(4, 0.5, 4))

# 3. 의자 등받이
back_prim = UsdGeom.Cube.Define(stage, '/Chair/Geom/Back')
# 시트 뒤쪽(Z=-2)에, 시트 상단(Y=5.25)부터 5만큼의 높이(중심 Y=7.75)
UsdGeom.XformCommonAPI(back_prim).SetTranslate(Gf.Vec3d(0, 7.75, -2))
UsdGeom.XformCommonAPI(back_prim).SetScale(Gf.Vec3f(4, 5, 0.5))

# 4. 의자 기둥 (중앙)
post_prim = UsdGeom.Cube.Define(stage, '/Chair/Geom/Post')
# Y=0부터 5까지 (중심 Y=2.5), 얇은 기둥
UsdGeom.XformCommonAPI(post_prim).SetTranslate(Gf.Vec3d(0, 2.5, 0))
UsdGeom.XformCommonAPI(post_prim).SetScale(Gf.Vec3f(0.5, 5, 0.5))

# 5. 의자 바닥 받침
base_prim = UsdGeom.Cube.Define(stage, '/Chair/Geom/Base')
# 바닥(Y=0.25)에 넓게
UsdGeom.XformCommonAPI(base_prim).SetTranslate(Gf.Vec3d(0, 0.25, 0))
UsdGeom.XformCommonAPI(base_prim).SetScale(Gf.Vec3f(3, 0.5, 3))

# 6. [핵심] '/Chair' Prim을 이 파일의 DefaultPrim으로 설정
# .GetPrim()을 사용해야 합니다!
stage.SetDefaultPrim(chair_prim.GetPrim())

# 7. 저장
stage.GetRootLayer().Save()

print(f"'{output_filename}' 에셋 파일이 생성되었습니다.")
print("usdview로 열어서 의자 모양이 잘 만들어졌는지 확인해 보세요.")