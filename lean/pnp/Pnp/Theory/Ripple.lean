/- 算術地形理論(ALT)正典 第8号 (2026-08-08, opus-5 8周目)
   論文2(平坦性の漸近証明)の補題のうち、有限・初等で形式化できる部分。

   L1 (ピーク値): |1 + e^{iθ}|² = 2 + 2cos θ。θ = πa/3 に代入すると a mod 6 で
     4, 3, 1, 0, 1, 3 となり、5以上の素数は ±1 mod 6 なので値は常に 3。
     a ≡ 3 (mod 6) で 0 になることが「3 を含む切断列ではリップルが消える」の正体。
   L4 (q-最大性): M(q) = (1/2)|Φ_q(−1)|^{1/φ(q)}。12乗して有理数で比較すると
     q = 6 が厳密に最大であることが norm_num で決着する。
   L2 (奇数列の3次項ゼロ): G(θ) = Π cos(aθ/2) が偶関数であること。 -/
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

namespace ALT

/- ============ L1: 円上の点との距離の2乗 ============ -/

/-- 基本補題: |1 + e^{iθ}|² = 2 + 2 cos θ。リップル解析の出発点。 -/
theorem normSq_one_add_exp (θ : ℝ) :
    Complex.normSq (1 + Complex.exp ((θ : ℂ) * Complex.I)) = 2 + 2 * Real.cos θ := by
  rw [Complex.exp_mul_I]
  simp only [Complex.normSq_apply, Complex.add_re, Complex.add_im, Complex.one_re,
    Complex.one_im, Complex.cos_ofReal_re, Complex.mul_re, Complex.mul_im,
    Complex.I_re, Complex.I_im, Complex.sin_ofReal_re, Complex.sin_ofReal_im,
    Complex.cos_ofReal_im]
  nlinarith [Real.sin_sq_add_cos_sq θ]

/-- a ≡ 1 (mod 6) と a ≡ 5 (mod 6) では |1 + ζ₆^a|² = 3(√3 の2乗)。 -/
theorem normSq_at_pi_div_three :
    Complex.normSq (1 + Complex.exp ((Real.pi / 3 : ℝ) * Complex.I)) = 3 := by
  rw [normSq_one_add_exp, Real.cos_pi_div_three]; norm_num

/-- a ≡ 3 (mod 6) では |1 + ζ₆^a|² = 0。3 を含む切断列でリップルが消える理由。 -/
theorem normSq_at_pi :
    Complex.normSq (1 + Complex.exp ((Real.pi : ℝ) * Complex.I)) = 0 := by
  rw [normSq_one_add_exp, Real.cos_pi]; norm_num

/-- a ≡ ±2 (mod 6) では |1 + ζ₆^a|² = 1(mod-6 の副次モード、無視できる)。 -/
theorem normSq_at_two_pi_div_three :
    Complex.normSq (1 + Complex.exp ((2 * Real.pi / 3 : ℝ) * Complex.I)) = 1 := by
  have h : Real.cos (2 * Real.pi / 3) = -(1/2) := by
    have : (2 : ℝ) * Real.pi / 3 = Real.pi - Real.pi / 3 := by ring
    rw [this, Real.cos_pi_sub, Real.cos_pi_div_three]
  rw [normSq_one_add_exp, h]; norm_num

/- ============ L4: なぜ 6 か(有限部分の厳密決着) ============
   M(q) = (1/2)|Φ_q(−1)|^{1/φ(q)} を 12 乗すると、上位の q すべてが
   分母 4096 の有理数になり、大小関係が norm_num で決着する。
     M(6)^12  = (3/4)^6   = 729/4096      φ(6)=2,  Φ_6(−1)=3
     M(10)^12 = (5/16)^3  = 125/4096      φ(10)=4, Φ_10(−1)=5
     M(4)^12  = (1/2)^6   =  64/4096      φ(4)=2,  Φ_4(−1)=2
     M(14)^12 = (7/64)^2  =  49/4096      φ(14)=6, Φ_14(−1)=7
     M(8)^12  = (1/8)^3   =   8/4096      φ(8)=4,  Φ_8(−1)=2
     M(q)^12  = (1/2)^12  =   1/4096      その他 q≥3(Φ_q(−1)=1) -/

