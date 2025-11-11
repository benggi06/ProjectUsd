# 파일 경로: 14_customProperties/cubebox_a02/create_cube.py

import os
from pxr import Usd, UsdGeom, Sdf, Gf, Vt

ref_file_name = "cubebox_a02.usda" # .usda (ASCII)로 저장합니다.
ref_stage = None 

try:
    ref_stage = Usd.Stage.CreateNew(ref_file_name)
    root_layer = ref_stage.GetRootLayer() 

    # 1. UsdGeom.Mesh로 큐브를 정의 (UsdGeom.Cube 렌더링 문제를 우회)
    cube_mesh = UsdGeom.Mesh.Define(ref_stage, "/Cube")

    # 2. 큐브의 8개 정점(point) 위치 정의
    points = [
        (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
        (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5)
    ]
    cube_mesh.CreatePointsAttr().Set(points)

    # 3. 큐브의 6개 면(face) 정의
    face_counts = [4, 4, 4, 4, 4, 4]
    cube_mesh.CreateFaceVertexCountsAttr().Set(face_counts)
    
    # 4. 각 면이 사용할 정점 인덱스 정의
    face_indices = [
        0, 1, 2, 3,  # +Z (앞)
        4, 5, 6, 7,  # -Z (뒤)
        3, 2, 6, 7,  # +Y (위)
        0, 1, 5, 4,  # -Y (아래)
        1, 5, 6, 2,  # +X (오른쪽)
        0, 4, 7, 3   # -X (왼쪽)
    ]
    cube_mesh.CreateFaceVertexIndicesAttr().Set(face_indices)

    # 5. PrimvarsAPI를 사용하여 색상 설정
    primvars = UsdGeom.PrimvarsAPI(cube_mesh)
    display_color_primvar = primvars.CreatePrimvar("displayColor", Sdf.ValueTypeNames.Color3fArray)
    display_color_primvar.Set([Gf.Vec3f(0.4, 0.25, 0.15)])
    display_color_primvar.SetInterpolation(UsdGeom.Tokens.constant)

    # 6. defaultPrim 설정 (defaultPrim 누락 문제 해결)
    root_layer.defaultPrim = cube_mesh.GetPrim().GetName()
    
    root_layer.Save() 
    print(f"참조 파일 생성 완료: {ref_file_name}")

finally:
    if ref_stage:
        del ref_stage