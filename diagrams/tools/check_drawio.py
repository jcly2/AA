"""draw.io 파일 점검: 40 격자와 도형 겹침.

사용: python3 check_drawio.py <파일.drawio 또는 디렉터리>
  - 격자: 도형의 x, y, 폭, 높이가 40의 배수인지. 40보다 작은 장식 도형(포트·공)은 중심만 본다.
  - 겹침: 서로를 품지 않는 두 도형(절대 좌표)이 겹치는지.
  결과가 모두 0이어야 한다.
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET


def check(path):
    cells = {c.get('id'): c for c in ET.parse(path).getroot().iter('mxCell')}
    memo = {}

    def box(cid):
        if cid in memo:
            return memo[cid]
        c = cells[cid]
        g = c.find('mxGeometry')
        x, y = float(g.get('x', 0)), float(g.get('y', 0))
        w, h = float(g.get('width', 0)), float(g.get('height', 0))
        p = c.get('parent')
        if p in cells and cells[p].get('vertex') == '1':
            px, py, _, _ = box(p)
            x, y = x + px, y + py
        memo[cid] = (x, y, w, h)
        return memo[cid]

    verts = [cid for cid, c in cells.items() if c.get('vertex') == '1']
    off = []
    for cid in verts:
        g = cells[cid].find('mxGeometry')
        x, y = float(g.get('x', 0)), float(g.get('y', 0))
        w, h = float(g.get('width', 0)), float(g.get('height', 0))
        vals = [x + w / 2, y + h / 2] if (w < 40 and h < 40) else [x, y, w, h]
        if 'umlActor' in (cells[cid].get('style') or ''):
            vals = [x + w / 2, y, h]  # 액터는 중심 x만 격자에
        if any(abs(v / 40 - round(v / 40)) > 1e-6 for v in vals):
            off.append(cid)

    def contains(a, b):
        return a[0] <= b[0] and a[1] <= b[1] and b[0] + b[2] <= a[0] + a[2] and b[1] + b[3] <= a[1] + a[3]

    hits = []
    for i, a in enumerate(verts):
        for b in verts[i + 1:]:
            A, B = box(a), box(b)
            if contains(A, B) or contains(B, A):
                continue
            if A[0] < B[0] + B[2] and B[0] < A[0] + A[2] and A[1] < B[1] + B[3] and B[1] < A[1] + A[3]:
                hits.append((a, b))
    print(f'{os.path.basename(path):40} 격자 벗어남 {len(off)}  겹침 {len(hits)}')
    for x in off[:5]:
        print('   격자:', x, (cells[x].get('value') or '')[:20])
    for a, b in hits[:5]:
        print('   겹침:', a, b)
    return len(off) + len(hits)


if __name__ == '__main__':
    t = sys.argv[1]
    files = sorted(glob.glob(os.path.join(t, '*.drawio'))) if os.path.isdir(t) else [t]
    bad = sum(check(f) for f in files)
    print('합계', bad)
    sys.exit(1 if bad else 0)
