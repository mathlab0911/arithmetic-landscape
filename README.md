# Arithmetic Landscape Theory

Research repository for the **gap series** `Γ(A) = Σ_{j=1..k} a_j / 2^j`, an order-sensitive
arithmetic invariant that governs the local structure of subset-sum landscapes.

**Status:** private while the papers are unpublished. Submission is held until paper 3 is written.

| | Title | State |
|---|---|---|
| Paper 1 | *The gap series of an integer sequence: an arithmetic invariant governing subset-sum landscapes* | 20 pp, frozen, no hypotheses |
| Paper 2 | *Asymptotic flatness of subset-sum landscapes of primes: the sub-peak spectrum and the constant √3/2* | 30 pp, no hypotheses (ineffective at one point, via Siegel–Walfisz) |
| Paper 3 | rigidity + the λ² correction law | in progress |

---

## Layout

| Path | Contents |
|---|---|
| `paper/` | The two papers (LaTeX + built PDF). Built in the sandbox with `pdflatex`. |
| `lean/pnp/Pnp/Theory/` | The formal development — the canon. 9 files, 99 theorems, `sorry` 0, extra axioms 0. |
| `lean/pnp/Pnp/Experiments/` | Throwaway Lean experiments. |
| `lean/pnp/*.py`, `*.log` | Numerical experiments. **Every number in the papers comes from a `.log` here.** |
| `book/` | Source of the Japanese introductory series (`*.md` + `build.py`). |
| `reports/` | Model-to-model reports. See below. |
| `explainer/` | Per-round explanation PDFs for the author (Japanese). |
| `docs/` | Documents meant to be read by a human or sent outside. |
| `archive/` | Superseded one-off documents, kept for history. |
| `入門_第N巻_*.pdf` | The introductory series, built from `book/`. The main human-facing deliverable. |

---

## Naming convention

Everything follows `<kind>_<key>[_<date>].<ext>`, with these fixed rules:

- **Round numbers are always `rNNN`, zero-padded to three digits.** `r013`, `r081`. This is what
  makes directory listings sort correctly; `r13` sorting after `r120` has bitten us.
- **Dates are always ISO `YYYY-MM-DD`.** Never `0809`, never a letter suffix.
- **Never disambiguate with a letter.** Two files from the same day get different round numbers,
  not `...b.pdf` and `...c.pdf`. (The `explainer/` directory was renamed out of exactly that.)
- **A file that gets replaced rather than accumulated carries no date** — the books, the papers.
  Git holds their history.

| kind | pattern | example |
|---|---|---|
| model-to-model report | `reports/to-<model>/rNNN.md` | `reports/to-opus5/r081.md` |
| round explainer (JA) | `explainer/解説_rNNN_YYYY-MM-DD.pdf` | `explainer/解説_r064_2026-08-09.pdf` |
| book volume (JA) | `入門_第N巻_<題>.pdf` | `入門_第2巻_平らになる.pdf` |
| procedure for the author (JA) | `docs/手順_<主題>.md` | `docs/手順_arXiv投稿_論文1.md` |
| reply to an external review (JA) | `docs/回答_<相手>_rNNN.md` | `docs/回答_外部評価_r064.md` |
| material sent outside | `docs/相談_<主題>_YYYY-MM-DD.md` | `docs/相談_補正法則の謎_2026-08-09.md` |
| experiment / design spec | `lean/pnp/spec_<主題>_rNNN.md` | `lean/pnp/spec_paper3-experiments_r073.md` |
| experiment script + log | `lean/pnp/<name>_rNNN.py` / `.log` | `lean/pnp/e4d_r082.py` |

## `reports/` — one live file per direction

```
reports/
├── to-fable5/          reports opus-5 writes for fable-5
│   ├── r080.md         ← the live one: exactly one file here
│   └── archive/        r013.md … r078.md
└── to-opus5/           reports fable-5 writes for opus-5
    ├── r081.md         ← the live one
    └── archive/        r019.md … r079.md
```

**Rule: when a new report is written, the previous one moves to `archive/` in the same commit.**
The top of each directory always shows the one document that is currently in play. Nothing is
deleted.

### One exception, deliberately left alone

Experiment scripts and logs written before round 082 use two-digit round numbers
(`e4d_r80.py`). They are referenced by name from the archived reports, so renaming them would
break the trail. **The three-digit rule applies to everything created from round 082 onward.**
