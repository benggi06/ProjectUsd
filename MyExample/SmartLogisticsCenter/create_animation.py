from pxr import Usd, UsdGeom, Sdf

def create_animation_demo():
    # 1. 설비 레이어 열기
    layer_equip_path = "layer_equipment.usda"
    stage_equip = Usd.Stage.Open(layer_equip_path)

    # 2. 애니메이션 구간 설정
    stage_equip.SetStartTimeCode(0)
    stage_equip.SetEndTimeCode(100)
    stage_equip.SetFramesPerSecond(24)

    # 3. 움직일 로봇 찾기 (AGV_1)
    prim_path = "/World/Equipment/AGV_1"
    agv_prim = stage_equip.GetPrimAtPath(prim_path)
    
    if not agv_prim.IsValid():
        print("❌ 오류: AGV_1을 찾을 수 없습니다. 이전 단계를 먼저 실행해주세요.")
        return

    # 4. API 객체 생성
    xform_api = UsdGeom.XformCommonAPI(agv_prim)

    # 5. [수정됨] TimeSamples로 키프레임 찍기
    # 복잡하게 Op를 찾지 않고, SetTranslate에 'time' 파라미터를 직접 넣습니다.
    
    print("🎬 애니메이션 키프레임 생성 중...")
    
    # 0 프레임: 원점 (0, 0, 5)
    xform_api.SetTranslate((0, 0, 5), time=0)
    
    # 50 프레임: 앞으로 전진 (0, 0, 15)
    xform_api.SetTranslate((0, 0, 15), time=50)
    
    # 100 프레임: 다시 원점 복귀 (0, 0, 5)
    xform_api.SetTranslate((0, 0, 5), time=100)

    stage_equip.Save()
    print(f"🎉 애니메이션 적용 완료! {layer_equip_path} 저장됨.")
    print("이제 'usdview main.usda'를 실행하고 재생(Play, 단축키 Space) 버튼을 눌러보세요!")

if __name__ == "__main__":
    create_animation_demo()