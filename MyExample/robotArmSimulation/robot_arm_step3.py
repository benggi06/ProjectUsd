from pxr import Usd, UsdGeom, Sdf # Sdf를 임포트해야 데이터 타입을 지정할 수 있습니다.

# 1. 2단계에서 만든 스테이지 열기
stage = Usd.Stage.Open('robot_arm_step2.usda')
if not stage:
    raise RuntimeError("robot_arm_step2.usda 파일을 찾을 수 없습니다!")

print("2단계 스테이지(애니메이션 포함)를 열었습니다.")

# 2. 로봇 팔 전체의 '상태' 속성 추가
# /World/RobotArm Prim을 가져옵니다.
robot_prim_path = '/World/RobotArm'
robot_prim = stage.GetPrimAtPath(robot_prim_path)

if not robot_prim:
    raise RuntimeError(f"Prim을 찾을 수 없습니다: {robot_prim_path}")

# [Custom Property 핵심 1]
# 'custom:status'라는 이름의 '문자열(String)' 속성을 생성합니다.
# 'custom:' 접두사는 이 속성이 표준 스키마가 아닌 사용자 정의 속성임을 나타냅니다.
status_attr = robot_prim.CreateAttribute(
    'custom:status', 
    Sdf.ValueTypeNames.String
)
# 이 속성에 정적인(static) 값을 설정합니다.
status_attr.Set('Operating') # "작동 중"

print("'/World/RobotArm' Prim에 'custom:status = Operating' 속성을 추가했습니다.")

# 3. 'Gripper'의 '물건 잡기' 상태 속성 추가 (애니메이션)
# Gripper Prim을 가져옵니다. (경로 주의!)
gripper_prim_path = '/World/RobotArm/Base/Arm1/Arm2/Gripper'
gripper_prim = stage.GetPrimAtPath(gripper_prim_path)

if not gripper_prim:
    raise RuntimeError(f"Prim을 찾을 수 없습니다: {gripper_prim_path}")

# [Custom Property 핵심 2]
# 'custom:isGrabbing'이라는 이름의 '불리언(Bool)' 속성을 생성합니다.
grabbing_attr = gripper_prim.CreateAttribute(
    'custom:isGrabbing', 
    Sdf.ValueTypeNames.Bool
)

# 이 속성에 'TimeSamples'를 적용하여 애니메이션을 줍니다.
# (학습자료: 04_TimeCodes 응용)
# 
print("'Gripper' Prim에 'custom:isGrabbing' (Bool) 속성 애니메이션을 추가합니다.")
grabbing_attr.Set(False, time=0)    # 0 프레임: 안 잡음
grabbing_attr.Set(False, time=49)   # 49 프레임: 아직 안 잡음
grabbing_attr.Set(True, time=50)    # 50 프레임: 물건을 잡음! (Arm1이 180도 돈 시점)
grabbing_attr.Set(True, time=99)    # 99 프레임: 계속 잡고 있음
grabbing_attr.Set(False, time=100)  # 100 프레임: 물건을 놓음 (원위치)

# 4. 새 파일로 저장 (Export)
output_path = 'robot_arm_step3.usda'
stage.GetRootLayer().Export(output_path)

print(f"'{output_path}' 파일에 커스텀 속성이 추가되어 저장되었습니다.")