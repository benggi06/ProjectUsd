from pxr import Usd, UsdGeom, Gf

def force_fix_animation():
    print("🔧 [긴급 수정] 박스 낙하 애니메이션 복구 시작...")

    # -------------------------------------------------------
    # 1. main.usda (최상위 파일) 타임라인 강제 고정
    # -------------------------------------------------------
    stage_main = Usd.Stage.Open("main.usda")
    stage_main.SetStartTimeCode(0)
    stage_main.SetEndTimeCode(60)
    stage_main.SetFramesPerSecond(24)
    stage_main.GetRootLayer().Save()
    print("✅ main.usda 타임라인 설정 완료 (0 ~ 60 프레임)")

    # -------------------------------------------------------
    # 2. layer_equipment.usda (설비 파일) 박스 애니메이션 재작성
    # -------------------------------------------------------
    layer_equip_path = "layer_equipment.usda"
    stage_equip = Usd.Stage.Open(layer_equip_path)
    
    # 박스 찾기
    box_path = "/World/Equipment/DropBox"
    box_prim = stage_equip.GetPrimAtPath(box_path)
    
    if not box_prim.IsValid():
        print(f"❌ 오류: {box_path}를 찾을 수 없습니다. 이전 코드를 먼저 실행해 박스를 만들어주세요.")
        return

    # 기존 애니메이션(Transform) 초기화 (충돌 방지)
    xform_api = UsdGeom.XformCommonAPI(box_prim)
    
    # 기존의 위치 조작(Ops)을 모두 지우고 새로 시작하려는 시도
    # (복잡성을 피하기 위해 위치값을 덮어쓰는 방식을 사용합니다)

    # 박스 위치 재설정 (선반 사이 통로: X=1.25)
    start_pos = (1.25, 5.0, 0.0)
    
    print(f"📦 박스({box_path}) 위치를 {start_pos}로 초기화하고 다시 떨어뜨립니다.")

    # 물리 시뮬레이션 변수
    height = start_pos[1]
    velocity = 0.0
    gravity = -9.81
    dt = 1.0 / 24.0

    # 키프레임 굽기 (Baking)
    for frame in range(61):
        # 위치 설정
        xform_api.SetTranslate((start_pos[0], height, start_pos[2]), time=frame)
        
        # 물리 계산
        velocity += gravity * dt
        height += velocity * dt
        
        # 바닥 충돌 (Bounce)
        if height <= 0.25:
            height = 0.25
            velocity = -velocity * 0.5 # 튕김 계수
            if abs(velocity) < 0.5: velocity = 0; height = 0.25

    stage_equip.Save()
    print(f"✅ {layer_equip_path} 애니메이션 저장 완료.")
    print("\n🚨 [중요] usdview를 반드시 '껐다가 다시 켜주세요' (Reload로는 부족할 수 있습니다).")

if __name__ == "__main__":
    force_fix_animation()