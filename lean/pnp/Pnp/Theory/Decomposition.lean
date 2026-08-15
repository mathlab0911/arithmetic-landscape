/- 算術地形理論(ALT)正典 第4号 (2026-08-07, 5周目)
   定理19: lm の厳密分解(層別定理)。
   分類定理(定理5〜7)を「和の値 s」で層別すると、各層で局所最小条件が
   「a_i > 2d(d = |s−n|)」という制限付き表現条件に退化する。
   これにより lm/deg → W(定理18で W = Γ)の証明は「独立近似の正当化」から
   「表現数関数 r の中央窓での平坦性」という古典解析の問題に厳密に帰着する。 -/
import Pnp.Theory.Landscape

namespace ALT

section Decomposition

variable {k : Nat}

/-- 過剰側 d-層: 和が n+d で、選んだ全要素が 2d を超える配位の数。
    (= 切断列 A_{>2d} による n+d の表現数) -/
def overCount (A : Fin k → Nat) (n d : Nat) : Nat :=
  ((Finset.univ : Finset (Finset (Fin k))).filter
    (fun S => S.sum A = n + d ∧ ∀ i ∈ S, 2 * d < A i)).card

/-- 不足側 d-層: 和 + d = n で、選ばなかった全要素が 2d を超える配位の数。
    (= I_d = {a_i ≤ 2d} を全部含む配位 = A_{>2d} による n−d−σ_d の表現数) -/
def underCount (A : Fin k → Nat) (n d : Nat) : Nat :=
  ((Finset.univ : Finset (Finset (Fin k))).filter
    (fun S => S.sum A + d = n ∧ ∀ i ∉ S, 2 * d < A i)).card

/-- 基底状態数(実験の deg 列の正典定義) -/
def degCount (A : Fin k → Nat) (n : Nat) : Nat :=
  ((Finset.univ : Finset (Finset (Fin k))).filter (fun S => S.sum A = n)).card

/-- 層補題(過剰側): 和 s ≥ n の局所最小層は overCount に一致 -/
theorem fiber_over {A : Fin k → Nat} (hA : ∀ i, 0 < A i) {n s : Nat} (hs : n ≤ s) :
    ((Finset.univ : Finset (Finset (Fin k))).filter
      (fun S => IsStrictLocalMin A n S ∧ S.sum A = s)).card = overCount A n (s - n) := by
  unfold overCount
  congr 1
  apply Finset.filter_congr
  intro S _
  constructor
  · rintro ⟨hmin, hsum⟩
    have hns : n ≤ S.sum A := by omega
    have hcond := (isStrictLocalMin_iff_of_ge hA hns).mp hmin
    refine ⟨by omega, fun i hi => ?_⟩
    have := hcond i hi
    omega
  · rintro ⟨hsum, hcond⟩
    have hns : n ≤ S.sum A := by omega
    refine ⟨(isStrictLocalMin_iff_of_ge hA hns).mpr (fun i hi => ?_), by omega⟩
    have := hcond i hi
    omega

/-- 層補題(不足側): 和 s < n の局所最小層は underCount に一致 -/
theorem fiber_under {A : Fin k → Nat} (hA : ∀ i, 0 < A i) {n s : Nat} (hs : s < n) :
    ((Finset.univ : Finset (Finset (Fin k))).filter
      (fun S => IsStrictLocalMin A n S ∧ S.sum A = s)).card = underCount A n (n - s) := by
  unfold underCount
  congr 1
  apply Finset.filter_congr
  intro S _
  constructor
  · rintro ⟨hmin, hsum⟩
    have hns : S.sum A ≤ n := by omega
    have hcond := (isStrictLocalMin_iff_of_le hA hns).mp hmin
    refine ⟨by omega, fun i hi => ?_⟩
    have := hcond i hi
    omega
  · rintro ⟨hsum, hcond⟩
    have hns : S.sum A ≤ n := by omega
    refine ⟨(isStrictLocalMin_iff_of_le hA hns).mpr (fun i hi => ?_), by omega⟩
    have := hcond i hi
    omega

/-- 定理19(厳密分解・和インデックス形): lm は和の値 s ごとの層別数え上げの総和。
    独立近似を一切含まない恒等式。 -/
