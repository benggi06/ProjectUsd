from pxr import Usd, UsdGeom

# 생성할 USD 파일의 경로를 지정합니다.
file_path = "_assets/xformcommonapi.usda"

# 지정된 경로에 새로운 USD 스테이지(파일)를 생성합니다.
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# 스테이지에 '/Cone'이라는 경로로 원뿔(Cone) Prim을 정의(생성)합니다.
cone: UsdGeom.Cone = UsdGeom.Cone.Define(stage, "/Cone")

# 스테이지에 '/Cube'라는 경로로 정육면체(Cube) Prim을 정의(생성)합니다.
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, "/Cube")

# 원뿔의 디스플레이 색상을 설정합니다 (RGB 값).
cone.GetDisplayColorAttr().Set([(1.0, 0.5, 0.25)])

# 원뿔 프림에 Y축 애트리뷰트 추가
cone.CreateAxisAttr("Y")

# 원뿔 Prim의 변환(이동, 회전, 크기)을 쉽게 조작하기 위해 XformCommonAPI 객체를 생성합니다.
cone_xform_api = UsdGeom.XformCommonAPI(cone)

# API를 사용하여 원뿔의 크기를 모든 축에서 절반(0.5)으로 줄입니다.
cone_xform_api.SetScale((0.5, 0.5, 0.5))

# API를 사용하여 원뿔의 위치를 Y축으로 1.5만큼 이동시킵니다.
cone_xform_api.SetTranslate((0.0, 1.5, 0.0))

# 스테이지의 변경 사항을 실제 파일로 저장합니다.
stage.Save()

# 정상 작동 여부
print("정상 작동")