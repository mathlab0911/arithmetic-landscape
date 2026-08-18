# The written proof of the decay-rate theorem

**This is the proof behind `\STATUS{proved}` on Theorem `thm:decayrate` of the standalone
note** (*Two speeds at the boundary*, `paper/note1.pdf` and `paper-ja/note1_ja.pdf`), which
states the theorem, gives its mechanism in one paragraph, and points here for the argument.

> **Theorem.** For every fixed `s > 1`, with `w_j = (j+1)^{−s}`, a first zero `t₁(k)` exists
> for all large `k` and `2 k t₁(k)² / log k → s − ½`.
>
> **Status: proved, two routes.** Written out here (r229, repaired r231) and re-derived
> independently along a different route by the second reader, who had not seen this text
> (r228); he then read this document statement by statement against that re-derivation and
> raised the status in r230 §2. The two edits he made mandatory, **R1** (display the window
> justification) and **R2** (give the last asymptotic its error term), are applied below.

**Why it is a Markdown file and not a section of the note.** Because it is the *evidence* for
a status, and in this repository evidence is a named artefact beside the statement that rests
on it — as `abel_r220b` is for Theorem `thm:monotone` and `hstar_r222c` is for the measured
branch. Adding it to the note as an appendix means adding it to *both* editions in the same
round (F60 instance 5: a Japanese edition ships with its source, never after). That is a
separate act and it is scheduled; until it happens, a reader who wants the proof should not
have to ask the author for it (F64).

**How to read it against the note.** Lemma 1 below is `eq:abel` in the note; the sentence in
the note that begins *"The mechanism is visible in"* is Steps 1–5 compressed to a paragraph;
the note's claim that `D_jρ^j` has exactly one interior minimum is Step 2 here.

**Status of every ingredient, stated up front (F38).**

| ingredient | status |
|---|---|
| Lemma 1 (Abel identity) | **proved (two routes)** — r224 hand derivation, r220 60-digit check |
| Lemma 2 (exact unimodality) | **proved** — fable's r228 §1.1, reproduced here in full |
| Lemma 3 (moment identities) | **proved in Lean** — `Pnp/Theory/AbelWeights.lean`, kernel-replayed |
| Lemmas 4–7 | **proved on paper, second reading complete** (fable, r228 §1.2–§1.5) |
| Theorem | what this document is for |

---

## Notation

Fix `s > 1`. For `j ≥ 0` put `w_j = (j+1)^{−s}`, and for `k ≥ 2`

```
    F_k(t) = 1 + 2 Σ_{j=0}^{k−1} w_j ρ^j cos(jθ),      ρ = √(1+4t²),  θ = arctan(2t),
```

which is `F_k(½+it)` for the generating function of the programme. Write `z = 1 + 2it`, so
`|z| = ρ` and `arg z = θ`; write `D_j = w_{j−1} − w_j > 0` for `j ≥ 1`, and `a_j = D_j ρ^j`.
Let `t₁(k)` be the smallest `t > 0` with `F_k(t) = 0`.

> ## Theorem
>
> For every fixed `s > 1`,
> ```
>     2 k t₁(k)² / log k  →  s − ½        as k → ∞.
> ```

Everything below is one proof. The three ranges of `s` appear only in Step 4, as cases in a
single estimate; **no statement in this document is restricted to a sub-range of `s > 1`.**

---

## Step 1 — an exact identity (Lemma 1)

Abel summation with `S_j = Σ_{i≤j} z^i = (z^{j+1}−1)/(z−1)` and `z − 1 = 2it`, using
`Re[(z^m−1)/2it] = ρ^m sin(mθ)/2t`:

```
 (B)   F_k(t) = 1 + (1/t) [ w_{k−1} ρ^k sin(kθ) + H*(t) ],     H*(t) = Σ_{j=1}^{k−1} a_j sin(jθ).
```

Exact for every weight sequence and every `t > 0`. Write `A(t) = k^{−s} ρ^k / t > 0`, so that
`F_k = 1 + H*/t + A sin(kθ)` — one non-oscillating part and one oscillation whose amplitude is
`A`.

## Step 2 — `a_j` has exactly one interior minimum (Lemma 2, exact)

`D_j = ∫_j^{j+1} s x^{−(s+1)} dx`. The integrand is strictly log-convex on `(0,∞)`, since
`(log f)''(x) = (s+1)/x² > 0`. For log-convex `f`, Cauchy–Schwarz gives

```
   D_{(j₁+j₂)/2} = ∫₀¹ f((j₁+j₂)/2 + u) du ≤ ∫₀¹ √(f(j₁+u) f(j₂+u)) du ≤ √(D_{j₁} D_{j₂}),
```

