from pxr import Usd, Sdf, UsdGeom

def create_logistics_scene():
    # 1. 스테이지 생성
    stage = Usd.Stage.CreateNew("LogisticsCenter.usda")
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    
    # 2. 로봇 원본 파일(가정)을 레퍼런스로 가져오기 위한 준비
    # 실제로는 "AGV_Asset.usda" 파일이 존재해야 합니다.
    agv_asset_path = "./assets/AGV_Asset.usda"
    
    # 3. 로봇 3대 배치 (References)
    for i in range(3):
        agv_prim_path = f"/World/AGV_{i}"
        agv_prim = stage.DefinePrim(agv_prim_path, "Xform")
        
        # Reference 추가
        agv_prim.GetReferences().AddReference(agv_asset_path)
        
        # 위치 설정 (X축으로 2미터씩 띄우기)
        UsdGeom.XformCommonAPI(agv_prim).SetTranslate((i * 2.0, 0, 0))
        
        # 4. 각 로봇의 상태 다르게 설정 (Variants)
        # AGV_Asset.usda 안에 "State"라는 VariantSet이 있다고 가정
        vset = agv_prim.GetVariantSet("State")
        
        if i == 0:
            vset.SetVariantSelection("Idle")    # 대기
        elif i == 1:
            vset.SetVariantSelection("Moving")  # 이동 중
        else:
            vset.SetVariantSelection("Error")   # 고장
            
    stage.GetRootLayer().Save()
    print("LogisticsCenter.usda 생성 완료!")

if __name__ == "__main__":
    create_logistics_scene()