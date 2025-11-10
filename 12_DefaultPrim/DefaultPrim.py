from pxr import Usd

# 생성할 USD 파일의 경로를 지정합니다.
file_path = "_assets/default_prim.usda"
# 지정된 경로에 새로운 USD 스테이지(파일)를 생성합니다.
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# '/hello'라는 최상위 Prim을 정의(생성)합니다.
stage.DefinePrim("/hello")
# '/hello' Prim 아래에 'world'라는 자식 Prim을 정의(생성)합니다.
stage.DefinePrim("/hello/world")

# '/hello' 경로에 있는 Prim 객체를 가져옵니다.
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")

# 이 스테이지의 '기본 Prim'을 '/hello' Prim으로 설정합니다.
# (이 파일을 다른 곳에서 참조(Reference)할 때 '/hello'가 기본으로 로드됩니다.)
stage.SetDefaultPrim(hello_prim)

# 스테이지의 변경 사항을 파일로 저장합니다.
stage.Save()