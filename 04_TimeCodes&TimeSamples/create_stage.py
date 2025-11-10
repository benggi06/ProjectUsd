# pxr 라이브러리에서 Usd, UsdGeom(지오메트리), Gf(벡터/행렬) 모듈을 불러온다
from pxr import Usd, UsdGeom, Gf

# "_assets/timecode_sample.usda" 이름으로 새 스테이지(작업 공간)를 만든다
stage: Usd.Stage = Usd.Stage.CreateNew("_assets/timecode_sample.usda")

# 스테이지 최상위에 "/World" 경로로 Xform(트랜스폼) 프림을 정의한다
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# "/World" 프림의 자식으로 "Sphere" (구) 프림을 정의한다
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# "/World" 프림의 자식으로 "Backdrop" (Cube 타입) 프림을 정의한다 (배경용)
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))

# "Backdrop" 프림의 디스플레이 색상(displayColor)을 (0,0,1) (파란색)으로 설정한다
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])

# "Backdrop" 프림에 Xform(변환)을 적용하기 위한 API를 가져온다
cube_xform_api = UsdGeom.XformCommonAPI(box)

# "Backdrop" 프림의 스케일(크기)을 (5, 5, 0.1)로 설정 (넓고 얇게)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))

# "Backdrop" 프림의 위치(translate)를 (0, 0, -2)로 설정 (뒤로 2만큼)
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

# 모든 변경 사항을 파일에 저장한다
stage.Save()