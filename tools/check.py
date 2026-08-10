#!/usr/bin/env python3
"""
check.py -- the mechanised half of the failure ledger.

Ledger entries that describe a mechanical, checkable failure belong in the build,
not only in the ledger.  Each check below names the ledger entry it enforces.

  C1  F20  every experiment script has a stored log next to it
  C2  F19  every number quoted in the live report is a substring of some log
  C3  F21  exactly one live report per direction; the rest are archived
  C4  F40  no \label{} disappears from a paper without being declared
  C5  ---  repository naming convention (README): rNNN, three digits, no suffix
  C6  7.0  ledger entries written but not yet folded into the skill are surfaced, not lost
  C7  F12  every \Lean{...} the papers cite is a name that exists in the canon

Usage:  python3 tools/check.py            (from the repository root)
Exit:   0 = all pass, 1 = at least one failure.
"""
import os
import re
import sys

# The notes contain em-dashes; on a Japanese Windows console stdout is cp932 and printing them
# raises UnicodeEncodeError, so the checker dies on its own output.  (Found r115, running it
# from PowerShell instead of the sandbox for the first time.)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNP = os.path.join(ROOT, 'lean', 'pnp')
PAPER = os.path.join(ROOT, 'paper')
LABDIR = os.path.join(PAPER, '.labels')
ALLOW = os.path.join(ROOT, 'tools', 'allow_numbers.txt')

fails = []
notes = []


def fail(check, msg):
    fails.append(f'{check}: {msg}')


# ------------------------------------------------------------------ C1 (F20)
def c1_logs():
    missing = []
    for f in sorted(os.listdir(PNP)):
        m = re.fullmatch(r'(.+_r\d{2,3})\.py', f)
        if m and not os.path.exists(os.path.join(PNP, m.group(1) + '.log')):
            missing.append(f)
    if missing:
        fail('C1/F20', 'script without a stored log: ' + ', '.join(missing))
    n = len([f for f in os.listdir(PNP) if re.fullmatch(r'.+_r\d{2,3}\.py', f)])
    notes.append(f'C1/F20  scripts checked for logs: {n}')


# ------------------------------------------------------------------ C2 (F19)
def live_report():
    d = os.path.join(ROOT, 'reports', 'to-fable5')
    md = [f for f in os.listdir(d) if f.endswith('.md')]
    return os.path.join(d, md[0]) if len(md) == 1 else None


def c2_numbers():
    rep = live_report()
    if rep is None:
        notes.append('C2/F19  skipped (no unique live report)')
        return
    allow = set()
    if os.path.exists(ALLOW):
        allow = {l.split('#')[0].strip() for l in open(ALLOW, encoding='utf-8')}
        allow.discard('')
    blob = ''
    for f in os.listdir(PNP):
        if f.endswith('.log'):
            blob += open(os.path.join(PNP, f), encoding='utf-8', errors='replace').read()
    quoted, bad = set(), []
    for line in open(rep, encoding='utf-8').read().splitlines():
        if not line.lstrip().startswith('|'):
            continue
        for tok in re.findall(r'\d+\.\d{2,}', line):
            quoted.add(tok)
    for tok in sorted(quoted):
        if tok in allow:
            continue
        if tok not in blob and tok.rstrip('0') not in blob:
            bad.append(tok)
    if bad:
        fail('C2/F19', f'number(s) in {os.path.basename(rep)} not found in any log '
                       f'(compute it in a script or allow-list it): ' + ', '.join(bad))
    notes.append(f'C2/F19  table numbers checked against logs: {len(quoted)}')


# ------------------------------------------------------------------ C3 (F21)
def c3_one_live():
    for d in ('to-fable5', 'to-opus5'):
        p = os.path.join(ROOT, 'reports', d)
        live = [f for f in os.listdir(p) if f.endswith('.md')]
        if len(live) != 1:
            fail('C3/F21', f'reports/{d} holds {len(live)} live reports '
                           f'({", ".join(sorted(live)) or "none"}); it must hold exactly one')
    notes.append('C3/F21  one live report per direction')


