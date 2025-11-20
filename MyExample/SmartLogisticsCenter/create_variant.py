from pxr import Usd, UsdGeom, Sdf, Gf

def create_variant_demo():
    # ---------------------------------------------------------
    # 1단계: 상태가 변하는 AGV 자산(Asset) 만들기
    # ---------------------------------------------------------
    agv_path = "Asset_AGV.usda"
    stage_agv = Usd.Stage.CreateNew(agv_path)
    UsdGeom.SetStageUpAxis(stage_agv, UsdGeom.Tokens.y)
    
    # 1. 로봇의 본체 정의
    agv_prim = UsdGeom.Xform.Define(stage_agv, "/AGV")
    
    # 시각화를 위해 작은 박스로 표현
    body = UsdGeom.Cube.Define(stage_agv, "/AGV/Body")
    body.AddScaleOp().Set((0.5, 0.3, 0.8)) # 납작한 로봇 형태
    
    # 2. [핵심] VariantSet 생성 ("State"라는 이름의 스위치 생성)
    # 전역(Global) VariantSet을 만듭니다.
    vset = agv_prim.GetPrim().GetVariantSets().AddVariantSet("State")
    
    # 3. 각 옵션(Variant)별 내용 정의
    
    # --- 옵션 A: Idle (대기 중 - 파란색) ---
    vset.AddVariant("Idle")          # 옵션 이름 등록
    vset.SetVariantSelection("Idle") # 지금부터 작성할 내용은 'Idle' 안에 들어감
    with vset.GetVariantEditContext():
        # 이 블록 안에서 하는 설정은 'Idle'일 때만 적용됨
        body.GetDisplayColorAttr().Set([(0.2, 0.2, 0.8)]) # Blue
        
    # --- 옵션 B: Working (작업 중 - 초록색) ---
    vset.AddVariant("Working")
    vset.SetVariantSelection("Working")
    with vset.GetVariantEditContext():
        body.GetDisplayColorAttr().Set([(0.2, 0.8, 0.2)]) # Green
        # 작업 중일 때는 크기를 약간 키워본다던지 하는 지오메트리 변경도 가능
        
    # --- 옵션 C: Error (고장 - 빨간색) ---
    vset.AddVariant("Error")
    vset.SetVariantSelection("Error")
    with vset.GetVariantEditContext():
        body.GetDisplayColorAttr().Set([(0.9, 0.1, 0.1)]) # Red

    # 기본 선택값 설정 (파일을 처음 열었을 때 보일 상태)
    vset.SetVariantSelection("Idle")
    
    stage_agv.SetDefaultPrim(agv_prim.GetPrim())
    stage_agv.Save()
    print(f"✅ 가변형 자산 생성 완료: {agv_path}")


    # ---------------------------------------------------------
    # 2단계: 설비 레이어에 로봇 배치하고 상태 바꾸기
    # ---------------------------------------------------------
    layer_equip_path = "layer_equipment.usda"
    stage_equip = Usd.Stage.Open(layer_equip_path)
    
    # 로봇 3대 배치
    states = ["Idle", "Working", "Error"]
    positions = [(-2, 0), (0, 0), (2, 0)] # x, z 좌표
    
    print("🤖 로봇 배치 및 상태 설정 중...")
    
    for i in range(3):
        prim_path = f"/World/Equipment/AGV_{i}"
        agv_inst = stage_equip.DefinePrim(prim_path, "Xform")
        
        # Reference 추가
        agv_inst.GetReferences().AddReference(f"./{agv_path}")
        
        # 위치 설정 (선반들 사이 통로에 배치)
        # Z축을 5미터 앞으로 당겨서 선반과 겹치지 않게 함
        UsdGeom.XformCommonAPI(agv_inst).SetTranslate((positions[i][0], 0, 5))
        
        # [핵심] 이 인스턴스만의 Variant 선택!
        # "State" 스위치를 찾아서 원하는 상태로 딸깍 변경
        vset_inst = agv_inst.GetVariantSet("State")
        vset_inst.SetVariantSelection(states[i])

    stage_equip.Save()
    print(f"🎉 로봇 배치 완료! {layer_equip_path} 업데이트 됨.")
    print("다시 'usdview main.usda'를 실행해 3가지 색상의 로봇을 확인하세요.")

if __name__ == "__main__":
    create_variant_demo()