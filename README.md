# ProjectUsd

NVIDIA OpenUSD 과정을 따라가며 Python(`pxr`)으로 OpenUSD의 핵심 개념을 하나씩 직접 구현한 학습 저장소입니다.
*Hands-on OpenUSD fundamentals in Python, following NVIDIA's OpenUSD course.*

학습 노트: [Notion – OpenUSD](https://www.notion.so/OpenUsd-27b2b2f98829803e9e65fc60b8b8656e)

## 다룬 내용

| 단계 | 주제 |
|---|---|
| 01–03 | Stage 생성, Prim, Attribute |
| 04–05 | TimeCode / TimeSample, Prim·Property 경로 |
| 06–09 | Schema, Scope, Xform, XformCommonAPI |
| 10–12 | Light, Reference, DefaultPrim |
| 13–16 | Value Resolution, Custom Property, Active Prim, Stage 순회(Traversal) |
| `composition_arcs/` | Sublayer, Reference, Payload, Inherit, Specialize, VariantSet |

## 미니 프로젝트

- **`iot/` – Jukebox 에셋:** 초안부터 마이크 추가, 텍스처, 레이어 분리까지 단계별 `.usda` 버전과, 머티리얼·텍스처를 붙이는 스크립트(`iotGraphic.py`)
- **`MyExample/`:** 로봇 팔 시뮬레이션, 스마트 물류센터, 스마트 오피스 장면 구성

## 기술

Python · OpenUSD (`pxr`: Usd, UsdGeom, UsdShade, Sdf, Gf) · NVIDIA Omniverse
