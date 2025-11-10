# Usd 모듈을 불러온다
from pxr import Usd

# "_assets/paths.usda" 이름으로 새 스테이지(작업 공간)를 만든다
stage: Usd.Stage = Usd.Stage.CreateNew("_assets/paths.usda")

# 스테이지 최상위에 "/hello" 프림을 정의한다
stage.DefinePrim("/hello")

# "/hello" 프림의 자식으로 "/hello/world" 프림을 정의한다
stage.DefinePrim("/hello/world")

# 스테이지에서 "/hello" 경로의 프림을 가져온다
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")

# 스테이지에서 "/hello/world" 경로의 프림을 가져온다
hello_world_prim: Usd.Prim = stage.GetPrimAtPath("/hello/world")

# 스테이지에서 "/world" 경로의 프림을 가져온다
# (참고: "/world"는 존재하지 않으므로, '유효하지 않은(invalid)' 프림이 반환된다)
world_prim: Usd.Prim = stage.GetPrimAtPath("/world")

# 각 프림 객체가 '유효한(Valid)' 프림인지 확인하여 출력한다
print("Is /hello a valid prim? ", hello_prim.IsValid())
print("Is /hello/world a valid prim? ", hello_world_prim.IsValid())
print("Is /world a valid prim? ", world_prim.IsValid())

# 변경 사항을 파일에 저장한다
stage.Save()