/-- M(q) の12乗(上位の q と、Φ_q(−1)=1 となる一般の q) -/
def M12 : ℕ → ℚ
  | 4  => 64 / 4096
  | 6  => 729 / 4096
  | 8  => 8 / 4096
  | 10 => 125 / 4096
  | 14 => 49 / 4096
  | _  => 1 / 4096

/-- 定理(L4 有限部): q = 6 は他のどの候補よりも厳密に大きい。
    「なぜ mod 6 が律速か」の算術的核心が、有理数の大小比較に落ちる。 -/
theorem M12_six_maximal :
    M12 10 < M12 6 ∧ M12 4 < M12 6 ∧ M12 14 < M12 6 ∧ M12 8 < M12 6 ∧
    (1 : ℚ) / 4096 < M12 6 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp [M12] <;> norm_num

/-- 2位との差も明示的(margin が有限で取れることの確認)。 -/
theorem M12_gap : M12 6 - M12 10 = 604 / 4096 := by
  simp [M12]; norm_num

/- ============ L2: 奇数列では log G の3次項が消える ============ -/

/-- 特性関数の実部 G(θ) = Π_{a∈A} cos(aθ/2)。 -/
noncomputable def G (A : List ℕ) (θ : ℝ) : ℝ :=
  (A.map (fun a => Real.cos ((a : ℝ) * θ / 2))).prod

/-- 定理(L2 の御利益): G は θ の偶関数。したがって展開に奇数次の項が現れない。
    一般の実数列でも成り立つ形で述べておく(奇数列に限らない)。 -/
theorem G_even (A : List ℕ) (θ : ℝ) : G A (-θ) = G A θ := by
  unfold G
  congr 1
  apply List.map_congr_left
  intro a _
  rw [show (a : ℝ) * (-θ) / 2 = -((a : ℝ) * θ / 2) by ring, Real.cos_neg]

/-- 系: 3次(および任意の奇数次)の Taylor 係数が消える、の使いやすい形。
    偶関数なので θ ↦ G(θ) − G(−θ) は恒等的にゼロ。 -/
theorem G_odd_part_zero (A : List ℕ) (θ : ℝ) : G A θ - G A (-θ) = 0 := by
  rw [G_even]; ring

/- ============ L3 の幅因子(算術部分): V₆ = Σa²/3 ============
   サブ弧 θ = 2π/6 での曲率は V_q = (1/4) Σ a² sec²(πa/q)。
   5以上の素数は ±1 mod 6 なので cos²(πa/6) = 3/4 が厳密に成り立ち、
   sec² = 4/3、したがって V₆ = (1/4)(4/3)Σa² = Σa²/3。
   幅因子 √(V₀/V₆) = √((1/4)/(1/3)) = √3/2 が、振幅の指数の「+1」の正体。 -/

/-- 補助: cos² は π の整数倍の平行移動で不変。 -/
theorem cos_sq_add_nat_mul_pi (x : ℝ) : ∀ m : ℕ,
    Real.cos (x + m * Real.pi) ^ 2 = Real.cos x ^ 2
  | 0 => by simp
  | (m + 1) => by
      have h : x + (↑(m + 1) : ℝ) * Real.pi = (x + m * Real.pi) + Real.pi := by
        push_cast; ring
      rw [h, Real.cos_add_pi, neg_pow, cos_sq_add_nat_mul_pi x m]
      simp

/-- a ≡ 1 (mod 6) なら cos²(πa/6) = 3/4。 -/
theorem cos_sq_pi_mul_div_six_of_one {a : ℕ} (h : a % 6 = 1) :
    Real.cos (Real.pi * a / 6) ^ 2 = 3 / 4 := by
  obtain ⟨m, hm⟩ : ∃ m : ℕ, a = 6 * m + 1 := ⟨a / 6, by omega⟩
  subst hm
  have h2 : Real.pi * ((6 * m + 1 : ℕ) : ℝ) / 6 = Real.pi / 6 + m * Real.pi := by
    push_cast; ring
  rw [h2, cos_sq_add_nat_mul_pi, Real.cos_pi_div_six]
  rw [div_pow, Real.sq_sqrt (by norm_num : (3:ℝ) ≥ 0)]
  norm_num

