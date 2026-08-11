# r129: a coherence pass after a day of surgery.  Ten commits touched every paper -- the
# definition of Gamma, the symbol for the representation count, three abstracts, the
# terminology tables, the assembly of Part III.  Each edit was checked; the SEAMS were not.
# This looks for the specific ways those edits can leave a paper contradicting itself.
import os, re

PAPER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'paper')
LIVE = ['paper.tex', 'paper2.tex', 'paper4.tex']

def body(f):
    s = open(os.path.join(PAPER, f), encoding='utf-8', errors='replace').read()
    return '\n'.join(l for l in s.split('\n') if not l.lstrip().startswith('%'))

PROBES = [
 # (name, regex, why this would be a seam defect)
 ('ground-state phrasing left beside r_A',
  r'number of ground states \$r_A|ground states? \$r_A\(',
  'after the rename, "the number of ground states r_A(n)" reads as two names again'),
 ('deg survivors', r'\\deg|\bdeg_[A-Zq]',
  'the physics symbol should be gone everywhere'),
 ('order-sensitive survivors', r'order-sensitive|order-blind',
  'retired with the layer definition'),
 ('two names for the window measure', r'window measure',
  'should appear only in the terminology row that retires it'),
 ('coarse-graining survivors', r'coarse-graining',
  'the identity has one name now'),
 ('lm defined only as local minima', r'\\lm_A\(n\)\s*=\s*\\#\{S',
  'paper 1 now defines lm by the representation-count sum first; a bare set-builder '
  'definition elsewhere is the old framing'),
 ('abstract still promises deg', r'\\deg_A\(n\) the number of',
  'stale abstract phrasing'),
]
print('=== seam probes ===')
tot = 0
for name, rx, why in PROBES:
    hits = []
    for f in LIVE:
        for m in re.finditer(rx, body(f)):
            ctx = body(f)[max(0, m.start()-60):m.start()+50].replace('\n', ' ')
            hits.append((f, ctx))
    print(f'{name:<42} {len(hits)}')
    for f, c in hits[:4]:
        print(f'      {f}: …{c}…')
    tot += len(hits)
print(f'total probe hits: {tot}')

print()
print('=== does each live paper still define what it uses first? ===')
for f in LIVE:
    s = body(f)
    i = s.find('\\end{abstract}')
    b = s[i:]
    first_r  = re.search(r'r_A\(n\)|r_B\(m\)|r_\{B', b)
    first_def= re.search(r'r_A\(n\)\s*=\s*\\#|r_B\(m\)\s*=\s*\\#|representation count', b)
    print(f'  {f:<12} first use of a representation count at {first_r.start() if first_r else "-":>6}'
          f'   first gloss at {first_def.start() if first_def else "-":>6}'
          f'   {"ok" if (first_def and first_r and first_def.start() <= first_r.start()+400) else "check"}')

print()
print('=== terminology tables: rows, and whether each row is glossed in ordinary language ===')
for f in LIVE:
    s = body(f)
    m = re.search(r'\\subsection\{Terminology[^}]*\}', s)
    if not m: print(f'  {f}: NO TABLE'); continue
    nxt = re.search(r'\\(?:sub)*section\{', s[m.end():])
    region = s[m.start(): m.end()+ (nxt.start() if nxt else 0)]
    rows = [r for r in region.split('\\\\[3pt]') if '&' in r]
    print(f'  {f:<12} {len(rows)} row(s)')