# ------------------------------------------------------------------ C4 (F40)
def c4_labels():
    os.makedirs(LABDIR, exist_ok=True)
    for tex in sorted(f for f in os.listdir(PAPER) if f.endswith('.tex')):
        stem = tex[:-4]
        src = open(os.path.join(PAPER, tex), encoding='utf-8', errors='replace').read()
        now = set(re.findall(r'\\label\{([^}]+)\}', src))
        snap = os.path.join(LABDIR, stem + '.txt')
        if os.path.exists(snap):
            was = {l.strip() for l in open(snap, encoding='utf-8') if l.strip()}
            gone = was - now
            if gone:
                fail('C4/F40', f'{tex}: label(s) removed since the last run: '
                               + ', '.join(sorted(gone))
                               + '  -- if intended, delete the line from '
                               + os.path.relpath(snap, ROOT))
                continue
            new = now - was
            if new:
                notes.append(f'C4/F40  {tex}: +{len(new)} new label(s)')
        else:
            notes.append(f'C4/F40  {tex}: snapshot created ({len(now)} labels)')
        with open(snap, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(sorted(now)) + '\n')


# ------------------------------------------------------------------ C5
def c5_naming():
    bad = []
    for d in ('to-fable5', 'to-opus5'):
        base = os.path.join(ROOT, 'reports', d)
        for sub in ('', 'archive'):
            p = os.path.join(base, sub)
            if not os.path.isdir(p):
                continue
            for f in os.listdir(p):
                if f.endswith('.md') and not re.fullmatch(r'r\d{3}\.md', f):
                    bad.append(os.path.join(d, sub, f))
    if bad:
        fail('C5', 'report name(s) off convention rNNN.md: ' + ', '.join(bad))
    notes.append('C5      report naming')


def c6_pending():
    p = os.path.join(ROOT, 'tools', 'ledger_pending.md')
    if not os.path.exists(p):
        return
    heads = [l.strip() for l in open(p, encoding='utf-8') if l.startswith('## ')]
    if heads:
        notes.append('C6      ledger entries PENDING a skill save: '
                     + '; '.join(h[3:] for h in heads))


# ------------------------------------------------------------------ C7 (F12)
# "Verify a citation against the actual document" applied to our own canon: a \Lean{name} in a
# paper is a citation, and a theorem that is renamed or removed leaves the paper claiming a
# machine check that no longer exists.  This checks the NAME only -- whether the statement is
# the intended one is F52's job (two-route proofs), and the two axes must not be confused (F54).
LEAN_NOISE = re.compile(
    r'^(Classical\.choice|Quot\.sound|propext|sorryAx|sorry|IsStrictLocalMin|name'
    r'|Theory/.*|\\#.*|lake build|leanprover/.*)$')


def c7_lean_citations():
    thy = os.path.join(PNP, 'Pnp', 'Theory')
    if not os.path.isdir(thy):
        notes.append('C7/F12  skipped (no Pnp/Theory)')
        return
    canon = set()
    decl = re.compile(r"^\s*(?:private\s+)?(?:noncomputable\s+)?"
                      r"(?:theorem|lemma|def|abbrev)\s+([A-Za-z_][A-Za-z0-9_']*)")
    for f in os.listdir(thy):
        if f.endswith('.lean'):
            for line in open(os.path.join(thy, f), encoding='utf-8', errors='replace'):
                m = decl.match(line)
                if m:
                    canon.add(m.group(1))
    cited = set()
    for tex in sorted(f for f in os.listdir(PAPER) if f.endswith('.tex')):
        src = open(os.path.join(PAPER, tex), encoding='utf-8', errors='replace').read()
        for nm in re.findall(r'\\Lean\{([^}]*)\}', src):
            nm = nm.replace('\\_', '_').strip()
            if nm and not LEAN_NOISE.match(nm):
                cited.add(nm)
    missing = sorted(cited - canon)
    if missing:
        fail('C7/F12', 'the papers cite Lean name(s) that are not in Pnp/Theory: '
                       + ', '.join(missing))
    notes.append(f'C7/F12  Lean citations checked against the canon: {len(cited)}')


