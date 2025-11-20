from pxr import Usd, UsdGeom, UsdPhysics, Sdf, Gf

def fix_physics_position():
    # 1. 설비 레이어 열기
    layer_equip_path = "layer_equipment.usda"
    stage = Usd.Stage.Open(layer_equip_path)
    
    # 타임라인 설정 확인
    stage.SetFramesPerSecond(24)
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(60)

    # ----------------------------------------------------
    # A. 물리 씬 & 바닥 설정 (혹시 없으면 생성)
    # ----------------------------------------------------
    scene_path = "/World/PhysicsScene"
    if not stage.GetPrimAtPath(scene_path):
        physics_scene = UsdPhysics.Scene.Define(stage, scene_path)
        physics_scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0, -1, 0))
        physics_scene.CreateGravityMagnitudeAttr().Set(9.81)

    # 바닥 충돌체 확인
    floor_path = "/World/Equipment/Floor_Collider"
    if not stage.GetPrimAtPath(floor_path):
        floor_collider = UsdGeom.Cube.Define(stage, floor_path)
        floor_collider.AddScaleOp().Set((20, 0.1, 20))
        floor_collider.AddTranslateOp().Set((0, -0.1, 0))
        UsdPhysics.CollisionAPI.Apply(floor_collider.GetPrim())

    # ----------------------------------------------------
    # B. 박스 위치 수정 (선반 사이 통로로 이동)
    # ----------------------------------------------------
    box_path = "/World/Equipment/DropBox"
    box = UsdGeom.Cube.Define(stage, box_path)
    
    # 필수 API 적용 (RigidBody, Collision)
    UsdPhysics.RigidBodyAPI.Apply(box.GetPrim())
    UsdPhysics.CollisionAPI.Apply(box.GetPrim())
    
    # 위치 제어 API
    xform_api = UsdGeom.XformCommonAPI(box)

    # [수정 포인트] X=1.25 위치는 선반(0.0)과 선반(2.5)의 딱 중간입니다.
    start_pos = (1.25, 5.0, 0.0) 
    
    # ----------------------------------------------------
    # C. 물리 시뮬레이션 다시 굽기 (Re-Baking)
    # ----------------------------------------------------
    print(f"📦 박스 위치를 {start_pos} (통로)로 옮기고 시뮬레이션을 다시 계산합니다...")

    height = start_pos[1] # 5.0
    velocity = 0.0
    gravity = -9.81
    dt = 1.0 / 24.0 # FPS

    for frame in range(61):
        # 1. 현재 위치 기록 (X=1.25, Z=0 고정)
        xform_api.SetTranslate((start_pos[0], height, start_pos[2]), time=frame)
        
        # 2. 물리 계산
        velocity += gravity * dt
        height += velocity * dt
        
        # 3. 바닥 충돌 처리
        if height <= 0.25:
            height = 0.25
            velocity = -velocity * 0.6 # 탄성 계수 (좀 더 잘 튀게 0.6으로 상향)
            
            if abs(velocity) < 0.5:
                velocity = 0
                height = 0.25

    stage.Save()
    print(f"🎉 수정 완료! {layer_equip_path} 저장됨.")
    print("이제 usdview main.usda를 실행해 보세요. 박스가 통로 사이로 떨어질 겁니다!")

if __name__ == "__main__":
    fix_physics_position()