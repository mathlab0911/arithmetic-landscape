# r128: the terminology inventory.  Dirk Zeindler declined the endorsement because the
# papers "make extensive use of non-standard terminology".  Before changing anything, count.
#
# Mechanical handle: LaTeX convention italicises a term where it is defined.  So for each
# term we can ask two things the source can answer:
#   (a) how often it is used, and
#   (b) whether its FIRST occurrence in the paper is the italicised one.
# A term first used in plain text and only italicised later is a term the reader met before
# it was defined -- which is precisely the complaint.
import os, re, collections

PAPER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'paper')
FILES = [('I','paper.tex'), ('II','paper2.tex'), ('(3)','paper3.tex'), ('III','paper4.tex')]

# Terms this programme coined or repurposed, as opposed to importing.  Listed by hand,
# because "is this standard in additive number theory" is not a question a regex can answer.
COINED = [
 'gap series', 'subset-sum landscape', 'landscape', 'window series', 'window identity',
 'window measure', 'stratification', 'stratum', 'strata', 'flatness', 'sandwich',
 'transfer function', 'the tilt', 'logarithmic slope', 'biased invariant',
 'coarse-graining identity', 'coset identity', 'sub-peak', 'annulus profile',
 'deep minor arc', 'ground state', 'energy', 'valley', 'ripple',
]
# Standard terms, listed so the report can show the ratio rather than only the bad half.
STANDARD = [
 'representation count', 'generating polynomial', 'circle method', 'major arc', 'minor arc',
 'local limit theorem', 'Edgeworth', 'cumulant', 'Ramanujan sum', 'cyclotomic',
 'Dirichlet kernel', 'Siegel--Walfisz', 'partition', 'exponential sum',
]

def body(p):
    s = open(p, encoding='utf-8', errors='replace').read()
    s = '\n'.join(l for l in s.split('\n') if not l.lstrip().startswith('%'))
    return s

print('=== how much coined vocabulary is there, and is it introduced before it is used? ===')
print(f'{"term":<26}{"I":>6}{"II":>6}{"(3)":>6}{"III":>6}   first use italicised?')
rows = []
for t in COINED:
    counts, flags = [], []
    for tag, f in FILES:
        s = body(os.path.join(PAPER, f))
        n = len(re.findall(re.escape(t), s, re.I))
        counts.append(n)
        if n:
            first = re.search(re.escape(t), s, re.I).start()
            # italicised or in a definition environment within 40 chars before
            ctx = s[max(0, first-40):first]
            ok = ('\\emph{' in ctx or '\\textit{' in ctx or '\\begin{definition}' in ctx
                  or '\\textbf{' in ctx)
            flags.append(f'{tag}:{"y" if ok else "N"}')
    rows.append((sum(counts), t, counts, flags))
rows.sort(reverse=True)
for tot, t, c, fl in rows:
    if tot == 0: continue
    print(f'{t:<26}' + ''.join(f'{x if x else "-":>6}' for x in c) + '   ' + ' '.join(fl))
tot_coined = sum(r[0] for r in rows)
tot_std = 0
for t in STANDARD:
    for _, f in FILES:
        tot_std += len(re.findall(re.escape(t), body(os.path.join(PAPER, f)), re.I))
print()
print(f'coined-vocabulary occurrences : {tot_coined}')
print(f'standard-vocabulary occurrences: {tot_std}')
print(f'ratio coined : standard = {tot_coined/max(tot_std,1):.2f} : 1')
print()
print('=== terms whose FIRST occurrence in a paper is not the definition (N above) ===')
bad = [(t, fl) for _, t, _, fl in rows for fl in [fl] if any(x.endswith(':N') for x in fl)]
for t, fl in bad:
    print(f'  {t:<26} {" ".join(x for x in fl if x.endswith(":N"))}')
print(f'  {len(bad)} term(s) met before they are introduced, somewhere in the series')
