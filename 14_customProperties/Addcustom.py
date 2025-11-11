from pxr import Usd, Sdf, UsdGeom # Sdf, UsdGeom 추가

# 메모리상에 새로운 USD 스테이지를 생성합니다.
stage = Usd.Stage.CreateInMemory()
# '/ExamplePrim' 경로에 'Xform' 타입의 Prim을 정의합니다.
prim = stage.DefinePrim("/ExamplePrim", "Xform")

# 'my_namespace:serial_number'라는 이름으로 'String' 타입의 속성을 생성합니다.
# 'custom=True': 이 속성이 USD 표준 스키마가 아닌, 사용자 정의 속성임을 명시합니다.
# 'my_namespace:': 표준 속성과의 이름 충돌을 방지하기 위한 네임스페이스입니다.
serial_num_attr = prim.CreateAttribute("my_namespace:serial_number", Sdf.ValueTypeNames.String, custom=True)

# 방금 생성한 속성이 'custom' 속성인지 확인합니다. (True여야 함)
assert serial_num_attr.IsCustom()

# 'my_namespace:maintenance_date'라는 두 번째 사용자 정의 속성을 생성합니다.
mtce_date_attr = prim.CreateAttribute("my_namespace:maintenance_date", Sdf.ValueTypeNames.String, custom=True)

# 'serial_number' 속성에 문자열 값을 설정합니다.
serial_num_attr.Set("qt6hfg23")
# 'maintenance_date' 속성에 문자열 값을 설정합니다.
mtce_date_attr.Set("20241004")

# .Get()을 사용하여 속성 값을 가져와 출력합니다.
print(f"Serial Number: {serial_num_attr.Get()}")
print(f"Last Maintenance Date: {mtce_date_attr.Get()}")