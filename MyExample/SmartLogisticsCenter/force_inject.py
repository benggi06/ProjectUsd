from pxr import Usd, UsdGeom, Sdf

def force_inject_animation():
    print("💉 [강제 주입] 애니메이션 데이터 직접 쓰기 모드 진입...")

    # 1. 설비 레이어 열기
    layer_equip_path = "layer_equipment.usda"
    stage = Usd.Stage.Open(layer_equip_path)
    
    # 2. 박스 Prim 찾기
    box_path = "/World/Equipment/DropBox"
    box_prim = stage.GetPrimAtPath(box_path)
    
    if not box_prim.IsValid():
        print("❌ 박스 Prim을 찾을 수 없습니다.")
        return

    # 3. [핵심] 속성(Attribute) 직접 가져오기
    # API를 거치지 않고 USD 데이터 구조에 바로 접근합니다.
    translate_attr = box_prim.GetAttribute("xformOp:translate")
    
    if not translate_attr.IsValid():
        # 혹시 속성이 없다면 만듭니다.
        xform_api = UsdGeom.Xformable(box_prim)
        translate_attr = xform_api.AddTranslateOp()

    # 4. [중요] 기존의 찌꺼기 데이터(고정값) 삭제
    # 이 부분이 없어서 아까 (0, 5, 0)에서 멈춰있던 것입니다.
    print("🧹 기존 고정값(Static Value) 삭제 중...")
    translate_attr.Clear() 

    # 5. 애니메이션 데이터 굽기
    print("🔥 애니메이션 키프레임 굽기 시작 (Frame 0~60)...")
    
    start_pos = (1.25, 5.0, 0.0) # 통로 위치 (X=1.25)
    height = start_pos[1]
    velocity = 0.0
    gravity = -9.81
    dt = 1.0 / 24.0

    for frame in range(61):
        # 직접 Attribute에 Set합니다.
        translate_attr.Set((start_pos[0], height, start_pos[2]), time=frame)
        
        # 물리 계산
        velocity += gravity * dt
        height += velocity * dt
        
        # 바닥 충돌
        if height <= 0.25:
            height = 0.25
            velocity = -velocity * 0.5
            if abs(velocity) < 0.5: velocity = 0; height = 0.25

    stage.Save()
    print(f"✅ {layer_equip_path} 저장 완료!")
    print("👉 이제 usdview를 껐다가 다시 켜서 확인해주세요.")
    print("👉 52프레임 쯤에서 Y값이 5가 아니라 바닥에 붙어 있어야 성공입니다.")

if __name__ == "__main__":
    force_inject_animation()