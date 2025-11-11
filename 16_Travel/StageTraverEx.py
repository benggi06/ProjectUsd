# pxr 패키지에서 Usd (USD 핵심) 모듈을 임포트합니다.
from pxr import Usd

# 지정된 파일("_assets/stage_traversal.usda")을 Usd.Stage (스테이지)로 엽니다.
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# stage.Traverse()를 사용하여 스테이지의 모든 (활성화된) 프리미티브를 순회합니다.
# (Traverse는 기본적으로 활성, 로드, 정의된 프리미티브만 깊이 우선 방식으로 방문합니다)
for prim in stage.Traverse():
    # 순회 중인 각 프리미티브(prim)의 경로(Path)를 출력합니다.
    print(prim.GetPath())