# r130: the file-level DROP_GUARD, before retiring paper 3 from the tree.
#
# Same asymmetry as the r123 guard on the mapping table: additions announce themselves at
# build time, deletions do not.  Paper 3's 33 environments are all carried by Part III
# (MOVE 22 / CALIB 8 / OPEN 2 / SPLIT 1 / DROP 0), so the file is a duplicate -- but a
# duplicate that something still points at is not a duplicate, it is a dependency.
#
# Refuses the removal if any live reference to the retired stems survives anywhere the
# repository shows a reader.
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RETIRING = ['paper3.tex', 'paper3.pdf', 'paper3_ja.tex', 'paper3_ja.pdf']
STEMS = ['paper3', 'paper3_ja']
OLD_TITLE_BITS = ['The transfer function of subset-sum landscapes',
                  '部分和地形の転送関数']

# A mention is not a dependency.  The first version grepped every .tex/.py/.md in the tree
# and refused on twelve hits that were, by then, comments explaining the retirement -- the
# guard detecting its own success.  So it asks two different questions instead.
#
#   (1) Can a READER reach a reference?  Only the built documents and the two READMEs are
#       reader-facing.  A citation, a cross-document macro, an \input, or a README row
#       describing the file as present, is a dependency.
#   (2) Can a TOOL still run?  Not by grep -- by running it.  A script that opens the file
#       either handles its absence or it does not, and only executing it says which.
#
# A comment that records the retirement passes both, correctly.
import subprocess, tempfile, shutil

READER_FACING = [os.path.join('paper', f) for f in sorted(os.listdir(os.path.join(ROOT, 'paper')))
                 if f.endswith('.tex') and f not in RETIRING]
READER_FACING += [os.path.join('paper-ja', f)
                  for f in sorted(os.listdir(os.path.join(ROOT, 'paper-ja')))
                  if f.endswith('.tex') and f not in RETIRING]
READER_FACING += ['README.md', os.path.join('paper-ja', 'README.md')]

PATTERNS = [
    (r'\\Xref\{paper3\}|\\Xlab\{paper3\}', 'a cross-document macro'),
    (r'\\cite\{[^}]*\bP3\b[^}]*\}|\\bibitem\{P3\}', 'a citation of the retired manuscript'),
    (r'\\(?:input|include)\{[^}]*paper3', 'an \\input'),
    (r'`paper3(?:_ja)?\.(?:tex|pdf)`', 'a README row naming the file'),
    # The retired title in a TITLE POSITION -- a row of the papers table, or a \title{} --
    # means an artefact still presents itself under it.  Naming it in the historical note
    # that records the retirement is not that, and must not be refused: you cannot say what
    # was retired without saying its name.
    (r'^\|.*(?:' + '|'.join(re.escape(t) for t in OLD_TITLE_BITS) + ')'
     r'|\\title\{[^}]*(?:' + '|'.join(re.escape(t) for t in OLD_TITLE_BITS) + ')',
     'the retired title in a title position'),
]

print(f'(1) reader-facing scan: {len(READER_FACING)} file(s)')
hits = collections.defaultdict(list)
for rel in READER_FACING:
    src = open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read()
    for ln, line in enumerate(src.split('\n'), 1):
        if line.lstrip().startswith(('%', '<!--')):
            continue
        for rx, why in PATTERNS:
            if re.search(rx, line):
                hits[why].append((rel, ln, line.strip()[:100]))
total = sum(len(v) for v in hits.values())
for why, items in hits.items():
    print(f'  [{len(items)}] {why}')
    for rel, ln, txt in items:
        print(f'      {rel}:{ln}  {txt}')
print(f'  -> {total} reader-facing reference(s)')

print()
print('(2) functional: do the tools survive the removal?')
tmp = tempfile.mkdtemp()
shadow = os.path.join(tmp, 'study')
shutil.copytree(ROOT, shadow, ignore=shutil.ignore_patterns('.git', '.lake', '*.olean'))
for f in RETIRING:
    for d in ('paper', 'paper-ja'):
        q = os.path.join(shadow, d, f)
        if os.path.exists(q):
            os.remove(q)
oks = []
for name, cmd in (('check.py', ['python3', 'tools/check.py']),
                  ('terms_r128', ['python3', 'lean/pnp/terms_r128.py']),
                  ('p3map_r121', ['python3', 'lean/pnp/p3map_r121.py'])):
    r = subprocess.run(cmd, cwd=shadow, capture_output=True, text=True)
    first = (r.stdout + r.stderr).strip().split('\n')[0][:90]
    if name == 'p3map_r121':
        good = r.returncode == 1 and 'retired from the tree' in (r.stdout + r.stderr)
        verdict = 'stops with an explanation' if good else 'CRASHES OR LIES'
    else:
        good = r.returncode == 0
        verdict = 'passes' if good else 'FAILS'
    oks.append(good)
    print(f'  {name:<14} exit {r.returncode}  {verdict}')
    if not good:
        print(f'      {first}')
shutil.rmtree(tmp, ignore_errors=True)

print()
if total or not all(oks):
    print(f'REFUSING THE REMOVAL: {total} reader-facing reference(s); '
          f'{oks.count(False)} tool(s) not ready.')
    sys.exit(1)
print('no reader-facing reference survives, and every tool handles the absence.')
print('the removal is safe.')
