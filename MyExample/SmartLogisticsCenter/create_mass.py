from pxr import Usd, UsdGeom, Sdf

def create_mass_production_demo():
    # ---------------------------------------------------------
    # 1단계: 자산(Asset) 만들기 - '표준 선반'
    # ---------------------------------------------------------
    asset_path = "Asset_Rack.usda"
    stage_asset = Usd.Stage.CreateNew(asset_path)
    UsdGeom.SetStageUpAxis(stage_asset, UsdGeom.Tokens.y)

    # 선반의 최상위 Prim (이것을 Reference로 당겨갈 예정)
    rack_root = UsdGeom.Xform.Define(stage_asset, "/Rack")
    
    # 간단한 시각화를 위해 큐브로 선반 모양 흉내내기
    # (실제로는 모델링 툴에서 만든 정교한 모델을 씁니다)
    shelf = UsdGeom.Cube.Define(stage_asset, "/Rack/Geom")
    shelf.AddScaleOp().Set((0.8, 2.0, 0.5))  # 가로 0.8m, 높이 2m, 깊이 0.5m
    shelf.AddTranslateOp().Set((0, 1.0, 0))  # 바닥 위로 올리기 (Pivot 맞춤)
    
    # 색상 추가 (약간의 파란색)
    shelf.GetDisplayColorAttr().Set([(0.1, 0.5, 0.8)])

    # Default Prim 설정 (Reference 할 때 중요!)
    stage_asset.SetDefaultPrim(rack_root.GetPrim())
    stage_asset.Save()
    print(f"✅ 자산 생성 완료: {asset_path}")


    # ---------------------------------------------------------
    # 2단계: 설비 레이어에 100개 배치하기
    # ---------------------------------------------------------
    # 아까 만든 layer_equipment.usda를 엽니다.
    layer_equip_path = "layer_equipment.usda"
    stage_equip = Usd.Stage.Open(layer_equip_path)
    
    # /World/Equipment 그룹 아래에 배치 시작
    rows = 10
    cols = 10
    spacing = 2.5 # 2.5미터 간격

    print("📦 선반 100개 배치 중...")
    
    for i in range(rows):
        for j in range(cols):
            # 1. 각 선반의 고유 경로 이름 생성 (예: /World/Equipment/Rack_0_0)
            prim_path = f"/World/Equipment/Rack_{i}_{j}"
            
            # 2. Prim 정의 (Xform: 위치 정보를 담을 그릇)
            rack_prim = stage_equip.DefinePrim(prim_path, "Xform")
            
            # 3. [핵심] 원본 파일 Reference 추가
            # addReference(파일경로)
            rack_prim.GetReferences().AddReference(f"./{asset_path}")
            
            # 4. [핵심] 인스턴싱 활성화 (Instanceable = True)
            # 이걸 True로 하면 USD는 내부 내용을 읽지 않고 '포인터'처럼 처리합니다.
            # 수천 개를 띄울 때 성능 차이가 엄청납니다.
            rack_prim.SetInstanceable(True)
            
            # 5. 위치 잡기
            x_pos = (i - rows/2) * spacing
            z_pos = (j - cols/2) * spacing
            UsdGeom.XformCommonAPI(rack_prim).SetTranslate((x_pos, 0, z_pos))

    stage_equip.Save()
    print(f"🎉 배치 완료! {layer_equip_path} 파일이 업데이트되었습니다.")
    print("다시 'usdview main.usda'를 실행해서 확인해보세요.")

if __name__ == "__main__":
    create_mass_production_demo()