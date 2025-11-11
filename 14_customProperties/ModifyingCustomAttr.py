# 필요한 USD 모듈 임포트
from pxr import Usd, UsdGeom, Sdf

# 수정할 USD 파일 경로
file_path = "_assets/custom_attributes.usda"
# USD 파일을 '스테이지(Stage)'로 열기
stage: Usd.Stage = Usd.Stage.Open(file_path)
# "/World/Packages/Box" 경로에 있는 프리미티브(Prim) 가져오기
box_prim = stage.GetPrimAtPath("/World/Packages/Box")

# 'acme:weight'라는 이름의 속성(Attribute)을 가져오기
weight_attr: Usd.Attribute = box_prim.GetAttribute("acme:weight")
# 'weight_attr' 속성의 값을 4.25로 설정 (변경)
weight_attr.Set(4.25)

# 'weight_attr' 속성의 현재 값을 가져와서 출력
print("Weight of Box:", weight_attr.Get())

# 스테이지에 적용된 모든 변경 사항을 원본 파일에 저장
stage.Save()