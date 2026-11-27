"""머메이드 흐름도(flowchart)를 편집 가능한 draw.io 파일로 바꾼다 (범용 최소판).

사용:
  python3 mmd2drawio.py <원본.mmd> <배치.json> <출력.drawio> [제목]
  - 배치.json: extract_layout.js가 머메이드 SVG에서 뽑은 좌표
  - 머메이드가 계산한 배치(줄·열 순서)를 그대로 가져오고, 다음 규칙으로 정리한다.
    1) 도형 크기 통일: 사각형·DB 200x80, 원 160x160, 액터 40x80
    2) 40 격자: 위치·크기는 40의 배수. 중심이 60 안쪽으로 어긋난 도형은 같은 줄·열로 맞춘다
    3) 순서 유지: 원래의 좌우·상하 순서를 지키고, 커진 크기로 겹치면 40 간격을 두고 민다
    4) subgraph는 안쪽부터 내용에 맞추고 안쪽 여백 40
    5) 선은 draw.io 직교선(orthogonalEdgeStyle) + 교차 이음 표시(jumpStyle=arc).
       상대 위치로 나가는 변·들어가는 변을 정해 선이 도형 뒤로 돌아가지 않게 한다
    6) 색은 머메이드 기본 테마, classDef 색은 그대로
"""
import html
import json
import re
import sys

G = 40          # 격자
ALIGN_TOL = 60  # 이 안쪽으로 어긋난 중심은 같은 줄·열로 맞춘다
GAP = 40        # 밀어낼 때 도형 사이 최소 간격
PAD = 40        # subgraph 안쪽 여백(제목도 이 안에 들어간다)

SIZE = {'rect': (200, 80), 'round': (200, 80), 'stadium': (200, 80), 'subroutine': (200, 80),
        'cylinder': (200, 80), 'circle': (160, 160), 'actor': (40, 80)}

FONT = 'fontFamily=Malgun Gothic;fontSize=11;'
NODE_C = 'fillColor=#ECECFF;strokeColor=#9370DB;'   # 머메이드 기본: 노드 연보라
GROUP_C = 'fillColor=#ffffde;strokeColor=#aaaa33;'  # 머메이드 기본: subgraph 연노랑
EDGE_C = 'strokeColor=#333333;strokeWidth=1;'       # 선은 모두 1pt

STYLE = {
    'rect': 'rounded=0;whiteSpace=wrap;html=1;',
    'round': 'rounded=1;whiteSpace=wrap;html=1;',
    'stadium': 'rounded=1;arcSize=50;whiteSpace=wrap;html=1;',
    'subroutine': 'shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.06;',
    'cylinder': 'shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=8;',
    'circle': 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;',
    'actor': 'shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;',
}


def r40(v):
    return int(round(v / G)) * G


