from pxr import Usd, UsdGeom, Sdf

def create_payload_demo():
    print("🏗️ Payload(지연 로딩) 구조 적용 중...")

    # ---------------------------------------------------------
    # 1. 무거운 내부 부품 데이터 만들기 (Heavy_Parts.usda)
    # ---------------------------------------------------------
    heavy_path = "Heavy_Parts.usda"
    stage_heavy = Usd.Stage.CreateNew(heavy_path)
    UsdGeom.SetStageUpAxis(stage_heavy, UsdGeom.Tokens.y)
    
    root = UsdGeom.Xform.Define(stage_heavy, "/InternalParts")
    
    # 무거움을 시뮬레이션하기 위해 작은 구(Sphere) 100개 생성
    print("   - 정밀 부품(Sphere) 100개 생성 중...")
    for i in range(10):
        for j in range(10):
            sphere = UsdGeom.Sphere.Define(stage_heavy, f"/InternalParts/Bolt_{i}_{j}")
            sphere.AddTranslateOp().Set((i*0.05, 0.5, j*0.05))
            sphere.GetRadiusAttr().Set(0.02)
            
    stage_heavy.SetDefaultPrim(root.GetPrim())
    stage_heavy.Save()


    # ---------------------------------------------------------
    # 2. 로봇 자산(Asset_AGV.usda)에 Payload 연결하기
    # ---------------------------------------------------------
    # 기존에 만든 로봇 파일을 엽니다.
    agv_path = "Asset_AGV.usda"
    stage_agv = Usd.Stage.Open(agv_path)
    agv_prim = stage_agv.GetPrimAtPath("/AGV")
    
    # [핵심] Payload 추가
    # References 대신 Payloads를 사용합니다.
    # 이제 "Heavy_Parts.usda"는 기본적으로 로딩되지 않습니다.
    agv_prim.GetPayloads().AddPayload(f"./{heavy_path}")
    
    stage_agv.Save()
    
    print(f"✅ 적용 완료! {agv_path}에 Payload가 심어졌습니다.")
    print("👉 usdview main.usda를 실행해서 확인해보세요.")

if __name__ == "__main__":
    create_payload_demo()