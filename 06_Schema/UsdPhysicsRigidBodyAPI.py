from pxr import Usd, UsdGeom, UsdPhysics, Gf

file_path = "_assets/physics_example.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# 1. 씬 구성
world_xform = UsdGeom.Xform.Define(stage, "/World")

# 큐브 (떨어질 물체)
cube = UsdGeom.Cube.Define(stage, "/World/Cube")
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(0, 10, 0))

# 바닥 (고정된 물체) - Plane 대신 크기가 있는 Cube로 바닥을 만듭니다 (시각적으로 더 확실함)
ground = UsdGeom.Cube.Define(stage, "/World/Ground")
UsdGeom.XformCommonAPI(ground).SetScale(Gf.Vec3f(20, 0.1, 20)) # 넓고 얇게
UsdGeom.XformCommonAPI(ground).SetTranslate(Gf.Vec3d(0, -1, 0)) # 약간 아래로

# 2. 물리 적용
# 큐브: 리지드 바디(다이내믹) + 충돌체
UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
UsdPhysics.CollisionAPI.Apply(cube.GetPrim())

# 바닥: 충돌체만 적용 (RigidBodyAPI가 없으면 자동으로 고정된 Static Collider가 됨)
UsdPhysics.CollisionAPI.Apply(ground.GetPrim())

# 3. 속도 설정 (던지기)
cube_rb = UsdPhysics.RigidBodyAPI(cube.GetPrim())
cube_rb.CreateVelocityAttr().Set(Gf.Vec3f(5, 0, 0))
cube_rb.CreateAngularVelocityAttr().Set(Gf.Vec3f(0, 10, 0))

# 4. 씬 물리 설정 (중력)
scene = UsdPhysics.Scene.Define(stage, "/World/PhysicsScene")
scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0, -1, 0))
scene.CreateGravityMagnitudeAttr().Set(980.0) # Omniverse는 보통 cm 단위라 9.8 대신 980이 적절할 수 있음 (일단 기본 9.8로 테스트 후 너무 느리면 수정)
# *수정*: 단위를 맞추기 위해 일단 10 정도로 설정하고 봅니다. USD 기본 단위는 미터(m)입니다.
scene.CreateGravityMagnitudeAttr().Set(9.8)

stage.Save()

print("정상 작동")