# pxr 패키지에서 Usd (USD 핵심) 모듈을 임포트합니다.
from pxr import Usd

# 지정된 USD 파일을 스테이지(Stage)로 엽니다.
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# 이 스테이지의 '기본 프리미티브(Default Prim)'를 가져옵니다.
# (파일에 defaultPrim이 "/World"로 설정되어 있다고 가정합니다.)
default_prim: Usd.Prim = stage.GetDefaultPrim()

# 기본 프리미티브의 *모든* 직계 자식(children) 프리미티브를 순회합니다.
# (참고: GetChildren()은 활성/로드된 자식만, GetAllChildren()은 모든 자식을 가져옵니다.)
for child in default_prim.GetAllChildren():
    # 각 자식 프리미티브의 경로(Path)를 출력합니다.
    print(child.GetPath())