# ------------------------------------------------------------------ C8 (F38)
# Every theorem-like environment must declare its status somehow.  An external review found
# prop:ripple stating a Laplace formula with no marking at all, so a reader could not tell a
# theorem from a calibrated ansatz without re-deriving it.  That was found by a human reading
# carefully; this is the same question asked mechanically.
#
# Four things count as declaring a status, and the list is deliberately generous -- the check
# is for SILENCE, not for a house style:
#   * an explicit \STATUS{...} on or beside the statement;
#   * a \Lean{...} citation (kernel-verified is the strongest status there is);
#   * a plain \begin{proof} following it (the status is "proved, here");
#   * being a \begin{conjecture} (the environment names its own status).
# What fails: no proof at all, or a proof whose optional argument QUALIFIES it -- Derivation,
# Outline, Sketch.  Those are the author signalling a caveat without saying what it is.
STATUS_ENVS = ('theorem', 'proposition', 'lemma', 'corollary')
QUALIFIED = ('derivation', 'outline', 'sketch', 'idea', 'heuristic', 'informal', 'partial')

def c8_status_at_statement():
    checked, bad = 0, []
    for tex in sorted(f for f in os.listdir(PAPER) if f.endswith('.tex')):
        lines = open(os.path.join(PAPER, tex), encoding='utf-8', errors='replace').read().split('\n')
        stack, envs = [], []
        for i, L in enumerate(lines):
            for e in STATUS_ENVS + ('conjecture',):
                if '\\begin{%s}' % e in L:
                    stack.append((e, i))
                if '\\end{%s}' % e in L and stack:
                    e0, i0 = stack.pop()
                    if e0 in STATUS_ENVS:
                        envs.append((e0, i0, i))
        starts = sorted(a for _, a, _ in envs)
        for e, a, b in envs:
            checked += 1
            body = '\n'.join(lines[max(0, a - 3):min(len(lines), b + 4)])
            nxt = next((s for s in starts if s > b), len(lines))
            after = '\n'.join(lines[b + 1:nxt])
            if '\\STATUS' in body or '\\Lean{' in body or '\\Lean{' in after[:400]:
                continue
            m = re.search(r'\\begin\{proof\}(?:\[([^\]]*)\])?', after)
            lab = re.search(r'\\label\{([^}]+)\}', '\n'.join(lines[a:b + 1]))
            lab = lab.group(1) if lab else 'line %d' % (a + 1)
            if m is None:
                bad.append('%s %s (no proof, no \\STATUS, no \\Lean)' % (tex, lab))
            elif any(q in (m.group(1) or '').lower() for q in QUALIFIED):
                bad.append('%s %s (proof[%s] without a \\STATUS)' % (tex, lab, m.group(1)))
    if bad:
        fail('C8/F38', 'statement(s) whose status a reader cannot determine at the '
                       'statement: ' + '; '.join(bad))
    notes.append('C8/F38  theorem-like statements checked for a declared status: %d' % checked)


