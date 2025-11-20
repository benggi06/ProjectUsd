from pxr import Usd

def fix_timeline():
    # 최상위 파일 열기
    stage = Usd.Stage.Open("main.usda")
    
    # 타임라인 정보를 메인 파일에 강제로 설정
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(100)
    stage.SetFramesPerSecond(24)
    
    stage.GetRootLayer().Save()
    print("✅ main.usda 타임라인 업데이트 완료!")
    print("이제 usdview main.usda를 실행하면 타임라인이 0~100으로 잡힐 것입니다.")

if __name__ == "__main__":
    fix_timeline()