theorem lm_eq_sum_strata (A : Fin k → Nat) (hA : ∀ i, 0 < A i) (n : Nat) :
    lm A n = (Finset.range (Finset.univ.sum A + 1)).sum
      (fun s => if n ≤ s then overCount A n (s - n) else underCount A n (n - s)) := by
  unfold lm
  have H : ∀ S ∈ (Finset.univ : Finset (Finset (Fin k))).filter
      (fun S => IsStrictLocalMin A n S),
      S.sum A ∈ Finset.range (Finset.univ.sum A + 1) := by
    intro S _
    simp only [Finset.mem_range]
    have h : S.sum A ≤ Finset.univ.sum A :=
      Finset.sum_le_sum_of_subset (Finset.subset_univ S)
    omega
  rw [Finset.card_eq_sum_card_fiberwise H]
  apply Finset.sum_congr rfl
  intro s _
  rw [Finset.filter_filter]
  by_cases hns : n ≤ s
  · rw [if_pos hns]
    exact fiber_over hA hns
  · rw [if_neg hns]
    exact fiber_under hA (by omega)

/-- 消滅補題(過剰側): 全要素が 2d 以下なら過剰側 d-層は空(d ≥ 1, n+d > 0) -/
theorem overCount_eq_zero (A : Fin k → Nat) {n d : Nat}
    (hbig : ∀ i, A i ≤ 2 * d) (hpos : 0 < n + d) : overCount A n d = 0 := by
  unfold overCount
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro S _
  rintro ⟨hsum, hcond⟩
  rcases Finset.eq_empty_or_nonempty S with rfl | ⟨i, hi⟩
  · rw [Finset.sum_empty] at hsum
    omega
  · have h1 := hcond i hi
    have h2 := hbig i
    omega

/-- 消滅補題(不足側): 全要素が 2d 以下なら不足側 d-層は空(d ≥ 1, n ≤ 総和) -/
theorem underCount_eq_zero (A : Fin k → Nat) {n d : Nat}
    (hbig : ∀ i, A i ≤ 2 * d) (hd : 0 < d) (hn : n ≤ Finset.univ.sum A) :
    underCount A n d = 0 := by
  unfold underCount
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro S _
  rintro ⟨hsum, hcond⟩
  have hSuniv : S = Finset.univ := by
    apply Finset.eq_univ_iff_forall.mpr
    intro i
    by_contra hi
    have h1 := hcond i hi
    have h2 := hbig i
    omega
  subst hSuniv
  omega

/-- d=0 の過剰側層は基底状態の全体(要素が全て正のとき) -/
theorem overCount_zero_eq_degCount {A : Fin k → Nat} (hA : ∀ i, 0 < A i) (n : Nat) :
    overCount A n 0 = degCount A n := by
  unfold overCount degCount
  congr 1
  apply Finset.filter_congr
  intro S _
  constructor
  · rintro ⟨hsum, _⟩
    omega
  · intro hsum
    exact ⟨by omega, fun i _ => by have := hA i; omega⟩

/-- 畳み込み(定理20の素材): 基底状態は「I との交わり」で層別される。
    I = I_d = {i : a_i ≤ 2d} と取れば deg(n) = Σ_{J ⊆ I_d} (J を小要素部として持つ
    基底状態の数) = Σ_J r_{A_{>2d}}(n − σ(J))。 -/
theorem degCount_fiberwise (A : Fin k → Nat) (n : Nat) (I : Finset (Fin k)) :
    degCount A n = I.powerset.sum (fun J =>
      ((Finset.univ : Finset (Finset (Fin k))).filter
        (fun S => S.sum A = n ∧ S ∩ I = J)).card) := by
  unfold degCount
  have H : ∀ S ∈ (Finset.univ : Finset (Finset (Fin k))).filter
      (fun S => S.sum A = n), S ∩ I ∈ I.powerset := by
    intro S _
    exact Finset.mem_powerset.mpr Finset.inter_subset_right
  rw [Finset.card_eq_sum_card_fiberwise H]
  apply Finset.sum_congr rfl
  intro J _
  rw [Finset.filter_filter]

