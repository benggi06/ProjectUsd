# Usd, UsdGeom(지오메트리), Gf(벡터/행렬) 모듈을 불러온다
from pxr import Usd, UsdGeom, Gf

# 이전에 만들었던 "timecode_sample.usda" 파일을 스테이지로 '연다' (Open)
stage: Usd.Stage = Usd.Stage.Open("_assets/timecode_sample.usda")

# (참고: 아래 프림들은 이미 파일에 존재하므로, Define은 프림을 '가져오는' 역할을 한다)
# "/World" Xform 프림을 가져온다
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# "/World/Sphere" 프림을 가져온다
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# "/World/Backdrop" 큐브 프림을 가져온다
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))

# Backdrop 프림의 색상을 파란색으로 (다시) 설정한다
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])

# Backdrop 프림의 Xform API를 가져온다
cube_xform_api = UsdGeom.XformCommonAPI(box)

# Backdrop 프림의 스케일을 (다시) 설정한다
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))

# Backdrop 프림의 위치를 (다시) 설정한다
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

# 이 스테이지(씬)의 '시작 시간'을 1 프레임으로 설정한다
stage.SetStartTimeCode(1)

# 이 스테이지(씬)의 '종료 시간'을 60 프레임으로 설정한다
stage.SetEndTimeCode(60)

# 현재 스테이지의 모든 내용을 '플래튼(flatten)'하여 새 파일로 '내보낸다' (Export)
# addSourceFileComment=False 는 원본 파일 경로 주석을 남기지 않는 옵션이다
stage.Export("_assets/timecode_ex1.usda", addSourceFileComment=False)