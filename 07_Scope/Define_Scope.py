# pxr 라이브러리에서 Usd, UsdGeom 모듈을 불러온다
from pxr import Usd, UsdGeom

# "_assets/scope.usda" 파일 경로에 새 스테이지를 만든다
file_path = "_assets/scope.usda"
stage = Usd.Stage.CreateNew(file_path)

# 스테이지 최상위에 "/World"라는 이름의 Xform 프림을 정의한다
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# "/World" 프림을 이 스테이지의 기본 프림(Default Prim)으로 설정한다
# (다른 씬에서 이 파일을 참조할 때 기본적으로 로드될 프림을 지정하는 것이다)
stage.SetDefaultPrim(world.GetPrim())

# "/World" 아래에 "Geometry"라는 이름의 Scope 프림을 정의한다
# Scope는 트랜스폼(이동/회전/크기) 없이 자식들을 단순히 그룹화하는 용도이다
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Geometry"))

# "Geometry" 스코프 아래에 "Cube"라는 이름의 Cube(상자) 프림을 정의한다
# 실제 경로는 "/World/Geometry/Cube"가 된다
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# 변경 사항을 파일에 저장한다
stage.Save()

# 쉘에서 작동여부 확인
print("정상 작동")