# ------------------------------------------------------------------ C9 (F59)
# The README is the first thing an outside reader sees, and it is the artefact nobody
# remembers to update.  Every count it states is checked here against the repository.
# Found the hard way: it claimed 13 canon files, 120 theorems, 14 replayed modules, 114
# scripts and 172 logs when the true numbers were 14, 125, 16, 115 and 182 -- and, worse,
# described papers 2 and 3 as "Complete" while the papers themselves say two steps are not
# written to referee standard and two theorems are proof skeletons.  The counts are
# mechanical, so they are asserted; the prose is not, so it is a standing review item.
def c9_readme_counts():
    path = os.path.join(ROOT, 'README.md')
    if not os.path.exists(path):
        notes.append('C9/F59  skipped (no README.md)')
        return
    src = open(path, encoding='utf-8', errors='replace').read()
    theory = os.path.join(ROOT, 'lean', 'pnp', 'Pnp', 'Theory')
    lean_files = sorted(f for f in os.listdir(theory) if f.endswith('.lean')) if os.path.isdir(theory) else []
    n_thm = 0
    for f in lean_files:
        for line in open(os.path.join(theory, f), encoding='utf-8', errors='replace'):
            if re.match(r'\s*(theorem|lemma)\s', line):
                n_thm += 1
    # the replayed set is the import closure of the root module, not the directory
    proj = os.path.join(ROOT, 'lean', 'pnp')
    closure, stack = set(), ['Pnp']
    while stack:
        m = stack.pop()
        if m in closure:
            continue
        closure.add(m)
        p = os.path.join(proj, *m.split('.')) + '.lean'
        if not os.path.exists(p):
            continue
        for line in open(p, encoding='utf-8', errors='replace'):
            g = re.match(r'\s*import\s+(Pnp[\w.]*)', line)
            if g:
                stack.append(g.group(1))
    expdir = os.path.join(ROOT, 'lean', 'pnp')
    n_py = len([f for f in os.listdir(expdir) if f.endswith('.py')])
    n_log = len([f for f in os.listdir(expdir) if f.endswith('.log')])

    claims = [
        (r'\*\*(\d+) files, (\d+) theorems and lemmas\*\*', (len(lean_files), n_thm),
         'canon files / theorems'),
        (r'lean4checker\W{0,3},\s*\*{0,2}(\d+) modules', (len(closure),), 'replayed modules'),
        (r'\*\*(\d+) scripts, (\d+) logs\*\*', (n_py, n_log), 'scripts / logs'),
    ]
    bad = []
    for pat, truth, what in claims:
        m = re.search(pat, src)
        if not m:
            bad.append('%s: the README no longer states this, so it cannot be checked' % what)
            continue
        said = tuple(int(g) for g in m.groups())
        if said != truth:
            bad.append('%s: README says %s, repository has %s'
                       % (what, ' / '.join(map(str, said)), ' / '.join(map(str, truth))))
    # page counts in the papers table, best effort -- pdfinfo may not be present
    try:
        import subprocess
        for n, stem in ((1, 'paper'), (2, 'paper2'), (3, 'paper3'), (4, 'paper4')):
            pdf = os.path.join(PAPER, stem + '.pdf')
            row = re.search(r'^\| %d \|.*?\*\*(\d+) pp\.' % n, src, re.M)
            if not (row and os.path.exists(pdf)):
                continue
            out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
            real = re.search(r'^Pages:\s+(\d+)', out, re.M)
            if real and int(real.group(1)) != int(row.group(1)):
                bad.append('paper %d: README says %s pp., PDF has %s pp.'
                           % (n, row.group(1), real.group(1)))
    except (OSError, ImportError):
        pass
    if bad:
        fail('C9/F59', 'the README states counts the repository does not support: '
                       + '; '.join(bad))
    notes.append('C9/F59  README counts checked against the repository: %d' % len(claims))


# ------------------------------------------------------------------ C10 (F39)
# The one link a stranger will actually click.  paper2.tex pointed at
# github.com/mathlab0911/arithmetic-landscape -- singular, a 404 -- in a PDF that had already
# been sent to someone deciding whether the work was serious.  Nothing catches a URL that is
# merely wrong: it compiles, it renders, and only a reader finds out.
REPO_URL = 'https://github.com/mathlab0911/arithmetic-landscapes'

def c10_repo_url():
    bad, seen = [], 0
    for tex in sorted(f for f in os.listdir(PAPER) if f.endswith('.tex')):
        src = open(os.path.join(PAPER, tex), encoding='utf-8', errors='replace').read()
        urls = re.findall(r'https?://github\.com/mathlab0911/[A-Za-z0-9_.\-]*', src)
        if not urls:
            bad.append('%s cites the repository nowhere -- a reader of it alone cannot find '
                       'the code or the Lean development' % tex)
            continue
        for u in urls:
            seen += 1
            if u.rstrip('.') != REPO_URL:
                bad.append('%s points at %s, not %s' % (tex, u, REPO_URL))
    if bad:
        fail('C10/F39', '; '.join(bad))
    notes.append('C10/F39 repository links in the papers checked: %d' % seen)


if __name__ == '__main__':
    for fn in (c1_logs, c2_numbers, c3_one_live, c4_labels, c5_naming, c6_pending,
               c7_lean_citations, c8_status_at_statement, c9_readme_counts, c10_repo_url):
        fn()
    for n in notes:
        print('  ok   ' + n)
    if fails:
        print()
        for f in fails:
            print('  FAIL ' + f)
        sys.exit(1)
    print('\nall checks pass')
