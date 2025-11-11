# all.py (최종본)
# 이 스크립트 하나로 참조 파일 생성과 메인 파일 생성을 모두 수행합니다.

import os
from pxr import Usd, UsdGeom, Sdf, Gf, Vt

# --- 1. 참조될 Mesh 큐브 파일 생성 ---
# 스크립트가 실행되는 14_customProperties 폴더 기준
ref_dir = "cubebox_a02"
ref_file_name = "cubebox_a02.usda"
ref_file_path = os.path.join(ref_dir, ref_file_name)

# 폴더가 없으면 생성
if not os.path.exists(ref_dir):
    os.makedirs(ref_dir)

ref_stage = None
try:
    ref_stage = Usd.Stage.CreateNew(ref_file_path)
    root_layer = ref_stage.GetRootLayer() 

    # 1.1 UsdGeom.Mesh로 큐브를 정의
    cube_mesh = UsdGeom.Mesh.Define(ref_stage, "/Cube")

    # 1.2 큐브의 8개 정점(point) 위치 정의
    points = [
        (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
        (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5)
    ]
    cube_mesh.CreatePointsAttr().Set(points)

    # 1.3 큐브의 6개 면(face) 정의
    face_counts = [4, 4, 4, 4, 4, 4]
    cube_mesh.CreateFaceVertexCountsAttr().Set(face_counts)
    face_indices = [
        0, 1, 2, 3,  # +Z (앞)
        4, 5, 6, 7,  # -Z (뒤)
        3, 2, 6, 7,  # +Y (위)
        0, 1, 5, 4,  # -Y (아래)
        1, 5, 6, 2,  # +X (오른쪽)
        0, 4, 7, 3   # -X (왼쪽)
    ]
    cube_mesh.CreateFaceVertexIndicesAttr().Set(face_indices)

    # 1.4 PrimvarsAPI를 사용하여 색상 설정
    primvars = UsdGeom.PrimvarsAPI(cube_mesh)
    display_color_primvar = primvars.CreatePrimvar("displayColor", Sdf.ValueTypeNames.Color3fArray)
    display_color_primvar.Set([Gf.Vec3f(0.4, 0.25, 0.15)])
    display_color_primvar.SetInterpolation(UsdGeom.Tokens.constant)

    # 1.5 defaultPrim 설정
    root_layer.defaultPrim = cube_mesh.GetPrim().GetName()
    
    root_layer.Save() 
    print(f"참조 파일 생성 완료: {ref_file_path}")

finally:
    if ref_stage:
        del ref_stage

        
# --- 2. 메인 파일 생성 및 참조 ---
        
main_dir = "_assets"
main_file_name = "custom_attributes.usda"
main_file_path = os.path.join(main_dir, main_file_name)

# 폴더가 없으면 생성
if not os.path.exists(main_dir):
    os.makedirs(main_dir)
    
main_stage = None
try:
    main_stage = Usd.Stage.CreateNew(main_file_path)

    # 2.1 Prim 계층 정의
    world_xform = UsdGeom.Xform.Define(main_stage, "/World")
    geometry_xform = UsdGeom.Xform.Define(main_stage, world_xform.GetPath().AppendPath("Packages"))
    
    # [핵심 수정] "Box"를 Xform이 아닌 "타입 없는(typeless)" Prim으로 정의합니다.
    box_prim_path = geometry_xform.GetPath().AppendPath("Box")
    box_prim = main_stage.DefinePrim(box_prim_path)

    # 2.2 레퍼런스 추가 (경로는 _assets 폴더 기준)
    # Windows 경로(\)를 USD 경로(/)로 변경
    ref_path_for_ref = os.path.join("..", ref_dir, ref_file_name).replace("\\", "/")
    box_prim.GetReferences().AddReference(ref_path_for_ref)

    # 2.3 커스텀 속성 생성 및 설정
    weight = box_prim.CreateAttribute("acme:weight", Sdf.ValueTypeNames.Float, custom=True)
    category = box_prim.CreateAttribute("acme:category", Sdf.ValueTypeNames.String, custom=True)
    hazard = box_prim.CreateAttribute("acme:hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)
    
    weight.Set(5.5)
    category.Set("Cosmetics")
    hazard.Set(False)
    
    main_stage.Save()
    print(f"메인 파일 생성 완료: {main_file_path}")

finally:
    if main_stage:
        del main_stage

print("\n모든 작업 완료. usdview로 '_assets/custom_attributes.usda' 파일을 확인하세요.")