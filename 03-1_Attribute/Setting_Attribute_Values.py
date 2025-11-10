from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex3.usda"

# 해당 경로에 usda 파일을 만들고 스테이지를 연다.
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# 스테이지 최상위에 Xform 타입의 /World 프림을 정의
world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# /World의 자식으로 Sphere와 Cube를 정의
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))

#  Cube 프림에 traslate 값을 (5, 0, 0)으로 설정
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5,0,0))

# 애트리뷰트 리스트에 있는 Cube 크기, 색상, 넓이 객체를 가져옴
cube_size: Usd.Attribute = cube.GetSizeAttr()
cube_displaycolor: Usd.Attribute = cube.GetDisplayColorAttr()
cube_extent: Usd.Attribute = cube.GetExtentAttr()

# 해당 객체의 실제 값을 가져와서 Set메소드로 변경, 
cube_size.Set(cube_size.Get() * 2)
cube_extent.Set(cube_extent.Get() * 2)
# displaycolor는 3차원의 RGB값 적용
cube_displaycolor.Set([(0.0, 1.0, 0.0)])

stage.Save()