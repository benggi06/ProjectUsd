# 'UsdGeom' 모듈을 추가로 import 합니다. 
# UsdGeom은 구, 큐브 등 기하학적 Prim(모델)을 다루는 모듈입니다.
from pxr import Usd, UsdGeom

# 1. 아까 만들었던 '빈 무대' 파일 경로
file_path = "_assets/first_stage.usda"

# 2. CreateNew() 대신 Open()으로 기존 스테이지를 엽니다.
stage = Usd.Stage.Open(file_path)

# 3. 스테이지에 Prim을 정의(Define)합니다.
# 경로: /hello/world
# 먼저 '/hello'라는 빈 Xform(그룹용) Prim을 만듭니다.
xformPrim = UsdGeom.Xform.Define(stage, '/hello')

# '/hello' Prim 안에 '/world'라는 이름의 Sphere(구) Prim을 만듭니다.
spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')

# 4. stage.Save()를 호출하여 모든 변경사항을 파일에 저장합니다.
stage.Save()

# 5. (Optional) 변경된 파일 내용을 콘솔에 출력해봅니다.
print("--- Stage Content (After Adding Prims) ---")
print(stage.ExportToString(addSourceFileComment=False))