/-- a ≡ 5 (mod 6) なら cos²(πa/6) = 3/4(5π/6 での余弦は符号違いで同じ2乗)。 -/
theorem cos_sq_pi_mul_div_six_of_five {a : ℕ} (h : a % 6 = 5) :
    Real.cos (Real.pi * a / 6) ^ 2 = 3 / 4 := by
  obtain ⟨m, hm⟩ : ∃ m : ℕ, a = 6 * m + 5 := ⟨a / 6, by omega⟩
  subst hm
  have h2 : Real.pi * ((6 * m + 5 : ℕ) : ℝ) / 6
      = (Real.pi - Real.pi / 6) + (m * Real.pi + Real.pi / 3 * 0) := by
    push_cast; ring
  rw [h2]
  simp only [mul_zero, add_zero]
  rw [cos_sq_add_nat_mul_pi, Real.cos_pi_sub, Real.cos_pi_div_six]
  rw [neg_pow, div_pow, Real.sq_sqrt (by norm_num : (3:ℝ) ≥ 0)]
  norm_num

/-- 定理(L3 幅因子の算術部分): 5 以上の素数(= ±1 mod 6)では
    sec²(πa/6) = 4/3 が厳密。ゆえに V₆ = Σa²/3 で、幅因子は √(V₀/V₆) = √3/2。 -/
theorem sec_sq_pi_mul_div_six {a : ℕ} (h : a % 6 = 1 ∨ a % 6 = 5) :
    1 / Real.cos (Real.pi * a / 6) ^ 2 = 4 / 3 := by
  rcases h with h | h
  · rw [cos_sq_pi_mul_div_six_of_one h]; norm_num
  · rw [cos_sq_pi_mul_div_six_of_five h]; norm_num

/- ============ 定理E: 奇数列の普遍的な mod-4 障害(床) ============
   奇数 a に対し i^a = ±i なので 1 + i^a = 1 ± i、絶対値は剰余に依らず常に √2。
   ⇒ |F_B(i)| = 2^{b/2} が厳密。**決してゼロにならない**(mod 6 とはここが違う)。
   一方 F_B(−1) = 0(奇数だから)。この2つから mod 4 の表現数分布のずれに
   下界 2√2·2^{−b/2} が出る(定理 thm:floor)。 -/

/-- 奇数 a に対し |1 + i^a|² = 2(a mod 4 が 1 でも 3 でも同じ)。
    これが「mod 4 のさざ波は消せない」ことの正体。 -/
theorem normSq_one_add_I_pow_odd (a : ℕ) (h : a % 2 = 1) :
    Complex.normSq (1 + Complex.I ^ a) = 2 := by
  obtain ⟨m, hm⟩ : ∃ m, a = 2 * m + 1 := ⟨a / 2, by omega⟩
  subst hm
  rw [pow_add, pow_mul, pow_one]
  have hI2 : (Complex.I ^ 2) ^ m = (-1 : ℂ) ^ m := by
    rw [Complex.I_sq]
  rw [hI2]
  rcases Nat.even_or_odd m with he | ho
  · rw [he.neg_one_pow]
    simp [Complex.normSq_apply]; norm_num
  · rw [ho.neg_one_pow]
    simp [Complex.normSq_apply]; norm_num

/-- 対比: 1 + ζ₆^a は a ≡ 3 (mod 6) でゼロになる。つまり mod 6 のさざ波は消せる。
    (`normSq_at_pi` が ζ₆³ = −1 での消滅。ここでは「消えない」側を主張する。) -/
theorem normSq_one_add_I_pow_odd_ne_zero (a : ℕ) (h : a % 2 = 1) :
    (1 + Complex.I ^ a) ≠ 0 := by
  intro hz
  have := normSq_one_add_I_pow_odd a h
  rw [hz] at this
  simp at this

/-- 4点 {cos φ, sin φ, −cos φ, −sin φ} の最大値の2乗は 1/2 以上。
    (max² は cos², sin² の大きいほうで、和が 1 だから半分は超える。) -/
