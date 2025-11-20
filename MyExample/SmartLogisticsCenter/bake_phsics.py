from pxr import Usd, UsdGeom

def bake_physics_simulation():
    # 1. 설비 레이어 열기
    layer_equip_path = "layer_equipment.usda"
    stage = Usd.Stage.Open(layer_equip_path)
    
    # 2. 타임라인 설정
    fps = 24.0
    stage.SetFramesPerSecond(fps)
    stage.SetStartTimeCode(0)
    total_frames = 60
    stage.SetEndTimeCode(total_frames)

    # 3. 대상: 아까 만든 DropBox
    box_prim = stage.GetPrimAtPath("/World/Equipment/DropBox")
    if not box_prim.IsValid():
        print("❌ 박스를 찾을 수 없습니다. 실습 1을 먼저 실행하세요.")
        return

    # 위치 제어를 위한 API
    xform_api = UsdGeom.XformCommonAPI(box_prim)
    
    # --- 간이 물리 계산 시작 ---
    # 초기 조건
    height = 5.0  # 초기 높이 (m)
    velocity = 0.0 # 초기 속도 (m/s)
    gravity = -9.81 # 중력 가속도 (m/s^2)
    dt = 1.0 / fps # 한 프레임당 시간 (초)
    
    print("🍎 중력 시뮬레이션 계산 및 베이킹 중...")

    for frame in range(total_frames + 1):
        # 1. 위치 기록 (키프레임 생성)
        # 현재 높이를 해당 프레임(time=frame)에 저장
        xform_api.SetTranslate((0, height, 0), time=frame)
        
        # 2. 물리 계산 (오일러 적분법)
        # 속도 = 속도 + 가속도 * 시간
        velocity += gravity * dt
        
        # 위치 = 위치 + 속도 * 시간
        height += velocity * dt
        
        # 3. 바닥 충돌 처리 (Bounce)
        # 바닥(y=0)보다 내려가면 튕기게 만듦
        if height <= 0.25: # 박스 절반 크기(0.25) 고려
            height = 0.25
            velocity = -velocity * 0.5 # 탄성 계수 0.5 (절반의 힘으로 튀어오름)
            
            # 속도가 너무 줄어들면 멈춤
            if abs(velocity) < 0.5:
                velocity = 0
                height = 0.25

    stage.Save()
    print(f"🎉 물리 베이킹 완료! {layer_equip_path}")
    print("usdview main.usda를 실행하고 스페이스바를 눌러 박스가 떨어지는 것을 확인하세요!")

if __name__ == "__main__":
    bake_physics_simulation()