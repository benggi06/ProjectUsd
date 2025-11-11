# pxr 패키지에서 Usd (USD 핵심) 모듈을 임포트합니다.
from pxr import Usd

# 지정된 USD 파일을 스테이지(Stage)로 엽니다.
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# "/World/Box" 경로의 프리미티브(Prim)부터 시작하는 PrimRange(순회 범위)를 생성합니다.
# PrimRange는 기본적으로 지정된 프리미티브와 그 *모든* 자손(descendants)을 포함합니다.
prim_range = Usd.PrimRange(stage.GetPrimAtPath("/World/Box"))

# 생성된 범위(prim_range)를 순회합니다.
for prim in prim_range:
    # 현재 프리미티브의 경로(Path)를 출력합니다.
    # (출력 순서: /World/Box, /World/Box/Lid, /World/Box/Lid/Handle 등)
    print(prim.GetPath())