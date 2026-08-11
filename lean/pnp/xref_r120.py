# r120: the consolidation inventory (fable r119 item 3).
#
# Before P-II and P-III can be assembled, we need the denominator: how many places in
# papers 2, 3 and 4 point at a sibling paper, and what each one will need when the series
# becomes P-I / P-II / P-III and paper 3 dissolves into P-III.
#
# Three kinds, in increasing order of danger:
#   (1) prose  -- "the companion paper", "paper 2", "papers 1-3".  Needs rewording.
#   (2) label  -- \Xlab{stem}{label}: names a label in a sibling.  Survives renaming;
#                 breaks only if the label is deleted.  Checked by C15.
#   (3) number -- \Xref{stem}{label}{n}: prints a sibling's number.  Breaks whenever the
#                 sibling is renumbered.  Two of the three were already broken at r120.
import os, re, collections

PAPER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'paper')
FILES = {1: 'paper', 2: 'paper2', 3: 'paper3', 4: 'paper4'}

PROSE = re.compile(
    r'companion paper|sister paper|sibling paper'
    r'|[Pp]apers?~?\s?[1-4]\b|[Pp]apers?\s?1[-–—]{1,2}\s?[0-9]')
XREF = re.compile(r'\\Xref\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}')
XLAB = re.compile(r'\\Xlab\{([^}]+)\}\{([^}]+)\}')

def body(stem):
    src = open(os.path.join(PAPER, stem + '.tex'), encoding='utf-8', errors='replace')
    return [l for l in src.read().split('\n') if not l.lstrip().startswith('%')]

def prose_body(stem):
    """Body with the \\Xref / \\Xlab macro arguments blanked out.

    First count came to 97 because {paper2} and {paper3} inside the new macros were being
    read as prose references to those papers.  A denominator that counts the instrument is
    not a denominator."""
    out = []
    for l in body(stem):
        l = re.sub(r'\\Xref\{[^}]*\}\{[^}]*\}\{[^}]*\}', 'XREF', l)
        l = re.sub(r'\\Xlab\{[^}]*\}\{[^}]*\}', 'XLAB', l)
        out.append(l)
    return out

def numbers(stem):
    path = os.path.join(PAPER, stem + '.aux')
    if not os.path.exists(path):
        return None
    src = open(path, encoding='utf-8', errors='replace').read()
    return {m.group(1): m.group(2) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', src)}

print('=== the denominator: prose references to a sibling paper ===')
tot = 0
which = collections.Counter()
for n, stem in FILES.items():
    c = 0
    for line in prose_body(stem):
        for m in PROSE.finditer(line):
            c += 1
            which[m.group(0).lower().strip()] += 1
    print(f'  paper{n}: {c}')
    tot += c
print(f'  TOTAL {tot}   <- every one of these needs rewording for P-I / P-II / P-III')
print('  by phrase:')
for k, v in which.most_common():
    print(f'    {v:>3}  {k}')

print()
print('=== resolvable references, and whether they resolve ===')
ok = bad = 0
for n, stem in FILES.items():
    src = '\n'.join(body(stem))
    for tgt, lab, printed in XREF.findall(src):
        nums = numbers(tgt) or {}
        good = nums.get(lab) == printed
        ok, bad = ok + good, bad + (not good)
        print(f'  paper{n}  \\Xref -> {tgt}:{lab} prints {printed}; '
              f'sibling says {nums.get(lab, "NO SUCH LABEL")}  {"ok" if good else "MISMATCH"}')
    for tgt, lab in XLAB.findall(src):
        nums = numbers(tgt) or {}
        good = lab in nums
        ok, bad = ok + good, bad + (not good)
        print(f'  paper{n}  \\Xlab -> {tgt}:{lab} = {nums.get(lab, "NO SUCH LABEL")}  '
              f'{"ok" if good else "MISSING"}')
print(f'  {ok} resolve, {bad} do not')

print()
print('=== bibliography entries for siblings that are never cited ===')
for n, stem in FILES.items():
    src = '\n'.join(body(stem))
    declared = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', src))
    cited = set()
    for m in re.finditer(r'\\cite\{([^}]+)\}', src):
        cited |= {k.strip() for k in m.group(1).split(',')}
    orphan = sorted(k for k in declared - cited if re.fullmatch(r'P[1-4]', k))
    if orphan:
        print(f'  paper{n}: {", ".join(orphan)} declared but never \\cite-d '
              f'-- the sibling is referred to in prose instead')