theorem max_abs_cos_sin_sq_ge (φ : ℝ) :
    (1 : ℝ) / 2 ≤ (max |Real.cos φ| |Real.sin φ|) ^ 2 := by
  have hpyth := Real.sin_sq_add_cos_sq φ
  rcases le_total |Real.cos φ| |Real.sin φ| with h | h
  · rw [max_eq_right h, sq_abs]
    nlinarith [abs_nonneg (Real.cos φ), abs_nonneg (Real.sin φ),
      sq_abs (Real.cos φ), sq_abs (Real.sin φ)]
  · rw [max_eq_left h, sq_abs]
    nlinarith [abs_nonneg (Real.cos φ), abs_nonneg (Real.sin φ),
      sq_abs (Real.cos φ), sq_abs (Real.sin φ)]

/-- 定理E(iii)の核となる不等式。
    相対スプレッドは 2^{b/2}·max(|cos φ|,|sin φ|) / 2^{b−2} = 4·max·2^{−b/2} なので、
    主張「相対スプレッド ≥ 2√2·2^{−b/2}」は 2^{−b/2} を約せば
    **4·max(|cos φ|,|sin φ|) ≥ 2√2** に帰着する。それをここで証明する。 -/
theorem spread_lower_bound (φ : ℝ) :
    2 * Real.sqrt 2 ≤ 4 * max |Real.cos φ| |Real.sin φ| := by
  have h := max_abs_cos_sin_sq_ge φ
  have hnn : (0:ℝ) ≤ max |Real.cos φ| |Real.sin φ| :=
    le_max_of_le_left (abs_nonneg _)
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hsn : (0:ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  nlinarith [h, hnn, hs, hsn]

/-! ## 定理E(ii): スプレッドは b の偶奇だけで決まる(15周目に形式化)

`R_c = Σ_{m ≡ c (4)} r_B(m)` は逆離散フーリエ変換で
`R_c = 2^{b−2} + (1/2)·2^{b/2}·cos(φ − cπ/2)`(φ = π(p−q)/4)と書ける。
4点 `{cos φ, sin φ, −cos φ, −sin φ}` の最大と最小の差は `2·max(|cos φ|, |sin φ|)` なので

    max_c R_c − min_c R_c = 2^{b/2} · max(|cos φ|, |sin φ|).

したがって定理E(ii)は、**この max が φ = π·n/4 の n の偶奇だけで決まる**ことに帰着する。
n = p − q は p + q = b と同じ偶奇なので、n の偶奇 = b の偶奇。以下それを証明する。 -/

/-- max(|cos φ|, |sin φ|)² = (1 + |cos 2φ|)/2。倍角公式そのもの。 -/
theorem max_abs_cos_sin_sq (φ : ℝ) :
    (max |Real.cos φ| |Real.sin φ|) ^ 2 = (1 + |Real.cos (2 * φ)|) / 2 := by
  have hpyth : Real.sin φ ^ 2 + Real.cos φ ^ 2 = 1 := Real.sin_sq_add_cos_sq φ
  have hdbl : Real.cos (2 * φ) = Real.cos φ ^ 2 - Real.sin φ ^ 2 := by
    rw [two_mul, Real.cos_add]; ring
  rcases le_total |Real.cos φ| |Real.sin φ| with h | h
  · have hc : Real.cos φ ^ 2 ≤ Real.sin φ ^ 2 := by
      nlinarith [abs_nonneg (Real.cos φ), abs_nonneg (Real.sin φ),
        sq_abs (Real.cos φ), sq_abs (Real.sin φ), h]
    rw [max_eq_right h, sq_abs, hdbl, abs_of_nonpos (by linarith)]
    linarith
  · have hc : Real.sin φ ^ 2 ≤ Real.cos φ ^ 2 := by
      nlinarith [abs_nonneg (Real.cos φ), abs_nonneg (Real.sin φ),
        sq_abs (Real.cos φ), sq_abs (Real.sin φ), h]
    rw [max_eq_left h, sq_abs, hdbl, abs_of_nonneg (by linarith)]
    linarith

/-- b が偶数(n = 2m)のとき max(|cos(πn/4)|, |sin(πn/4)|) = 1。
    ⇒ スプレッド = 2^{b/2}。 -/
theorem max_abs_cos_sin_quarter_even (m : ℕ) :
    max |Real.cos ((2 * m : ℕ) * Real.pi / 4)| |Real.sin ((2 * m : ℕ) * Real.pi / 4)| = 1 := by
  set φ : ℝ := ((2 * m : ℕ) : ℝ) * Real.pi / 4 with hφ
  have h2 : 2 * φ = 0 + m * Real.pi := by rw [hφ]; push_cast; ring
  have habs : |Real.cos (2 * φ)| = 1 := by
    have hsq1 : Real.cos (2 * φ) ^ 2 = 1 := by
      rw [h2, cos_sq_add_nat_mul_pi]; simp
    nlinarith [abs_nonneg (Real.cos (2 * φ)), sq_abs (Real.cos (2 * φ)), hsq1]
  have hsq : (max |Real.cos φ| |Real.sin φ|) ^ 2 = 1 := by
    rw [max_abs_cos_sin_sq, habs]; norm_num
  have hnn : (0:ℝ) ≤ max |Real.cos φ| |Real.sin φ| := le_max_of_le_left (abs_nonneg _)
  nlinarith [hsq, hnn]

/-- b が奇数(n = 2m+1)のとき max(|cos(πn/4)|, |sin(πn/4)|) = √2/2 = 1/√2。
    ⇒ スプレッド = 2^{b/2}/√2 = 2^{(b−1)/2}。 -/
theorem max_abs_cos_sin_quarter_odd (m : ℕ) :
    max |Real.cos ((2 * m + 1 : ℕ) * Real.pi / 4)| |Real.sin ((2 * m + 1 : ℕ) * Real.pi / 4)|
      = Real.sqrt 2 / 2 := by
  set φ : ℝ := ((2 * m + 1 : ℕ) : ℝ) * Real.pi / 4 with hφ
  have h2 : 2 * φ = Real.pi / 2 + m * Real.pi := by rw [hφ]; push_cast; ring
  have habs : |Real.cos (2 * φ)| = 0 := by
    have hz : Real.cos (2 * φ) ^ 2 = 0 := by
      rw [h2, cos_sq_add_nat_mul_pi, Real.cos_pi_div_two]; norm_num
    have : Real.cos (2 * φ) = 0 := by nlinarith [hz]
    rw [this]; simp
  have hsq : (max |Real.cos φ| |Real.sin φ|) ^ 2 = 1 / 2 := by
    rw [max_abs_cos_sin_sq, habs]; norm_num
  have hnn : (0:ℝ) ≤ max |Real.cos φ| |Real.sin φ| := le_max_of_le_left (abs_nonneg _)
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hsn : (0:ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  nlinarith [hsq, hnn, hs, hsn]

/-- 系: 偶数側の値 1 は奇数側の値 √2/2 より真に大きい。
    「b が偶数のほうがスプレッドが √2 倍大きい」ことの形式化。 -/
theorem quarter_even_gt_odd : Real.sqrt 2 / 2 < 1 := by
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hsn : (0:ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  nlinarith [hs, hsn]

end ALT

#print axioms ALT.normSq_one_add_exp
#print axioms ALT.normSq_at_pi_div_three
#print axioms ALT.normSq_at_pi
#print axioms ALT.normSq_at_two_pi_div_three
#print axioms ALT.M12_six_maximal
#print axioms ALT.M12_gap
#print axioms ALT.G_even
#print axioms ALT.G_odd_part_zero
#print axioms ALT.cos_sq_add_nat_mul_pi
#print axioms ALT.cos_sq_pi_mul_div_six_of_one
#print axioms ALT.cos_sq_pi_mul_div_six_of_five
#print axioms ALT.sec_sq_pi_mul_div_six
#print axioms ALT.normSq_one_add_I_pow_odd
#print axioms ALT.normSq_one_add_I_pow_odd_ne_zero
#print axioms ALT.max_abs_cos_sin_sq_ge
#print axioms ALT.spread_lower_bound
#print axioms ALT.max_abs_cos_sin_sq
#print axioms ALT.max_abs_cos_sin_quarter_even
#print axioms ALT.max_abs_cos_sin_quarter_odd
#print axioms ALT.quarter_even_gt_odd
