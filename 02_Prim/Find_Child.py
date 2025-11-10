from pxr import Usd

file_path = "_assets/prim_hierarchy.usda"
# 이전에 저장한 usda파일을 스테이지로 연다.
stage: Usd.Stage = Usd.Stage.Open(file_path)

# 스테이지의 /Geometry 경로의 프림을 가져옴
prim: Usd.Prim = stage.GetPrimAtPath("/Geometry")

# 찾은 자식 프림을 담기 위한 변수 선언
child_prim: Usd.Prim

# '직계 자식' 중 Box가 있는지 확인
if child_prim := prim.GetChild("Box"):
    print("Child prim exists")
else:
    print("Child prim DOES NOT exist")