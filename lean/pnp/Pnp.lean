-- This module serves as the root of the `Pnp` library.
-- Import modules here that should be built as part of the library.
import Pnp.Basic
import Pnp.Theory.Landscape
import Pnp.Theory.Symmetry
import Pnp.Theory.Bridge
import Pnp.Theory.Decomposition
import Pnp.Theory.Fiber
import Pnp.Theory.Sandwich
import Pnp.Theory.Total
import Pnp.Theory.Ripple
import Pnp.Theory.TermwiseMin
import Pnp.Theory.ModFour
import Pnp.Theory.OddPeaks
import Pnp.Theory.OddProd
import Pnp.Theory.CosetProd
-- r117: Cyclotomic had been in Pnp/Theory, recorded as canon, and imported by nothing --
-- so lake never built it and lean4checker never replayed it.  tools/check_lean.ps1 now
-- fails (exit 4) if any Pnp/Theory file is outside this closure.
import Pnp.Theory.Cyclotomic
-- r120: 極値定理(Γ の値域と両端の一意性・狭義単調性)。
-- 論文1 §極値値 が引用する。
import Pnp.Theory.Extremal