so `D` is log-convex in `j` and `D_{j+1}/D_j` is strictly increasing. Hence
`a_{j+1}/a_j = ρ · D_{j+1}/D_j` is strictly increasing and crosses `1` **at most once**:

> `a_j` is strictly decreasing, then strictly increasing, with a single interior minimum.
> **No asymptotics; true at every `j`.**

This is the only structural fact the tail estimate needs, and it is why the tail is summable
**by cancellation**. Brute force cannot do it: `Σ_j |a_j|` over the tail is `≍ k t^{s+1}`, which
at the working scale `t ≍ √(log k / k)` **diverges for `1 < s < 2`**.

## Step 3 — the two moment identities (Lemma 3, in Lean)

For every real sequence `w` and every `J`, by telescoping:

```
   Σ_{j=1}^{J} j   D_j = Σ_{i<J} w_i        − J   w_J
   Σ_{j=1}^{J} j²  D_j = Σ_{i<J} (2i+1) w_i − J²  w_J
```

`Pnp/Theory/AbelWeights.lean`, replayed through the kernel. They are separated out because an
algebra slip here would sit on **both sides** of every numerical comparison and so be invisible
to all of them (F87).

## Step 4 — the head (Lemmas 4–5), **and the only place `s` splits into cases**

Put `J = ⌈1/(2t)⌉` and `HEAD = Σ_{j≤J} a_j sin(jθ)`. Since `a_j sin(jθ) = D_j Im(z^j)` exactly,

```
   |Im(z^j) − 2jt| ≤ Σ_{m≥2} C(j,m)(2t)^m = (1+2t)^j − 1 − 2jt ≤ (2jt)² e^{2jt}/2,
```

using `(1+x)^j ≤ e^{jx}` and `e^y − 1 − y ≤ y²e^y/2`. On `j ≤ J` we have `2jt ≤ 1 + 2t`, so for
`t ≤ ½` the exponential is at most `e²`, giving

```
 (H1)   | HEAD − 2t Σ_{j≤J} j D_j |  ≤  2 e² t² Σ_{j≤J} j² D_j
 (H2)   | 2 Σ_{j≤J} j D_j − 2ζ(s) |  ≤  2 ( Σ_{i≥J} w_i + J w_J )  ≤  2 J^{1−s} · s/(s−1)
```

— (H2) because Step 3 turns the truncation error into the tail of a convergent series plus
`J w_J ≤ J^{1−s}`.

**The case analysis, and it is confined to bounding one sum.** By Step 3,
`Σ_{j≤J} j² D_j ≤ 2 Σ_{i<J} (i+1)^{1−s}`, and

* `1 < s < 2`:  `≤ 2 J^{2−s}/(2−s)`,  so `(H1)/t ≤ 4e² s' t · J^{2−s} ≍ t^{s−1}`;
* `s = 2`:      `≤ 2(1 + log J)`,      so `(H1)/t ≍ t log(1/t)`;
* `s > 2`:      `≤ 2 ζ(s−1)`,          so `(H1)/t ≍ t`.

In all three, `(H1)/t → 0`; and `(H2) ≍ t^{s−1} → 0`. Hence, with `E(t)` denoting the total,

```
 (E)   HEAD/t = 2ζ(s) + E(t),     |E(t)| ≤ 2e² t Σ_{j≤J} j²D_j + 2 J^{1−s} s/(s−1)  →  0.
```

*Both constants are computable at every finite `k`; nothing here is merely `O(·)`.*
**Note the domain claim is exact:** at `s = 1` the constant `s/(s−1)` is undefined, so the
argument does not fail below the line — **it does not apply.**

## Step 5 — the tail, by Dirichlet on each monotone side (Lemma 6)

Let `j*` be the minimiser from Step 2 and split `(J, k)` at it. On `(J, j*]` the sequence `a_j`
decreases, on `(j*, k)` it increases, and `|Σ_{j=m}^{n} sin(jθ)| ≤ 1/sin(θ/2)`. Abel's
inequality on each side:

```
   |Σ_{(J,j*]}| ≤ a_J / sin(θ/2) =: B₁ ,        |Σ_{(j*,k)}| ≤ 2 a_{k−1} / sin(θ/2) =: B₂ .
```

With `a_J ≍ s(2t)^{s+1}`, `sin(θ/2) ≍ t` and `a_{k−1} ≍ s k^{−(s+1)} ρ^k`:

```
   B₁/t ≲ s 2^{s+1} t^{s−1} → 0 (s > 1) ,      B₂/t ≲ 4 s k^{−1/2} / (λ log k) → 0 .
```

**These are two different rates and are never to be tested as one** (F108). Combining with (E):

```
 (H)   H*/t = 2ζ(s) + O(t^{s−1}) + O(t log(1/t)) + O(k^{−1/2}/log k) .
```

## Step 6 — where the zero is (Lemma 7)

