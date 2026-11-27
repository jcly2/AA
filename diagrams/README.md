# 다이어그램 핸드오프: 그리는 규칙과 머메이드 → draw.io 변환

AA 보고서(취약계층 돌봄 시스템)에서 다이어그램 26개를 그리면서 정한 규칙과, 머메이드로 쓴 그림을 편집 가능한 draw.io로 옮긴 방식을 정리했습니다. 이 폴더의 `tools/`는 그 방식을 다른 프로젝트에서도 쓸 수 있게 줄인 **범용 최소판**입니다. 보고서에 쓴 전체 생성기는 저장소의 `tools/`에 있습니다(마지막 절 참고).

## 1. 핵심 아이디어

**원본은 머메이드로 쓰고, 배치는 머메이드에게 맡기고, 결과물은 draw.io로 만든다.**

| 단계 | 하는 일 | 왜 |
| --- | --- | --- |
| ① 머메이드 작성 | 문서(md) 안에 그림을 텍스트로 쓴다 | 문서와 그림이 같이 바뀌고, diff·리뷰가 쉽다 |
| ② 머메이드 렌더(SVG) | `mmdc`로 SVG를 만든다 | 노드 순서·줄·열 배치(dagre)를 직접 계산하지 않고 머메이드 결과를 그대로 쓴다 |
| ③ 좌표 추출 | 브라우저에서 SVG를 열어 노드·subgraph·선의 실제 좌표를 JSON으로 뽑는다 | 머메이드 소스만으로는 위치를 알 수 없다. 렌더된 DOM에서 읽는 것이 가장 정확하다 |
| ④ draw.io 생성 | 좌표를 바탕으로 도형·subgraph·선을 **편집 가능한 셀**로 만든다 | 이미지 붙여 넣기가 아니라 셀이라서, 사람이 draw.io에서 바로 고칠 수 있다 |
| ⑤ 정리 | 크기 통일, 40 격자, 줄·열 맞춤, 직교선 | 머메이드 그대로는 크기가 글자마다 달라 보고서 그림으로 쓰기에 어수선하다 |
| ⑥ 점검·PNG | 격자·겹침 0을 확인하고 draw.io 공식 뷰어로 PNG를 만든다 | 렌더 결과가 draw.io 앱에서 보는 것과 같다 |

원칙: **머메이드가 원본이고 draw.io는 생성물입니다.** 그림을 고칠 때는 머메이드를 고치고 다시 생성합니다. 사람이 draw.io에서 직접 손댄 파일은 생성기로 덮어쓰지 않도록 따로 표시해 둡니다(보고서에서는 Use Case Diagram 하나가 그랬습니다).

## 2. 그리는 규칙

### 2.1 크기와 격자
- 모든 도형의 위치(x, y)와 크기(폭, 높이)는 **40의 배수**입니다.
- 도형 크기는 종류별로 하나로 통일합니다.
  - 사각형·DB(원통): 200×80
  - 원: 160×160 (타원으로 늘리지 않음)
  - 액터: 40×80
  - 큐(Message Queue)만 글자에 맞춥니다.
- 40보다 작은 장식(포트, 인터페이스 공, ● 표식)은 크기 대신 **중심**을 40 격자에 둡니다.
- 머메이드 배치에서 중심이 **60 안쪽**으로 어긋난 도형은 같은 줄·열로 맞춥니다. 원래의 좌우·상하 순서는 지키고, 커진 크기 때문에 겹치면 40 간격을 두고 밉니다. 밀린 도형이 있으면 같은 줄·열 전체를 함께 밉니다.
- subgraph(묶음)는 안쪽부터 내용에 맞추고, 안쪽 여백은 40입니다.

### 2.2 선
- 선은 모두 **draw.io 직교선**(`edgeStyle=orthogonalEdgeStyle`)입니다. draw.io에서 도형을 옮겨도 선이 직각으로 다시 그려집니다.
  - 예외: Use Case Diagram은 UML 관례대로 액터와 UC를 직선으로 잇습니다.
