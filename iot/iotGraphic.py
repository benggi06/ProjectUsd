from pxr import Usd, UsdGeom, Gf, UsdShade, Sdf

def apply_texture_material(stage, prim, texture_path):
    """
    특정 Prim에 텍스처를 입히고, UV 좌표를 강제로 1:1 매핑하는 함수
    """
    prim_path = prim.GetPath()
    prim_name = prim_path.name
    
    # Material 생성
    looks_path = "/Jukebox/Looks"
    if not stage.GetPrimAtPath(looks_path):
        UsdGeom.Scope.Define(stage, looks_path)
        
    mat_path = f"{looks_path}/{prim_name}_Mat"
    material = UsdShade.Material.Define(stage, mat_path)

    # Shader 그래프
    st_reader = UsdShade.Shader.Define(stage, f"{mat_path}/stReader")
    st_reader.CreateIdAttr("UsdPrimvarReader_float2")
    st_reader.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("st")
    st_reader.CreateOutput("result", Sdf.ValueTypeNames.Float2)

    tex_shader = UsdShade.Shader.Define(stage, f"{mat_path}/Texture")
    tex_shader.CreateIdAttr("UsdUVTexture")
    tex_shader.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(texture_path)
    tex_shader.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(
        st_reader.ConnectableAPI(), "result"
    )
    tex_shader.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)

    pbr_shader = UsdShade.Shader.Define(stage, f"{mat_path}/PBR")
    pbr_shader.CreateIdAttr("UsdPreviewSurface")
    pbr_shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.8)
    pbr_shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    pbr_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
        tex_shader.ConnectableAPI(), "rgb"
    )

    material.CreateSurfaceOutput().ConnectToSource(
        pbr_shader.ConnectableAPI(), "surface"
    )
    UsdShade.MaterialBindingAPI(prim).Bind(material)

    # UV 강제 할당 (모든 면에 텍스처 꽉 채우기)
    face_uvs = [Gf.Vec2f(0,0), Gf.Vec2f(1,0), Gf.Vec2f(1,1), Gf.Vec2f(0,1)]
    all_uvs = face_uvs * 6 
    primvars_api = UsdGeom.PrimvarsAPI(prim)
    st_primvar = primvars_api.CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying)
    st_primvar.Set(all_uvs)
    indices = [0, 1, 2, 3] * 6
    st_primvar.SetIndices(indices)

