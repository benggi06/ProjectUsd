# USD 핵심 모듈 임포트
from pxr import Usd

# USD 스테이지(Stage)를 열 파일 경로 지정
file_path = "_assets/active-inactive.usda"
# 지정된 파일을 스테이지로 열기
stage = Usd.Stage.Open(file_path)

# 프리미티브(Prim)를 비활성화하기 전 스테이지의 내용을 출력
print("Stage contents BEFORE deactivating:")
# stage.Traverse()를 사용해 스테이지의 모든 프리미티브를 순회
for prim in stage.Traverse():
    # 현재 순회 중인 프리미티브의 경로를 출력
    print(prim.GetPath())

# "/World/Box" 경로에 있는 프리미티브 객체를 가져옴
box = stage.GetPrimAtPath("/World/Box")
# SetActive(False)를 호출하여 해당 프리미티브를 '비활성(Inactive)' 상태로 설정
# (참고: True를 전달하면 '활성(Active)' 상태가 됨)
box.SetActive(False)

# 프리미티브를 비활성화한 후 스테이지의 내용을 다시 출력
print("\n\nStage contents AFTER deactivating:")
# 스테이지를 다시 순회 (이때 'Box' 프림과 그 하위 프림들은 비활성화되어 순회에서 제외됨)
for prim in stage.Traverse():
    # 활성화된 프리미티브의 경로만 출력됨
    print(prim.GetPath())