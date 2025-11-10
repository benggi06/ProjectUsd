# Usd (스테이지)와 UsdGeom (지오메트리) 모듈을 불러온다
from pxr import Usd, UsdGeom

# 저장할 파일 경로를 지정한다
file_path = "_assets/sphere_prim.usda"

# 새 .usda 파일을 만들고 스테이지(작업 공간)를 연다
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# 스테이지의 "/World/Sphere" 경로에 'Sphere' (구) 타입 프림을 정의한다
# (참고: 부모인 /World 프림은 자동으로 'def' 타입으로 생성된다)
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")

# 'sphere' 프림의 'radius' (반지름) 어트리뷰트(속성)를 가져와서(.GetRadiusAttr())
# 그 값을 10으로 설정한다(.Set(10))
sphere.GetRadiusAttr().Set(10)

# 모든 변경 사항을 파일에 저장한다
stage.Save()

# 쉘 창에서 정상작동했는지 확인
print("정상 작동!")