Let `T = T(k,s)` solve `k^{−s} ρ(T)^k = (1 + 2ζ(s)) T`, i.e. `A(T) = 1 + 2ζ(s)`.

**(a) `A` is increasing** where `d log A/dt = 4kt/(1+4t²) − 1/t > 0`, i.e. once `4(k−1)t² > 1` —
true throughout the relevant range, since `4kt² ≍ 2λ log k`.

**(b) `A` is steep.** A relative increase `η` in `t` multiplies `A` by `≈ exp(4kT²η) = k^{2λη}`.
So `η = |E|/(2λ log k)` suffices to absorb a head error `E`. *The robustness of the argument is
the steepness — the same steepness that makes the crossing sharp.*

**(c) The phase sweeps.** `d(kθ)/dt = 2k/(1+4t²)`. Because `arctan` is **concave**, the forward
advance over `[t, t+L]` is *less* than the linearised `2kL/(1+4t²)`; taking

```
   L = 2π (1 + 4t²)/k
```

guarantees a full period. **The one line, displayed, because this is the spot that was
wrong once** (R1, fable r230 §1.2): the advance over `[t, t+L]` is at least
`2kL/(1+4(t+L)²)`, so a full period needs

```
   4π(1+4t²)/(1+4(t+L)²) ≥ 2π   ⟺   1 + 4t² ≥ 8tL + 4L² ,
```

which holds once `tL ≍ √(log k)/k^{3/2} → 0` — true at the working scale, and checked
independently as `m6fix_r226b` N3. Hence there is a point with `sin(kθ) = −1` in the window
for all large `k`. *(The linearised constant `π` is not enough: it fails by a hair, in exactly
the direction concavity predicts. F110.)*

> A document whose selling point is that nothing is waved at must not wave at the one place
> that has already been wrong.

Combining (a)–(c) with (H): for `t ≤ T(1−η)` the amplitude is too small and `F_k > 0` because
`|sin| ≤ 1`; and at the first `t* ≥ T(1+η)` where `sin(kθ) = −1`, `F_k(t*) ≤ 0`. Therefore

```
 (Z)   T(1 − η)  ≤  t₁  ≤  T(1 + η) + 2π(1 + 4T²)/k ,        η = |E| / (2λ log k) .
```

## Step 7 — the conclusion

First, the last asymptotic in the document is given its error explicitly (R2, fable r230
§1.3), so that no `o(1)` survives in a display: `log ρ^k = 2kt² − 4kt⁴(1+O(t²))` and
`kt⁴ ≍ λ² log²k/4k`, hence

```
   ρ^k = k^{λ} · exp( O( log²k / k ) ) .
```

Taking logs in `k^{−s}ρ(T)^k = (1+2ζ(s))T` with that form and `T = √(λ log k/2k)`:

```
   (λ − s) log k = log(1+2ζ(s)) + ½ log λ + ½ log log k − ½ log 2 − ½ log k + o(1),
```

so `λ_T := 2kT²/log k = s − ½ + (log log k)/(2 log k) + O(1/log k) → s − ½`. In (Z), `η → 0` by
(E), and `2π(1+4T²)/(kT) ≍ 1/√(k log k) → 0`; hence `t₁/T → 1` and

```
   2 k t₁²/log k = λ_T (1 + o(1))²  →  s − ½ .    ∎
```

---

## What a referee should attack, in order

1. **Step 2's Cauchy–Schwarz line.** It carries the whole tail estimate. It is fable's and
   mine now, so it has had two readings — but it is the load-bearing novelty.
2. **Step 6(c).** The one place a constant was wrong once already (F110). The claim is now
   stated with the concavity in the right direction; check the direction, not the constant.
3. ~~**Step 7's `ρ^k = k^λ(1+o(1))`.**~~ **CLOSED at r231** — I flagged it, fable ruled it
   safe and specified the explicit form, and Step 7 now displays `ρ^k = k^λ·exp(O(log²k/k))`.
   Recorded as closed rather than deleted, because a reader who cannot see what was open
   cannot audit what is left (F35).

## Numerical support already on file

`prove_r225.log` (K1 24/24 worst 0.2218; K3 the derived bound covers the measured error 24/24
worst 0.8307; K4 bracket 24/24; K5 rate stable 1.03–1.11), `debts_r226.log` (M1 worst 0.0160,
M2 worst 0.9820, M3 worst 0.3136, M5 smallest `4(k−1)t² = 19.91`, M7 bracket 24/24 with `t₁` at
position 0.40–0.58), `m6fix_r226b.log` (the corrected window, N1 failing 12/12 as predicted).

**Two registered criteria remain filed as FAILs and are not repaired here** (r228's standing
policy): K2/K6 from r225 and M6 from r226. None of them is load-bearing for the theorem; all
three are recorded with their diagnoses.