/- ---- 数値クロスチェック(定理19は証明済みだが、定義の健全性を #eval でも確認) ---- -/

-- A6 = (3,5,7,11,13,17), T = 56。定理19の左右一致を全 n ≤ 56 で確認
#eval (List.range 57).all (fun n =>
  lm A6 n == (Finset.range 57).sum
    (fun s => if n ≤ s then overCount A6 n (s - n) else underCount A6 n (n - s)))
-- 期待 true

#eval [lm A6 28, degCount A6 28, overCount A6 28 0]  -- deg = overCount d=0 の実例
#eval overCount A6 28 9  -- 2d=18 > 17 = 最大要素 → 消滅補題どおり 0 のはず
#eval underCount A6 28 9 -- 同上 0

/- ============ 定理20(挟み撃ち)の設計(fable-5, 5周目)— opus-5 への引継ぎ ============
   記号: A: k項の増加奇数列, T = ΣA, 中央目標 n(〜T/2), D = (a_k−1)/2,
   I_d = {i : a_i ≤ 2d}, N(d) = |I_d|, σ_d = Σ_{i∈I_d} a_i,
   B_d = A_{>2d}(切断列), r_B(m) = B による m の部分和表現数。
   窓 Win_d = [n − σ_d − d, n + d](幅 σ_d + 2d)。

   【主張20a(全単射)】 card{S : S.sum = n ∧ S ∩ I_d = J} = r_{B_d}(n − σ(J))
     (写像 S ↦ S \ I_d。degCount_fiberwise と合わせて
      deg(n) = Σ_{J ⊆ I_d} r_{B_d}(n − σ(J)) が従う)
     同様に overCount A n d = r_{B_d}(n+d)、underCount A n d = r_{B_d}(n−d−σ_d)。

   【主張20b(挟み撃ち・有限不等式)】 d* ≤ D と ε > 0 について
   仮定(平坦性): ∀ d ≤ d*, ∀ m, m' ∈ Win_d: r_{B_d}(m') ≤ (1+ε) · r_{B_d}(m)
   仮定(裾): ∀ d ∈ (d*, D]: max_m r_{B_d}(m) ≤ C · 2^{−N(d)} · deg(n)
   結論: (1+ε)^{−2} · W_{d*} − TailC ≤ lm/deg ≤ (1+ε)^2 · W_{d*} + TailC,
     TailC = 2C · (W_D − W_{d*})(W は定理18の窓級数; W_D = Γ + a_k/2^k)。
   導出の要点: 各 d ≤ d* で deg = Σ_{J⊆I_d} r_{B_d}(n−σ(J)) の 2^{N(d)} 個の項が
   すべて r_{B_d}(n+d) の (1±ε) 倍 ⟹ overCount/deg ∈ (1±ε)^{±2}·2^{−N(d)}。
   これは ℚ 上の有限不等式であり、具体的な k ではすべての量が計算可能
   (= 個別インスタンスの認証付き誤差評価が Lean でできる)。

   【漸近戦略(論文2)】 残る解析的仮定は平坦性 ε_k → 0 のみ:
   - ランダム奇数列: 局所CLT / Erdős–Littlewood–Offord 型の反集中で証明可能な射程
   - 素数列: 相異なる素数の和への分割数の漸近(Roth–Szekeres 1954 系。要文献確認)
     ないし Vinogradov 型指数和で切断素数列の r の平坦性を直接評価
   - 裾仮定は max_m r_{B_d}(m) ≤ C·2^{|B_d|}/(スケール) 型の反集中上界(Erdős 1945)
     + deg の下界(これも平坦性側の副産物)から。
   平坦性は各 k で厳密に計算可能なので、まず実測(flatness_r5.py)で
   ε_k の減衰を確認してから漸近証明に投資する。 -/

end Decomposition

end ALT

#print axioms ALT.fiber_over
#print axioms ALT.fiber_under
#print axioms ALT.lm_eq_sum_strata
#print axioms ALT.overCount_eq_zero
#print axioms ALT.underCount_eq_zero
#print axioms ALT.overCount_zero_eq_degCount
#print axioms ALT.degCount_fiberwise
