# Usd, UsdGeom(지오메트리), Gf(벡터/행렬) 모듈을 불러온다
from pxr import Usd, UsdGeom, Gf

# 이전에 만든 "timecode_sample.usda" 파일을 스테이지로 '연다' (Open)
stage: Usd.Stage = Usd.Stage.Open("_assets/timecode_sample.usda")

# (파일에 이미 프림이 있으므로, Define은 프림을 '가져오는' 역할을 한다)
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))

# (Backdrop 프림 설정 - 이전과 동일)
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

# 스테이지의 '시작 시간'을 1로, '종료 시간'을 60으로 설정한다
stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)

# 'sphere' 프림의 'translate'(이동) 어트리뷰트를 가져온다
if translate_attr := sphere.GetTranslateOp().GetAttr():
    # 만약 어트리뷰트에 기존 값이 있다면, 모든 값을 '지운다' (Clear)
    # (TimeSample을 설정하기 전에 기본값을 청소하는 것이 좋다)
    translate_attr.Clear()

# 'sphere' 프림에 Xform(변환)을 적용하기 위한 API를 가져온다
sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

# 'sphere'의 위치(translate) 값을 'TimeCode'별로 설정한다 (키프레임 생성)
# time=1 (시작 프레임)
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)  
# time=30 (중간 프레임)
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)  
# time=45
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)  
# time=50
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)  
# time=60 (종료 프레임)
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)  

# 현재 스테이지의 모든 내용을 새 파일로 '내보낸다' (Export)
stage.Export("_assets/timecode_ex2a.usda", addSourceFileComment=False)