from math import pi
from pxr import Gf, Usd, UsdGeom, UsdLux

file_path = "_assets/light_props.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# 지오메트리를 담을 Scope와 기본 Cube 생성
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geom_scope.GetPath().AppendPath("Box"))

# 조명을 담을 Scope 생성 ("/Lights")
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Lights")

# --- DistantLight (태양광) 설정 ---
# "/Lights/Sun" 경로에 DistantLight 생성
distant_light = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("Sun"))

# 색상 설정: 빨간색 (RGB: 1.0, 0.0, 0.0)
distant_light.GetColorAttr().Set(Gf.Vec3f(1.0, 0.0, 0.0))
# 강도 설정: 120.0
distant_light.GetIntensityAttr().Set(120.0)

# 회전 설정: X축으로 45도 회전하여 빛의 방향 변경
# (DistantLight는 위치보다 회전이 중요합니다.)
if not (xform_api := UsdGeom.XformCommonAPI(distant_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
xform_api.SetRotate((45.0, 0.0, 0.0))
xform_api = None # 재사용을 위해 변수 초기화 (필수는 아님)

# --- SphereLight (구형 조명) 설정 ---
# "/Lights/SphereLight" 경로에 SphereLight 생성
sphere_light = UsdLux.SphereLight.Define(stage, lights_scope.GetPath().AppendPath("SphereLight"))

# 색상 설정: 파란색 (RGB: 0.0, 0.0, 1.0)
sphere_light.GetColorAttr().Set(Gf.Vec3f(0.0, 0.0, 1.0))
# 강도 설정: 50000.0 (SphereLight는 거리에 따라 감쇠하므로 높은 값이 필요할 수 있음)
sphere_light.GetIntensityAttr().Set(50000.0)

# 위치 설정: (5.0, 10.0, 0.0)으로 이동
# (SphereLight는 점 광원이므로 위치가 중요합니다.)
if not (xform_api := UsdGeom.XformCommonAPI(sphere_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
xform_api.SetTranslate((5.0, 10.0, 0.0))

stage.Save()

print("정상 작동")