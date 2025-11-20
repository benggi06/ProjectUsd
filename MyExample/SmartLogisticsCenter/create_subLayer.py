from pxr import Usd, UsdGeom, Sdf

def create_sublayers_demo():
    # ---------------------------------------------------------
    # 1단계: 개별 레이어 파일 만들기 (기초 데이터 채우기)
    # ---------------------------------------------------------
    
    # (1) 건물 레이어 (Layout): 바닥 생성
    layer_layout_path = "layer_layout.usda"
    stage_layout = Usd.Stage.CreateNew(layer_layout_path)
    UsdGeom.SetStageUpAxis(stage_layout, UsdGeom.Tokens.y)
    
    # /World/Building 그룹 생성 및 바닥(Plane) 추가
    building = UsdGeom.Xform.Define(stage_layout, "/World/Building")
    floor = UsdGeom.Mesh.Define(stage_layout, "/World/Building/Floor")
    # (간단히 시각화를 위해 Cube로 바닥 표현)
    floor = UsdGeom.Cube.Define(stage_layout, "/World/Building/Floor_Visual")
    floor.AddScaleOp().Set((20, 0.1, 20)) # 넓고 얇은 바닥
    
    stage_layout.SetDefaultPrim(stage_layout.GetPrimAtPath("/World"))
    stage_layout.GetRootLayer().Save()
    print(f"✅ 생성 완료: {layer_layout_path}")


    # (2) 설비 레이어 (Equipment): 로봇이 놓일 위치 표시
    layer_equip_path = "layer_equipment.usda"
    stage_equip = Usd.Stage.CreateNew(layer_equip_path)
    UsdGeom.SetStageUpAxis(stage_equip, UsdGeom.Tokens.y)
    
    # /World/Equipment 그룹 생성
    equip_grp = UsdGeom.Xform.Define(stage_equip, "/World/Equipment")
    
    # 여기에 나중에 로봇 등을 배치할 것임 (지금은 빈 그룹)
    stage_equip.SetDefaultPrim(stage_equip.GetPrimAtPath("/World"))
    stage_equip.GetRootLayer().Save()
    print(f"✅ 생성 완료: {layer_equip_path}")


    # (3) 조명 레이어 (Lighting)
    layer_light_path = "layer_lighting.usda"
    stage_light = Usd.Stage.CreateNew(layer_light_path)
    UsdGeom.SetStageUpAxis(stage_light, UsdGeom.Tokens.y)
    
    # /World/Lights 그룹 생성
    light_grp = UsdGeom.Xform.Define(stage_light, "/World/Lights")
    
    stage_light.SetDefaultPrim(stage_light.GetPrimAtPath("/World"))
    stage_light.GetRootLayer().Save()
    print(f"✅ 생성 완료: {layer_light_path}")


    # ---------------------------------------------------------
    # 2단계: 메인 파일에서 합치기 (SubLayering)
    # ---------------------------------------------------------
    main_stage_path = "main.usda"
    stage_main = Usd.Stage.CreateNew(main_stage_path)
    UsdGeom.SetStageUpAxis(stage_main, UsdGeom.Tokens.y)
    
    root_layer = stage_main.GetRootLayer()
    
    # 중요: 서브레이어 추가 (순서 중요!)
    # 리스트의 앞쪽이 더 강한 의견(Opinion)을 가집니다.
    # 여기서는 Lighting(가장 위) -> Equipment -> Layout(가장 아래) 순서로 쌓습니다.
    root_layer.subLayerPaths = [
        layer_light_path,
        layer_equip_path,
        layer_layout_path
    ]
    
    stage_main.Save()
    print(f"\n🎉 최종 합성 완료: {main_stage_path}")
    print("usdview로 main.usda 파일을 열어보세요!")

if __name__ == "__main__":
    create_sublayers_demo()