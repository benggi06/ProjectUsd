# 파일 경로: 14_customProperties/creatingCustomAttr.py

import os
from pxr import Usd, UsdGeom, Sdf

# --- 파일 경로 설정 ---
ref_dir = "cubebox_a02"
ref_file_name = "cubebox_a02.usda" # .usda를 참조

main_dir = "_assets"
main_file_name = "custom_attributes.usda"
main_file_path = os.path.join(main_dir, main_file_name)

# _assets 폴더가 없으면 생성
if not os.path.exists(main_dir):
    os.makedirs(main_dir)

stage: Usd.Stage = Usd.Stage.CreateNew(main_file_path)

# --- Prim 계층 정의 ---
world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Packages"))

# [핵심 수정] '스키마 불일치' 해결
# Box를 Xform이 아닌 "타입 없는(typeless)" Prim으로 정의합니다.
# 이렇게 해야 참조된 Mesh 타입이 이 Prim의 타입이 될 수 있습니다.
box_prim_path = geometry_xform.GetPath().AppendPath("Box")
box_prim = stage.DefinePrim(box_prim_path) 
# -------------------------

# [핵심 수정] 경로 수정
# _assets 폴더 기준으로, 상위 폴더(../)로 올라간 다음 cubebox_a02로 내려갑니다.
ref_path_for_ref = os.path.join("..", ref_dir, ref_file_name).replace("\\", "/")
box_prim.GetReferences().AddReference(ref_path_for_ref)

# --- 커스텀 속성 생성 (사용자 코드와 동일) ---
weight = box_prim.CreateAttribute("acme:weight", Sdf.ValueTypeNames.Float, custom=True)
category = box_prim.CreateAttribute("acme:category", Sdf.ValueTypeNames.String, custom=True)
hazard = box_prim.CreateAttribute("acme:hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

weight.SetDocumentation("The weight of the package in kilograms.")
category.SetDocumentation("The shopping category for the products this package contains.")
hazard.SetDocumentation("Whether this package contains hazard materials.")

weight.Set(5.5)
category.Set("Cosmetics")
hazard.Set(False)

# --- 스테이지 저장 ---
stage.Save()
print(f"메인 파일 생성 완료: {main_file_path}")

if stage:
    del stage