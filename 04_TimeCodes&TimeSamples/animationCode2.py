from pxr import Usd, UsdGeom, Gf

# "timecode_sample.usda" 파일을 스테이지로 '연다' (Open)
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

# 'sphere' 프림의 기존 'translate' 값을 지운다 (키프레임 설정을 위해)
if translate_attr := sphere.GetTranslateOp().GetAttr():
    translate_attr.Clear()
# 'sphere' 프림의 기존 'scale' 값을 지운다
if scale_attr := sphere.GetScaleOp().GetAttr():
    scale_attr.Clear()

# 'sphere' 프림에 Xform(변환)을 적용하기 위한 API를 가져온다
sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

# 'sphere'의 위치(translate) 값을 'TimeCode'별로 설정한다
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)  

# --- (새로운 부분) ---
# 'sphere'의 스케일(scale) 값을 'TimeCode'별로 설정한다
# time=1 (기본 크기)
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=1)  
# time=30 (기본 크기)
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=30)  
# time=45 (Y축으로 납작하게, Z축으로 넓게 찌그러짐)
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 0.20, 1.25), time=45)  
# time=50 (Y축으로 길쭉하게, X/Z축으로 얇게 늘어남)
sphere_xform_api.SetScale(Gf.Vec3f(0.75, 2.00, 0.75), time=50)  
# time=60 (기본 크기)
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=60)  

# 현재 스테이지의 모든 내용을 새 파일로 '내보낸다' (Export)
stage.Export("_assets/timecode_ex2b.usda", addSourceFileComment=False)