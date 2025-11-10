from pxr import Usd, UsdGeom, UsdLux, UsdShade

file_path = "_assets/distant_light.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# 기본 구조 생성 (World Xform 및 Geometry Scope)
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# 조명을 담을 Scope 생성 ("/World/Lights")
# Scope는 씬(Scene)을 논리적으로 그룹화하는 데 유용한 컨테이너 역할을 합니다.
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Lights"))

# DistantLight(원거리 조명) Prim 생성 ("/World/Lights/SunLight")
# 태양처럼 아주 멀리서 오는 평행한 빛을 표현할 때 사용됩니다.
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("SunLight"))

# (선택 사항) 조명 강도 및 각도 설정 예시
# distant_light.GetIntensityAttr().Set(5000) # 조명 강도 설정
# distant_light.GetAngleAttr().Set(0.53)     # 태양의 각도(크기) 설정 (그림자의 부드러움에 영향)

stage.Save()

print("정상 작동")