- 선 굵기는 1pt(#333333)로 통일합니다.
- 선끼리 같은 길을 겹쳐 지나지 않게 합니다. 한 줄기로 모으지 않습니다.
  - 예외: UML assembly에서 같은 인터페이스 공으로 모이는 선은 공 바로 앞 80 안에서만 합칩니다.
- 선이 다른 도형을 지나가지 않게 합니다.
- 교차는 **이음 표시**(`jumpStyle=arc`)로 그립니다. 교차가 연결점처럼 보이지 않게 하기 위해서입니다.
- 선 글자는 흰 배경(`labelBackgroundColor=#ffffff`)으로 둡니다.
- 점선은 의미를 하나로 정합니다.
  - 흐름도·배치도: 장애·복구·재구축 때만 쓰는 경로입니다.
  - UML: layer 의존, 시퀀스 반환입니다.
  - 문서 머리에 "점선은 ○○만"이라고 한 문장 적어 둡니다.

### 2.3 색
- 머메이드 기본 테마 색을 그대로 씁니다. 머메이드 미리보기와 draw.io 결과가 같은 그림으로 보이게 하려는 것입니다.
  - 노드: 연보라(#ECECFF, 테두리 #9370DB)
  - subgraph·배치 노드: 연노랑(#ffffde, 테두리 #aaaa33)
  - 시퀀스 노트: 노랑(#fff5ad)
- 강조는 머메이드 `classDef`로만 하고, 생성기는 그 색을 그대로 옮깁니다.
  - 보고서에서는 강조, 병목(채움 #f8cecc, 테두리 #b85450, 굵은 글자), 대기·예비(흐린 색)를 썼습니다.
- 굵은 테두리는 강조한 도형에만 씁니다.

### 2.4 표기(UML)
- **구조도(컴포넌트):** 사각형에 컴포넌트 아이콘과 `«component»` 이름을 둡니다.
  - 포트: 경계의 작은 사각형입니다.
  - 제공 인터페이스: ball(원)로 그립니다.
  - 요구 인터페이스: socket(반원)을 ball에 맞물립니다(assembly).
  - layer: `«layer»` 패키지로 그리고, layer 사이 의존은 점선 화살표입니다.
- **시퀀스:** lifeline, 동기 메시지(실선), 반환(점선), 결합 프래그먼트(alt/opt/loop/par)를 씁니다. 노드 구획은 점선 사각형입니다.
- **배치도:** 노드는 3D 상자(cube)입니다. «executionEnvironment»에는 SW 플랫폼을 적습니다(예: JRE ⇢ Ubuntu).
- 설계 기법이 그림에서 **보이게** 그립니다.
  - 예: Ping/Echo라면 감시하는 쪽(장애감시 → 노드관리GW)의 요구 인터페이스와, 받는 쪽 각 서버의 상태응답 컴포넌트가 모두 구조도에 나와야 합니다.
  - 본문에 적은 기법이 그림에 없다는 지적을 실제로 받았습니다.

### 2.5 배치 습관
- 주 흐름은 한 줄로 세워 이웃끼리 곧게 잇습니다.
- 감시·관리처럼 여러 대상으로 선이 나가는 요소는 대상 줄 아래(또는 위)에 넓게 둡니다. 그러면 선이 대상마다 빗살처럼 곧게 올라갑니다.
- Timer처럼 선이 여러 개 나가는 요소는 바로 아래 상대로 가는 선만 가운데에서 곧게 내립니다. 나머지 선은 상대 쪽 끝에서 냅니다.

## 3. 범용 최소판 사용법

### 3.1 준비
- Node.js 18 이상, Python 3.9 이상
- Playwright(Chromium): 좌표 추출과 PNG 생성에 씁니다.
- mermaid-cli: `npx`가 자동으로 받습니다. 버전은 11.4.2로 고정합니다.
- draw.io 뷰어 스크립트: PNG를 만들 때만 필요합니다. draw.io 공식 저장소 `jgraph/drawio`의 `src/main/webapp/js/viewer-static.min.js`입니다.

```bash
npm i playwright && npx playwright install chromium
```

```bash
git clone --depth 1 https://github.com/jgraph/drawio.git
```

### 3.2 실행
한 번에 변환합니다. 결과는 출력 폴더의 `<이름>.drawio`와 `png/<이름>.png`입니다.

```bash
tools/convert.sh example/sample.mmd example/out drawio/src/main/webapp/js/viewer-static.min.js
```

단계별로 돌릴 때는 아래 순서입니다.

```bash
npx -y @mermaid-js/mermaid-cli@11.4.2 -i example/sample.mmd -o work/sample.svg
```

```bash
node tools/extract_layout.js work
```

```bash
python3 tools/mmd2drawio.py example/sample.mmd work/sample.json example/out/sample.drawio
```

```bash
python3 tools/check_drawio.py example/out
```

```bash
node tools/render_drawio_png.js example/out example/out/png drawio/src/main/webapp/js/viewer-static.min.js
```

- 마지막 명령은 폴더 안 `.drawio`를 모두 렌더합니다.
- 컨테이너처럼 Chromium을 따로 지정해야 하면, puppeteer 설정 JSON(`{"executablePath": "...", "args": ["--no-sandbox"]}`)을 만들어 `PUPPETEER_CFG=<경로>`로 넘깁니다.

### 3.3 파일
| 파일 | 역할 |
| --- | --- |
| `tools/convert.sh` | ①~⑥을 한 번에 실행 |
| `tools/extract_layout.js` | 머메이드 SVG → 좌표 JSON. 노드(`g.node`), subgraph(`g.cluster`), 선(`path.flowchart-link`의 `data-points`, 글자) |
| `tools/mmd2drawio.py` | 좌표 JSON + 머메이드 원본 → draw.io. 크기 통일, 40 격자, 줄·열 맞춤, 순서 유지, subgraph 맞춤, 직교선, 변 위 연결점 분배 |
| `tools/check_drawio.py` | 격자 벗어남·도형 겹침 점검. 0이어야 합니다 |
| `tools/render_drawio_png.js` | draw.io 공식 뷰어로 PNG(2배 해상도) 생성. 서버 없이 페이지에 스크립트를 직접 넣습니다 |
| `example/sample.mmd` | 예제(4.2 CQRS 그림을 줄인 것) |
| `example/out/` | 예제 결과(`sample.drawio`, `png/sample.png`) |

### 3.4 코드에서 볼 곳
- **머메이드 SVG에서 좌표 읽기** (`extract_layout.js`)
  - 렌더된 DOM에서 `getBoundingClientRect()`로 읽어야 subgraph 중첩과 글자 크기가 반영된 실제 위치가 나옵니다.
  - 선 경로는 `data-points` 속성(base64 JSON)에 있습니다.
- **id 연결** (`short_id`, `split_edge`)
  - `mmdc`의 기본 svgId는 `my-svg`입니다. 그래서 노드 id는 `my-svg-flowchart-<노드>-<번호>`, 선 id는 `L_<출발>_<도착>_<번호>`입니다.
  - 노드 이름에 `_`가 있어도 알려진 노드 id로 나눠 출발·도착을 찾습니다.
- **도형 모양** (`parse_source`)
  - SVG만으로는 모양 구분이 애매해서, 머메이드 원본의 괄호로 정합니다.
  - `[(`는 DB, `((`는 원, `([`는 stadium, `[[`는 subroutine, `[`는 사각형입니다.
  - `classDef`와 `class` 줄을 읽어 색을 옮깁니다.
- **배치 정리** (`snap_layout`): 보고서 생성기의 방식을 그대로 옮겼습니다.
  1. 크기를 통일하고 머메이드 중심에 둡니다.
  2. 40 격자로 반올림합니다.
  3. 중심 차이가 60 미만인 도형을 같은 줄·열로 묶습니다.
  4. 원래 앞(왼쪽·위)에 있던 도형과 겹치면 40 간격으로 밉니다. 같은 줄·열은 함께 밀고, 변화가 없을 때까지 반복합니다.
  5. subgraph는 재귀로 안쪽부터 크기를 정합니다.
- **선** (`sides`, 연결점 분배)
  - 두 도형의 상대 위치로 나가는 변·들어가는 변을 정합니다.
  - 곧은 길을 다른 도형이 막으면 아래(세로 관계면 오른쪽)로 돌립니다.
  - 한 변에 선이 여럿 붙으면 상대 위치 순으로 변 위에 같은 간격으로 나눕니다(`exitX/exitY`, `entryX/entryY`). 화살표가 한 점에 겹치지 않습니다.

### 3.5 한계 (최소판)
- 머메이드 **flowchart만** 지원합니다. 시퀀스·UML 컴포넌트 표기는 보고서 전체 생성기에 있습니다(4절).
- 선의 꺾이는 경로는 draw.io 직교선 라우터에 맡깁니다.
  - 같은 두 열 사이를 지나는 선 여러 개가 같은 세로 구간을 나란히 쓸 수 있습니다. 예제 그림의 재구축 점선 두 개가 그렇습니다.
  - 이런 곳은 draw.io에서 꺾임점을 끌어 옮기면 됩니다.
  - 자동으로 없애려면 4절의 `route_drawio.py`처럼 선마다 통로를 따로 배정해야 합니다.
- 글꼴은 `Malgun Gothic`(Windows 기본)으로 지정했습니다. 다른 환경에서는 `FONT` 상수를 바꿉니다.

## 4. 보고서에서 쓴 전체 생성기 (참고)

저장소 루트의 `tools/`에 있습니다. 보고서 그림 번호와 이름이 코드에 박혀 있어 그대로 재사용하기는 어렵지만, 아래 기능이 필요하면 참고하세요. 그림별 배치 규칙은 `diagrams/drawio/README.md`에 모두 적어 두었습니다.

| 파일 | 최소판에 없는 기능 |
| --- | --- |
| `tools/mmd2drawio.py` | UML 컴포넌트 구조도(포트, ball/socket assembly, `«layer»` 패키지, layer 순서), UML 시퀀스(lifeline, 반환 점선, 프래그먼트, 노드 구획), 배치도(cube 노드), 같은 머메이드로 배치만 다른 대안 그림 만들기 |
| `tools/route_drawio.py` | 장애물을 피하는 직각 경로 탐색, 선마다 다른 통로 배정, 글자 자리 선택, 그림별 수동 배치(`deploy_layout`, `fault_top` 등), 교차 최소화, 교차 이음 표시 |
| `tools/straighten_drawio.py` | 직각 구조도를 직선 연결 버전으로 바꾸기(포트 자리를 탐색해 교차·스침 최소화) |
| `tools/annotate_deploy_v2.py` | 배치도 위에 결정 반영 영역(점선 영역 + 설명) 겹쳐 그리기 |
| `tools/find_crossings.py`, `tools/find_overlaps.py`, `tools/check_grid.py` | 교차 수, 선 겹침(0이어야 함), 격자 점검 |
| `tools/feedback_diagrams.py` | 별도 md의 머메이드 블록 목록(SPEC)을 같은 생성기로 변환하는 예(보고서 그림과 번호가 겹치지 않게 `BASE=100`) |

## 5. 해 보면서 배운 것
- **좌표는 SVG 렌더에서 읽습니다.** 머메이드 소스를 직접 배치하려 하면 dagre를 다시 구현하게 됩니다. 렌더 결과를 읽는 쪽이 짧고 정확합니다.
- **줄·열을 전역으로 다시 나누면 그림이 크게 벌어집니다.** 처음에는 모든 중심을 띠로 묶어 줄·열을 새로 매겼는데, 머메이드가 조금씩 다르게 둔 y값이 모두 다른 줄이 되어 그림이 몇 배로 커졌습니다. 머메이드 위치를 기본으로 두고 겹칠 때만 미는 방식이 원래 모양을 지킵니다.
- **폭 200과 160은 중심을 정확히 맞출 수 없습니다.** 반폭이 100과 80이라 40 격자에서 중심이 20 어긋납니다. 격자를 우선하고 20 차이는 감수합니다.
- **draw.io 직교선에 연결점을 지정해야 합니다.** 지정하지 않으면 여러 선이 같은 점으로 들어가고, 도형 뒤로 돌아가는 경로가 생깁니다.
- **PNG는 draw.io 공식 뷰어로 만듭니다.** 다른 렌더러를 쓰면 글자 줄바꿈과 도형 모양이 draw.io 앱과 달라집니다.
- **생성 후 점검을 숫자로 확인합니다.** 격자 벗어남 0, 겹침 0, 선 겹침 0을 매번 돌립니다. 눈으로만 보면 놓칩니다.
- **사람이 손댄 파일은 보호합니다.** 생성기가 덮어쓰지 않도록 목록에서 빼고 README에 적어 둡니다.
