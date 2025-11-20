from pxr import Usd, UsdGeom, UsdPhysics, Sdf, Gf

def setup_physics_schema():
    # 1. 메인 파일 열기 (또는 설비 레이어)
    # 여기서는 편의상 설비 레이어에 박스를 추가하겠습니다.
    layer_equip_path = "layer_equipment.usda"
    stage = Usd.Stage.Open(layer_equip_path)

    # ----------------------------------------------------
    # A. 물리 씬(Physics Scene) 정의
    # "이 월드에는 중력이 작용한다"
    # ----------------------------------------------------
    scene_path = "/World/PhysicsScene"
    physics_scene = UsdPhysics.Scene.Define(stage, scene_path)
    
    # 중력 설정 (Y축이 위쪽이므로, -Y 방향으로 9.8m/s^2)
    # magnitude(크기)와 direction(방향)을 설정할 수도 있고, vector로 한번에 할 수도 있습니다.
    physics_scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0, -1, 0))
    physics_scene.CreateGravityMagnitudeAttr().Set(9.81)


    # ----------------------------------------------------
    # B. 바닥(Floor)에 충돌 속성 추가 (부딪혀야 하니까)
    # ----------------------------------------------------
    # 주의: 바닥은 layer_layout.usda에 있지만, Override를 통해 여기서 속성을 덧붙일 수 있습니다.
    # 실습 편의를 위해 임시 바닥 충돌체를 여기에 하나 더 만들겠습니다.
    floor_collider = UsdGeom.Cube.Define(stage, "/World/Equipment/Floor_Collider")
    floor_collider.AddScaleOp().Set((20, 0.1, 20))
    floor_collider.AddTranslateOp().Set((0, -0.1, 0)) # 눈에 보이는 바닥 바로 아래
    
    # [핵심] 충돌체(Collision) API 적용 -> "이건 뚫고 지나갈 수 없다"
    UsdPhysics.CollisionAPI.Apply(floor_collider.GetPrim())
    
    # 시각적으로는 안 보여도 되므로 투명하게 하거나 invisible 처리 (선택)
    # floor_collider.MakeInvisible()


    # ----------------------------------------------------
    # C. 떨어질 박스(Crate) 만들기
    # ----------------------------------------------------
    box_path = "/World/Equipment/DropBox"
    box = UsdGeom.Cube.Define(stage, box_path)
    
    # 크기와 위치 (공중에 띄움)
    box.AddScaleOp().Set((0.5, 0.5, 0.5))
    box.AddTranslateOp().Set((0, 5.0, 0)) # 높이 5미터
    box.GetDisplayColorAttr().Set([(1, 0.5, 0)]) # 주황색

    # [핵심 1] RigidBody API 적용 -> "이건 움직이는 고체다"
    UsdPhysics.RigidBodyAPI.Apply(box.GetPrim())

    # [핵심 2] Collision API 적용 -> "이건 부딪힌다"
    UsdPhysics.CollisionAPI.Apply(box.GetPrim())

    # [핵심 3] 질량(Mass) 설정 (선택 사항)
    mass_api = UsdPhysics.MassAPI.Apply(box.GetPrim())
    mass_api.CreateMassAttr().Set(10.0) # 10kg

    stage.Save()
    print(f"✅ 물리 속성 설정 완료! {layer_equip_path}")
    print("이제 데이터에는 질량과 충돌 정보가 들어있습니다.")

if __name__ == "__main__":
    setup_physics_schema()