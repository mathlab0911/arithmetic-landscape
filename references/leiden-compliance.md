# The Leiden Declaration, and how this project answers it

The author signed the [Leiden Declaration on Artificial Intelligence and Mathematics]
(https://leidendeclaration.ai/) (June 2026, DOI 10.5281/zenodo.20302944; endorsed by the
IMU) on 2026-08-15, ORCID 0009-0000-0890-4395. This file maps each recommendation for
individual mathematicians (01–11) to the concrete practice of this repository, and it is
kept honest in both directions: **where we exceed a recommendation we say how, and where
we fail one we say so** — the same posture as the public signature comment.

This document describes practice; it is not itself a check. The mechanical checks that
enforce the practices below are listed in the README, C1–C20.

| # | Recommendation | This project |
|---|---|---|
| 01 | **Disclose tool use** — a "Tool and computational resource disclosure" section in papers | **Met, by that name.** Every paper and every Japanese edition carries *Tool and computational resource disclosure* (renamed from *Use of AI tools* to the section name the Declaration specifies), covering the language models used and their role, the proof assistant (Lean 4 / Mathlib, versions stated), the independent kernel checker, and the compute (one personal computer; no cluster; longest single computation ≈ 3 minutes). C16 fails the build if any paper lacks the section, and fails — rather than passes — when it can find no section at all. |
| 02 | **Support the needs of reviewing** — disclose, cite precisely, provide formal proofs where feasible | **Met.** Every theorem-like statement declares its status at the statement (C8); settled structural results are Lean-verified and replayed through the kernel against poisoned negative controls; every number in a paper traces to a committed script with a log (C1/C2/C12); cross-document references resolve mechanically against the sibling's build (C15). |
| 03 | **Open science** | **Met.** Public repository; manuscripts CC BY 4.0; code Apache-2.0 (matching Mathlib); archived and versioned at Zenodo (concept DOI 10.5281/zenodo.21941261), with the caveat *a DOI makes a version permanent; it does not make it true* printed where the badge is copied. |
| 04 | **Retain the responsibility for correctness** | **Met, verbatim.** The disclosure section of every paper states that the choice of problem, the design decisions, and the responsibility for every claim are the author's. |
| 05 | **Affirm the humanity of authorship** | **Met.** No automated system is credited as an author. The repository's *How this work is produced* section records the human direction of the work and leaves the traces of the process in place rather than presenting a tidied surface. |
| 06 | **Put effort into proper attribution** | **Met, with a standing rule.** The project's working posture for new-looking identities is *assume classical, name the transport, keep the landing* — instances on record credit Dirichlet, Kubert, and Kubert–Sinnott. Where satisfactory attribution is not possible the papers say so explicitly (e.g. the honest-novelty status on the class-number corollary), and the negative OEIS search of 2026-08-11 is kept as a dated, reproducible record rather than a claim. |
| 07 | **Participate in public discourse** | **Partial, by circumstance.** The public artefacts (README, homepage, Zenodo description) explain how AI was used and why the verification apparatus exists at this level. No wider outreach is undertaken; nothing here overstates AI capability — the failure ledger records what the process actually got wrong. |
| 08 | **Stay informed** | **Ongoing.** The project tracks the formal-mathematics tooling it depends on (Lean, Mathlib, lean4checker) and the practices of AI-assisted mathematics it borrows or rejects, with reasons recorded. |
| 09 | **Welcome new contributors / respect the field's values** | **Taken in the second direction.** This project enters mathematics from outside an institution; the Declaration asks such entrants to respect the field's values while helping adapt them. The entire apparatus — statuses at statements, kernel replay, logged numbers, the failure ledger — is this project's attempt to meet the field's standards in a checkable form. |
| 10 | **Consider carefully which tools to use** | **Not met, stated plainly.** The models used are commercial, proprietary, and energy-intensive, and no smaller or non-proprietary system currently suffices for this work. This is the one provision the signature comment names as failed. The mitigations — full disclosure, human responsibility, machine-checkable verification, modest compute — do not convert a failed provision into a met one, and this row will be updated if the tool landscape changes. |
| 11 | **Evaluate ethical consequences** | **Met at the scale of the work.** The subject is arithmetic of integer sequences; no application to harm is identified. No external partnerships exist. |

*Last reviewed: 2026-08-15 (round 171). When a practice changes, this file changes in the
same commit — a compliance table that lags its repository is a summary that lies (F35).*