def create_jukebox_layered(stage_path="Jukebox_Layered_Final.usda"):
    stage = Usd.Stage.CreateNew(stage_path)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    
    root_path = "/Jukebox"
    UsdGeom.Xform.Define(stage, root_path)
    
    # ==========================================
    # [1] 몸통 (Main Body) - 옆면 텍스처
    # ==========================================
    # Y=0 ~ 10까지 꽉 채우는 몸통
    body_path = f"{root_path}/Body_Main"
    body = UsdGeom.Cube.Define(stage, body_path)
    body.AddScaleOp().Set(Gf.Vec3f(10, 10, 10))
    # 기본 큐브는 중심이 0이므로 Y를 0으로 맞춤
    
    # >> 옆면 이미지 적용
    apply_texture_material(stage, body, "./jukebox_side.png")

    # ==========================================
    # [2] 윗면 판 (Top Plate) - 윗면 텍스처 (사용자 아이디어)
    # ==========================================
    # 아주 얇은(0.05) 판을 몸통 '살짝 위'에 얹습니다.
    # Y 위치: 몸통 꼭대기(10) + 아주 조금 위(0.05) = 10.05 (겹침 방지)
    plate_path = f"{root_path}/Top_Plate"
    plate = UsdGeom.Cube.Define(stage, plate_path)
    # 크기: 가로세로 10 (몸통과 동일), 두께 0.05 (종이장처럼)
    plate.AddScaleOp().Set(Gf.Vec3f(10, 0.05, 10)) 
    plate.AddTranslateOp().Set(Gf.Vec3f(0, 10.05, 0)) 
    
    # >> 윗면 이미지 적용
    apply_texture_material(stage, plate, "./jukebox_top.png")

    # ==========================================
    # [나머지 센서 및 부품]
    # ==========================================

    # 1. 마이크 (가장 윗면) - 판 위에 올라가야 하므로 위치 유지 (Y=11.5)
    mic_path = f"{root_path}/Microphone"
    mic = UsdGeom.Sphere.Define(stage, mic_path)
    mic.GetRadiusAttr().Set(1.5)
    mic.AddTranslateOp().Set(Gf.Vec3f(0, 11.5, 0)) 
    mic.GetDisplayColorAttr().Set([Gf.Vec3f(0.2, 0.2, 0.2)])

    # 2. 상단 카메라 센서
    camera_path = f"{root_path}/Camera_Sensor"
    camera = UsdGeom.Cylinder.Define(stage, camera_path)
    camera.GetAxisAttr().Set("Z")
    camera.GetHeightAttr().Set(0.5)
    camera.GetRadiusAttr().Set(0.6)
    camera.AddTranslateOp().Set(Gf.Vec3f(0, 6.0, 10.0)) 
    camera.GetDisplayColorAttr().Set([Gf.Vec3f(0.05, 0.05, 0.05)]) 

    # 3. LCD 디스플레이
    lcd_group_path = f"{root_path}/LCD_Group"
    lcd_group = UsdGeom.Xform.Define(stage, lcd_group_path)
    lcd_group.AddTranslateOp().Set(Gf.Vec3f(0, 2.0, 10.0)) 

    lcd_frame_path = f"{lcd_group_path}/Frame"
    lcd_frame = UsdGeom.Cube.Define(stage, lcd_frame_path)
    lcd_frame.AddScaleOp().Set(Gf.Vec3f(5.0, 1.5, 0.5)) 
    lcd_frame.AddTranslateOp().Set(Gf.Vec3f(0, 0, 0.5)) 
    lcd_frame.GetDisplayColorAttr().Set([Gf.Vec3f(0.0, 0.8, 0.9)])

    # 4. 초음파 센서
    us_group_path = f"{root_path}/Ultrasonic_Sensor"
    us_group = UsdGeom.Xform.Define(stage, us_group_path)
    us_group.AddTranslateOp().Set(Gf.Vec3f(-5.0, 6.0, 10.0)) 

    us_board = UsdGeom.Cube.Define(stage, f"{us_group_path}/Board")
    us_board.AddScaleOp().Set(Gf.Vec3f(2.0, 0.8, 0.1))
    us_board.GetDisplayColorAttr().Set([Gf.Vec3f(0.1, 0.1, 0.6)]) 

    for side, offset in [("L", -1.0), ("R", 1.0)]:
        eye = UsdGeom.Cylinder.Define(stage, f"{us_group_path}/Eye_{side}")
        eye.GetAxisAttr().Set("Z")
        eye.GetHeightAttr().Set(0.6)
        eye.GetRadiusAttr().Set(0.7)
        eye.AddTranslateOp().Set(Gf.Vec3f(offset, 0, 0))
        eye.GetDisplayColorAttr().Set([Gf.Vec3f(0.8, 0.8, 0.8)]) 

    # 5. 상태 LED
    led_path = f"{root_path}/Status_LED"
    led = UsdGeom.Sphere.Define(stage, led_path)
    led.GetRadiusAttr().Set(0.5)
    led.AddTranslateOp().Set(Gf.Vec3f(-7.5, 6.0, 10.2)) 
    led.GetDisplayColorAttr().Set([Gf.Vec3f(1.0, 0.0, 0.0)])

    # 6. 스피커
    speaker_path = f"{root_path}/Speaker"
    speaker = UsdGeom.Cylinder.Define(stage, speaker_path)
    speaker.GetAxisAttr().Set("Z")
    speaker.GetHeightAttr().Set(0.2) 
    speaker.GetRadiusAttr().Set(2.5) 
    speaker.AddTranslateOp().Set(Gf.Vec3f(0, -4.5, 10.0))
    speaker.GetDisplayColorAttr().Set([Gf.Vec3f(0.2, 0.2, 0.2)]) 

    # 7. 볼륨 노브 & 버튼
    knob_path = f"{root_path}/VolumeKnob"
    knob = UsdGeom.Cylinder.Define(stage, knob_path)
    knob.GetAxisAttr().Set("Z")
    knob.GetHeightAttr().Set(1.5)
    knob.GetRadiusAttr().Set(1.2)
    knob.AddTranslateOp().Set(Gf.Vec3f(6.0, -3.0, 10.0))
    knob.GetDisplayColorAttr().Set([Gf.Vec3f(0.7, 0.5, 0.3)]) 

    button_path = f"{root_path}/Ctrl_Button"
    button = UsdGeom.Cylinder.Define(stage, button_path)
    button.GetAxisAttr().Set("Z")
    button.GetHeightAttr().Set(0.8)
    button.GetRadiusAttr().Set(0.6)
    button.AddTranslateOp().Set(Gf.Vec3f(6.0, -6.0, 10.0))
    button.GetDisplayColorAttr().Set([Gf.Vec3f(0.5, 0.5, 0.5)]) 

    stage.GetRootLayer().Save()
    print(f"Success! USD file saved: {stage_path}")
    print("Make sure to open 'Jukebox_Layered_Final.usda'")

if __name__ == "__main__":
    create_jukebox_layered()