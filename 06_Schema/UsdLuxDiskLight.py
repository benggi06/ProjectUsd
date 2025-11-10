# Usd, UsdGeom(지오메트리), UsdLux(조명), Gf(벡터/행렬), Sdf(경로/타입) 모듈을 불러온다
from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf

# 저장할 파일 경로를 지정한다
file_path = "_assets/lux_example.usda"
# 새 .usda 파일을 만들고 스테이지(작업 공간)를 연다
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# --- 1. 씬 구성 (빛을 받을 물체들) ---
# 스테이지 최상위에 "/World" Xform 프림을 정의한다
world_xform = UsdGeom.Xform.Define(stage, "/World")

# 바닥 역할을 할 거대한 Plane(Mesh)을 정의한다 (간단히 Cube를 납작하게 만듦)
ground = UsdGeom.Cube.Define(stage, "/World/Ground")
ground.AddTranslateOp().Set(Gf.Vec3d(0, -1, 0))  # 약간 아래로 이동
ground.AddScaleOp().Set(Gf.Vec3f(10, 0.1, 10))   # 넓고 얇게 스케일 조절
ground.GetDisplayColorAttr().Set([(0.5, 0.5, 0.5)]) # 회색으로 설정

# 빛을 반사할 Sphere(구)를 중앙에 정의한다
sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")
sphere.GetRadiusAttr().Set(1.0)
sphere.AddTranslateOp().Set(Gf.Vec3d(0, 1, 0))   # 바닥 위로 약간 올림
sphere.GetDisplayColorAttr().Set([(0.8, 0.2, 0.2)]) # 빨간색으로 설정

# --- 2. 조명 (Disk Light) 설정 ---
# "/World/Lights/DiskLight" 경로에 Disk Light(원형 조명) 프림을 정의한다
# (중간 경로인 /World/Lights 는 자동으로 Xform 등으로 생성된다)
disk_light = UsdLux.DiskLight.Define(stage, "/World/Lights/DiskLight")

# 조명의 위치와 방향을 설정한다 (XformCommonAPI 사용)
# 위쪽(Y=5)에서 아래를 비추도록 설정한다. (X축 기준 -90도 회전)
UsdGeom.XformCommonAPI(disk_light).SetTranslate(Gf.Vec3d(3, 5, 0))
UsdGeom.XformCommonAPI(disk_light).SetRotate(Gf.Vec3f(-120, 0, 0))

# DiskLight 스키마에 포함된 모든 속성(Attribute) 이름들을 가져온다 (확인용)
dl_attribute_names = disk_light.GetSchemaAttributeNames()
# print(dl_attribute_names) # 필요하면 주석 해제하여 출력 확인

# 'intensity' (빛의 강도)를 1000으로 설정한다. (기본값보다 훨씬 밝게)
disk_light.GetIntensityAttr().Set(100) # 더 잘 보이도록 2000으로 상향 조정했습니다.
# 'radius' (조명의 크기)를 설정한다. 크기가 클수록 그림자가 부드러워진다.
disk_light.GetRadiusAttr().Set(2.0)

# 모든 변경 사항을 파일에 저장한다
stage.Save()

# 쉘 창에서 정상작동했는지 확인
print("정상 작동!")