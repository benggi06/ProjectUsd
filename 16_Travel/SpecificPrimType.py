# pxr 패키지에서 Usd (핵심) 및 UsdGeom (지오메트리 스키마) 모듈을 임포트합니다.
from pxr import Usd, UsdGeom

# 지정된 USD 파일을 스테이지(Stage)로 엽니다.
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# Scope 타입 프리미티브의 개수를 세기 위한 변수
scope_count = 0
# Xform 타입 프리미티브의 개수를 세기 위한 변수
xform_count = 0

# stage.Traverse()를 사용해 스테이지의 모든 (활성화된) 프리미티브를 순회합니다.
for prim in stage.Traverse():
    
    # 이 프리미티브가 'Scope' 타입인지 확인합니다.
    # UsdGeom.Scope(prim)는 'prim'이 Scope 스키마를 따를 경우 유효한 객체를,
    # 아니면 'None'과 유사한 falsy 객체를 반환합니다.
    if UsdGeom.Scope(prim):
        # Scope 타입이 맞다면, 카운터를 1 증가시킵니다.
        scope_count += 1
        # 해당 프리미티브의 이름을 "Scope Type: "과 함께 출력합니다.
        print("Scope Type: ", prim.GetName())
        
    # Scope가 아니라면, 'Xform' 타입인지 확인합니다.
    # (Xform은 변환(transform) 노드를 의미합니다.)
    elif UsdGeom.Xform(prim):
        # Xform 타입이 맞다면, 카운터를 1 증가시킵니다.
        xform_count +=1
        # 해당 프리미티브의 이름을 "Xform Type: "과 함께 출력합니다.
        print("Xform Type: ", prim.GetName())

# 순회가 끝난 후, 발견된 Scope 프리미티브의 총 개수를 출력합니다.
print("Number of Scope prims: ", scope_count)
# 발견된 Xform 프리미티브의 총 개수를 출력합니다.
print("Number of Xform prims: ", xform_count)