def up40(v):
    return int(-(-v // G)) * G


def esc(s):
    return html.escape(s, quote=True)


# ---------- 머메이드 원본 해석: 도형 모양, classDef ----------

SHAPE_RE = re.compile(r'(?<![\w-])([A-Za-z_]\w*)\s*(\[\(|\(\(|\(\[|\[\[|\[|\()')
BRACKET = {'[(': 'cylinder', '((': 'circle', '([': 'stadium', '[[': 'subroutine', '[': 'rect', '(': 'round'}


def parse_source(src):
    shapes, defs, assign = {}, {}, {}
    for line in src.split('\n'):
        s = line.strip()
        m = re.match(r'classDef (\w+) (.+)', s)
        if m:
            defs[m.group(1)] = dict(kv.split(':', 1) for kv in m.group(2).split(',') if ':' in kv)
            continue
        m = re.match(r'class ([\w,]+) (\w+)', s)
        if m:
            for nid in m.group(1).split(','):
                assign[nid] = m.group(2)
            continue
        if s.startswith(('subgraph', 'linkStyle', '%%', 'flowchart', 'graph', 'direction', 'end')):
            continue
        for m in SHAPE_RE.finditer(s):
            shapes.setdefault(m.group(1), BRACKET[m.group(2)])
    styles = {}
    for nid, c in assign.items():
        st = {k.strip(): v.strip() for k, v in defs.get(c, {}).items()}
        out = ''
        if 'fill' in st:
            out += f'fillColor={st["fill"]};'
        if 'stroke' in st:
            out += f'strokeColor={st["stroke"]};'
        if 'stroke-width' in st:
            out += f'strokeWidth={st["stroke-width"].replace("px", "")};'
        if 'color' in st:
            out += f'fontColor={st["color"]};'
        if st.get('font-weight') == 'bold':
            out += 'fontStyle=1;'
        styles[nid] = out
    return shapes, styles


# ---------- 머메이드 SVG 좌표(extract_layout.js 결과) 해석 ----------

def short_id(svgid):
    # mmdc 기본 svgId(my-svg) 기준: "my-svg-flowchart-NODE-3" → "NODE"
    p = 'my-svg-flowchart-'
    return svgid[len(p):].rsplit('-', 1)[0] if svgid.startswith(p) else svgid.replace('my-svg-', '')


def split_edge(eid, ids):
    # "L_A_B_0" → ("A", "B"). 노드 이름에 _가 있어도 알려진 id로 나눈다
    parts = eid[2:].rsplit('_', 1)[0].split('_')
    for i in range(1, len(parts)):
        a, b = '_'.join(parts[:i]), '_'.join(parts[i:])
        if a in ids and b in ids:
            return a, b
    return None, None


def label_text(n):
    h = re.sub(r'<br\s*/?>', '\n', n.get('html') or '')
    return html.unescape(re.sub(r'<[^>]+>', '', h)).strip() or n.get('label', '')


# ---------- 배치 정리: 머메이드 위치 유지 + 크기 통일 + 40 격자 ----------

class Box:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.r, self.b, self.cx, self.cy = x + w, y + h, x + w / 2, y + h / 2


def snap_layout(units, orig, size_of):
    """한 부모(캔버스 또는 subgraph) 안의 도형 위치를 정한다.
    1) 크기를 통일한 뒤 머메이드의 중심 위치에 두고 40 격자로 반올림한다.
    2) 원래 중심이 ALIGN_TOL 안쪽이던 도형들은 같은 줄·열로 맞춘다.
    3) 원래의 좌우·상하 순서를 지키며, 겹치게 된 도형은 40 간격을 두고 민다(밀린 줄·열은 함께 민다).
    반환: {id: [x, y]}(부모 기준, 여백 40), 부모 크기(w, h)"""
    size = {u: list(size_of(u)) for u in units}
    pos = {u: [r40(orig[u].cx - size[u][0] / 2), r40(orig[u].cy - size[u][1] / 2)] for u in units}
    groups = []
    for ax, cen in ((1, lambda u: orig[u].cy), (0, lambda u: orig[u].cx)):
        done = set()
        for u in sorted(units, key=cen):
            if u in done:
                continue
            grp = [v for v in units if v not in done and abs(cen(v) - cen(u)) < ALIGN_TOL]
            c = r40(cen(u) * 2) / 2  # 그룹 공통 중심(20 단위)
            for v in grp:
                pos[v][ax] = r40(c - size[v][ax] / 2)
                done.add(v)
            if len(grp) > 1:
                groups.append((ax, grp))

    def ov(a0, a1, b0, b1):
        return a0 < b1 - 2 and b0 < a1 - 2

    for _ in range(12):
        before = {u: tuple(pos[u]) for u in units}
        for ax in (0, 1):
            o = 1 - ax
            lo = (lambda u: orig[u].x) if ax == 0 else (lambda u: orig[u].y)
            hi = (lambda u: orig[u].r) if ax == 0 else (lambda u: orig[u].b)
            olo = (lambda u: orig[u].y) if ax == 0 else (lambda u: orig[u].x)
            ohi = (lambda u: orig[u].b) if ax == 0 else (lambda u: orig[u].r)
            for u in sorted(units, key=lo):
                for q in units:
                    if q == u or hi(q) > lo(u) + 2:
                        continue  # q가 원래 u의 앞(왼쪽·위)에 있던 도형만 본다
                    if (ov(olo(q), ohi(q), olo(u), ohi(u)) or
                            ov(pos[q][o], pos[q][o] + size[q][o], pos[u][o], pos[u][o] + size[u][o])):
                        pos[u][ax] = max(pos[u][ax], pos[q][ax] + size[q][ax] + GAP)
        for ax, grp in groups:  # 밀린 도형이 있으면 같은 줄·열 전체를 함께 민다
            c = max(pos[v][ax] + size[v][ax] / 2 for v in grp)
            for v in grp:
                pos[v][ax] = max(pos[v][ax], r40(c - size[v][ax] / 2))
        if all(tuple(pos[u]) == before[u] for u in units):
            break
    mx = min(p[0] for p in pos.values())
    my = min(p[1] for p in pos.values())
    for u in units:
        pos[u][0] -= mx - PAD
        pos[u][1] -= my - PAD
    w = max(pos[u][0] + size[u][0] for u in units) + PAD
    h = max(pos[u][1] + size[u][1] for u in units) + PAD
    return pos, size, (w, h)


def layout(lay, shapes):
    """도형과 subgraph의 부모 관계를 정하고, 안쪽 subgraph부터 배치한다."""
    items, orig = {}, {}
    for c in lay['clusters']:
        cid = 'g_' + short_id(c['id'])
        b = c['box']
        items[cid] = {'kind': 'group', 'text': c['label']}
        orig[cid] = Box(b['x'], b['y'], b['w'], b['h'])
    for n in lay['nodes']:
        nid = short_id(n['id'])
        text = label_text(n)
        shp = shapes.get(nid, 'rect')
        if text.startswith('«actor»'):
            shp, text = 'actor', text.replace('«actor»', '').strip()
        b = n['box']
        items['n_' + nid] = {'kind': 'node', 'id': nid, 'text': text, 'shape': shp}
        orig['n_' + nid] = Box(b['x'], b['y'], b['w'], b['h'])

    def inside(a, g):
        A, B = orig[a], orig[g]
        return a != g and B.x - 1 <= A.x and B.y - 1 <= A.y and A.r <= B.r + 1 and A.b <= B.b + 1

    groups = [g for g in items if items[g]['kind'] == 'group']
    for k in items:  # 부모 = 감싸는 subgraph 중 가장 작은 것
        cand = [g for g in groups if inside(k, g)]
        items[k]['parent'] = min(cand, key=lambda g: orig[g].w * orig[g].h) if cand else '1'
    kids = {}
    for k, it in items.items():
        kids.setdefault(it['parent'], []).append(k)
    result = {}

    def size_of(k):
        it = items[k]
        if it['kind'] == 'group':
            return place(k)
        return SIZE[it['shape']]

    def place(pid):
        units = kids.get(pid, [])
        if not units:
            return (G * 2, G * 2)
        pos, size, wh = snap_layout(units, orig, size_of)
        for u in units:
            result[u] = (pos[u][0], pos[u][1], size[u][0], size[u][1])
        return wh

    place('1')
    return items, result


# ---------- draw.io XML ----------

def build(src, lay, title):
    shapes, cstyles = parse_source(src)
    items, geo = layout(lay, shapes)
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def absxy(k):
        if k == '1':
            return 0, 0
        px, py = absxy(items[k]['parent'])
        return px + geo[k][0], py + geo[k][1]

    def depth(k):
        return 0 if k == '1' else 1 + depth(items[k]['parent'])

    for k in sorted(geo, key=lambda k: (items[k]['kind'] != 'group', depth(k))):  # 부모(바깥 subgraph)부터
        it = items[k]
        x, y, w, h = geo[k]
        if it['kind'] == 'group':
            style = ('rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;align=left;spacingLeft=6;' +
                     (cstyles.get(k[2:]) or GROUP_C) + FONT)
        else:
            style = STYLE[it['shape']] + FONT
            if it['shape'] != 'actor':
                extra = cstyles.get(it['id'], '')
                style += extra if 'fillColor' in extra else NODE_C + extra
        value = '<br>'.join(esc(t) for t in it['text'].split('\n'))
        cells.append(f'<mxCell id="{k}" value="{value}" style="{style}" vertex="1" parent="{it["parent"]}">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    nodes = [k for k in geo if items[k]['kind'] == 'node']

    def box(k):
        x, y = absxy(k)
        return x, y, x + geo[k][2], y + geo[k][3]

    def blocked(a, b, horizontal):
        """a와 b를 곧게(가로 또는 세로로) 이을 때 그 사이 띠를 다른 도형이 막는지."""
        A, B = box(a), box(b)
        if horizontal:
            x0, x1 = min(A[2], B[2]), max(A[0], B[0])
            y = (max(A[1], B[1]) + min(A[3], B[3])) / 2 if max(A[1], B[1]) < min(A[3], B[3]) else (A[1] + A[3]) / 2
            return any(box(k)[0] < x1 and box(k)[2] > x0 and box(k)[1] - 10 < y < box(k)[3] + 10
                       for k in nodes if k not in (a, b))
        y0, y1 = min(A[3], B[3]), max(A[1], B[1])
        x = (A[0] + A[2]) / 2
        return any(box(k)[1] < y1 and box(k)[3] > y0 and box(k)[0] - 10 < x < box(k)[2] + 10
                   for k in nodes if k not in (a, b))

    def sides(a, b):
        """나가는 변과 들어가는 변. 상대 위치로 정하고, 곧은 길이 막혀 있으면 아래(또는 오른쪽)로 돌린다."""
        A, B = box(a), box(b)
        dx = (B[0] + B[2]) / 2 - (A[0] + A[2]) / 2
        dy = (B[1] + B[3]) / 2 - (A[1] + A[3]) / 2
        if abs(dx) >= abs(dy):
            if blocked(a, b, True):
                return 'bottom', 'bottom'
            return ('right', 'left') if dx > 0 else ('left', 'right')
        if blocked(a, b, False):
            return 'right', 'right'
        return ('bottom', 'top') if dy > 0 else ('top', 'bottom')

    ids = {it['id'] for it in items.values() if it['kind'] == 'node'}
    edges = []
    for e in lay['edges']:
        if 'invisible' in (e['cls'] or ''):
            continue
        a, b = split_edge(e['id'], ids)
        if a:
            edges.append((e, 'n_' + a, 'n_' + b) + sides('n_' + a, 'n_' + b))

    # 한 변에 여러 선이 붙으면 상대 쪽 위치 순으로 변 위에 같은 간격으로 나눠 둔다(선이 한 점에 겹치지 않게)
    slots = {}
    for i, (e, a, b, sa, sb) in enumerate(edges):
        slots.setdefault((a, sa), []).append((i, b, 'out'))
        slots.setdefault((b, sb), []).append((i, a, 'in'))
    frac = {}
    for (k, sd), lst in slots.items():
        horiz_side = sd in ('top', 'bottom')  # 위·아래 변이면 x 순서로 나눈다
        lst.sort(key=lambda t: (box(t[1])[0] + box(t[1])[2]) / 2 if horiz_side else (box(t[1])[1] + box(t[1])[3]) / 2)
        for j, (i, _, d) in enumerate(lst):
            frac[(i, d)] = round((j + 1) / (len(lst) + 1), 3)

    def point(sd, f):
        return {'left': (0, f), 'right': (1, f), 'top': (f, 0), 'bottom': (f, 1)}[sd]

    for i, (e, a, b, sa, sb) in enumerate(edges):
        st = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;jumpStyle=arc;jumpSize=8;'
              'labelBackgroundColor=#ffffff;' + FONT + EDGE_C)
        if 'dotted' in e['cls'] or 'dashed' in e['cls']:
            st += 'dashed=1;'
        st += 'endArrow=block;endFill=1;' if e['end'] else 'endArrow=none;'
        if e['start']:
            st += 'startArrow=block;startFill=1;'
        ex, ey = point(sa, frac[(i, 'out')])
        nx, ny = point(sb, frac[(i, 'in')])
        st += f'exitX={ex};exitY={ey};exitPerimeter=0;entryX={nx};entryY={ny};entryPerimeter=0;'
        cells.append(f'<mxCell id="e{i + 1}" value="{esc(e["label"])}" style="{st}" edge="1" parent="1" '
                     f'source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    return (f'<mxfile host="drawio" type="device"><diagram id="d1" name="{esc(title)}">'
            '<mxGraphModel grid="1" gridSize="40" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
            'page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">'
            f'<root>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>\n')


if __name__ == '__main__':
    mmd, js, out = sys.argv[1:4]
    title = sys.argv[4] if len(sys.argv) > 4 else out.rsplit('/', 1)[-1].replace('.drawio', '')
    xml = build(open(mmd, encoding='utf-8').read(), json.load(open(js, encoding='utf-8')), title)
    open(out, 'w', encoding='utf-8').write(xml)
    print('wrote', out)
