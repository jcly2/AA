#!/usr/bin/env bash
# 머메이드(.mmd) → draw.io(.drawio) → PNG 한 번에.
# 사용: tools/convert.sh <입력.mmd> <출력 폴더> [viewer-static.min.js 경로]
#   필요: Node.js, Python 3, Playwright(chromium), mermaid-cli(npx로 자동 설치)
#   viewer-static.min.js: draw.io 공식 저장소 jgraph/drawio의 src/main/webapp/js/viewer-static.min.js
#   (경로를 주지 않으면 PNG는 건너뛴다)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
in="$1"; out="$2"; viewer="${3:-}"
name="$(basename "${in%.mmd}")"
work="$(mktemp -d)"
mkdir -p "$out"
# 1) 머메이드로 SVG 렌더(배치 계산은 머메이드에 맡긴다). svgId는 기본값 my-svg를 쓴다
npx -y @mermaid-js/mermaid-cli@11.4.2 -i "$in" -o "$work/$name.svg" -q ${PUPPETEER_CFG:+-p "$PUPPETEER_CFG"}
# 2) SVG에서 노드·subgraph·선 좌표를 JSON으로 뽑는다
node "$here/extract_layout.js" "$work"
# 3) draw.io로 변환(크기 통일, 40 격자, 직교선)
python3 "$here/mmd2drawio.py" "$in" "$work/$name.json" "$out/$name.drawio"
# 4) 점검(격자·겹침 0)
python3 "$here/check_drawio.py" "$out/$name.drawio" || echo "점검 항목이 남았습니다. draw.io에서 확인하세요."
# 5) PNG(2배 해상도)
if [ -n "$viewer" ]; then
  cp "$out/$name.drawio" "$work/"; mkdir -p "$out/png"
  node "$here/render_drawio_png.js" "$work" "$out/png" "$viewer" >/dev/null
  echo "png: $out/png/$name.png"
fi
