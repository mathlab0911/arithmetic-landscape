# r121, fable instruction 3: the paper-3 dissolution mapping table.
#
# Rule (fable r121 §2.2), applied mechanically to the claim ladder:
#   proved / Lean-verified / derived-and-verified -> Part III, as content, with its status
#   proof skeleton                                -> Part III "what is missing", as a named
#                                                    open problem, missing ingredient named
#   experimentally confirmed                      -> Part III, calibration material, with range
#   superseded by Part III                        -> dropped, with a one-line supersession note
# Nothing vanishes silently: every environment in paper3.tex appears in the output exactly once.
import os, re, collections

PAPER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'paper')
src = open(os.path.join(PAPER, 'paper3.tex'), encoding='utf-8').read()
src = '\n'.join(l for l in src.split('\n') if not l.lstrip().startswith('%'))
ENV = re.compile(r'\\begin\{(theorem|proposition|lemma|corollary|definition|remark|problem'
                 r'|conjecture)\}(\[[^\]]*\])?\s*(?:\\label\{([^}]+)\})?(.*?)\\end\{\1\}', re.S)
PROOF = re.compile(r'\A\s*\\begin\{proof\}')

# Superseded by Part III, stated here so the reason travels with the row.
SUPERSEDED = {
 'lem:kappa':   'the multiplicative kappa-transport, refuted at r-graveyard; Part III does not '
                'use it and the additive bridge replaces it',
 'rem:noKappa': 'the record of that refutation; it belongs to the graveyard note, not to '
                'Part III as content',
}

# Statuses that carry both a positive and a negative word.  The first version of this script
# matched 'proved' as a substring and sent prop:tiltlclt to MOVE -- but its status reads
# "R2 and R3 proved ...; R1 is the classical local limit computation ... written here to the
# level of its cumulant budget", i.e. it is the very gap that makes thm:rigid a skeleton.
# A classifier that guesses on mixed evidence is the failure it is meant to prevent, so mixed
# statuses are refused and must be entered here by hand, with the reason.
MIXED = re.compile(r'skeleton|not written|missing|budget|conditional|refuted|only to the level')
POSITIVE = re.compile(r'\bproved\b|\bderived\b|lean-verified')
HAND = {
 'prop:tiltlclt': ('SPLIT',
   'R2 and R3 are proved and move as content; R1 is given only to the level of its cumulant '
   'budget and is the SAME missing ingredient that thm:rigid and thm:transfer name, so it '
   'goes to "what is missing" as one open problem shared by all three'),
}

def status_text(body):
    """Everything inside \\STATUS{...}, counting braces.

    The first version used a lazy regex and stopped at the first `}` -- which, in any status
    containing a \\ref{...}, is the reference's own brace.  prop:tiltlclt's status was read as
    "R2 and R3 proved (they quote Lemmas~\\ref{lem:kappa" and classified as fully proved.  The
    bug and the misclassification were the same bug.
    """
    i = body.find('\\STATUS{')
    if i < 0:
        return ''
    j = i + len('\\STATUS{')
    depth = 1
    while j < len(body) and depth:
        if body[j] == '{':
            depth += 1
        elif body[j] == '}':
            depth -= 1
        j += 1
    return body[i + len('\\STATUS{'): j - 1]

def classify(lab, body):
    if lab in SUPERSEDED:
        return 'DROP', SUPERSEDED[lab]
    s = ' '.join(status_text(body).split())
    low = s.lower()
    if POSITIVE.search(low) and MIXED.search(low) and 'proof skeleton' not in low:
        if lab not in HAND:
            raise SystemExit(f'REFUSING TO GUESS: {lab} has a mixed status and no hand entry:\n'
                             f'  {s}\nAdd it to HAND with a reason.')
        return HAND[lab]
    if 'proof skeleton' in low:
        return 'OPEN', 'skeleton; carries into the "what is missing" section as a named open ' \
                       'problem, missing ingredient named at the statement'
    if 'refuted' in low:
        return 'DROP', 'refuted; belongs to the graveyard note'
    if 'lean-verified' in low or 'lean verified' in low:
        return 'MOVE', 'Lean-verified; moves as content with that status'
    if 'experimentally confirmed' in low:
        return 'CALIB', 'experimental; moves as calibration material, with its stated range'
    if 'proved' in low or 'derived' in low:
        return 'MOVE', 'proved/derived; moves as content with that status'
    return None, s

rows, tail = [], src
for kind, name, lab, body in ENV.findall(src):
    lab = lab or '(unlabelled)'
    # a definition or a remark with no status is decided by whether a proof follows it
    dest, why = classify(lab, body)
    if dest is None:
        i = src.find('\\end{' + kind + '}', src.find('\\label{' + lab + '}')) if lab != '(unlabelled)' else -1
        after = src[i:i+140] if i >= 0 else ''
        if kind == 'definition':
            dest, why = 'MOVE', 'definition; moves with the material that uses it'
        elif PROOF.search(after.split('}', 1)[-1]) or '\\begin{proof}' in after:
            dest, why = 'MOVE', 'proved in place (proof follows the statement); moves as content'
        else:
            dest, why = 'MOVE', 'exposition attached to material that moves; carries with it'
    rows.append((dest, kind, lab, (name or '').strip('[]'), why))

order = {'MOVE': 0, 'SPLIT': 1, 'CALIB': 2, 'OPEN': 3, 'DROP': 4}
rows.sort(key=lambda r: (order[r[0]], r[2]))
c = collections.Counter(r[0] for r in rows)
print(f'paper3.tex: {len(rows)} environments, all accounted for')
print(f'  MOVE  {c["MOVE"]:>2}   into Part III as content')
print(f'  CALIB {c["CALIB"]:>2}   into Part III as calibration material, with range')
print(f'  OPEN  {c["OPEN"]:>2}   into Part III\'s "what is missing", as named open problems')
print(f'  SPLIT {c["SPLIT"]:>2}   part moves as content, part to "what is missing"')
print(f'  DROP  {c["DROP"]:>2}   dropped, with a supersession note')
print()
print(f'{"dest":<7}{"kind":<12}{"label":<20}{"name":<40}reason')
for d, k, l, n, w in rows:
    print(f'{d:<7}{k:<12}{l:<20}{n[:38]:<40}{w}')
