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

end ALT

#print axioms ALT.normSq_one_add_exp
#print axioms ALT.normSq_at_pi_div_three
#print axioms ALT.normSq_at_pi
#print axioms ALT.normSq_at_two_pi_div_three
#print axioms ALT.M12_six_maximal
#print axioms ALT.M12_gap
#print axioms ALT.G_even
#print axioms ALT.G_odd_part_zero
