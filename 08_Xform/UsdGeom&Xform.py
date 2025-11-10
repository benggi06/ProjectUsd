# pxr 패키지에서 필요한 모듈을 가져옵니다.
from pxr import Usd, UsdGeom

# 루트 레이어 이름이 "xform_prim.usda"인 새로운 USD 스테이지를 생성합니다.
file_path = "_assets/xform_prim.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# 현재 스테이지의 "/World" 경로에 새로운 Xform(변환) 프림을 정의합니다.
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# 현재 스테이지의 변경 사항을 루트 레이어 파일에 저장합니다.
stage.Save()

# 저장된 내용을 문자열로 출력하여 확인합니다 (소스 파일 주석 제외).
print(stage.ExportToString(addSourceFileComment=False))