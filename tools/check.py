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

Usage:  python3 tools/check.py            (from the repository root)
Exit:   0 = all pass, 1 = at least one failure.
"""
import os
import re
import sys

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


if __name__ == '__main__':
    for fn in (c1_logs, c2_numbers, c3_one_live, c4_labels, c5_naming):
        fn()
    for n in notes:
        print('  ok   ' + n)
    if fails:
        print()
        for f in fails:
            print('  FAIL ' + f)
        sys.exit(1)
    print('\nall checks pass')
