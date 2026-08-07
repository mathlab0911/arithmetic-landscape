/- 算術地形理論(ALT)正典 第5号 (2026-08-08, opus-5 実務セッション・6周目)
   5周目の持ち越し①: 主張20a(層 = 切断列の表現数)の Lean 化。

   定理21(= 主張20a): I ⊆ [k] と J ⊆ I を固定したとき、
     #{S : σ(S) = n かつ S ∩ I = J} = #{U ⊆ Iᶜ : σ(U) + σ(J) = n} = r_{B}(n − σ(J))
   すなわち「小要素部を J に固定した基底状態の数」は、
   切断列 B = A|_{Iᶜ} による表現数そのものである。
   全単射は S ↦ S \ I(逆写像 U ↦ U ∪ J)。

   これに degCount_fiberwise(4周目/5周目)を合わせると
     deg(n) = Σ_{J ⊆ I_d} r_{B_d}(n − σ(J))
   が出て、定理20(挟み撃ち)の左辺が完全に表現数の言葉になる。 -/
import Pnp.Theory.Decomposition

namespace ALT

section Fiber

variable {k : Nat}

/-- 切断列による表現数 r_B(m) の Finset 版:
    Iᶜ に含まれる配位のうち、J の分を足して n になるものの個数 -/
def repCount (A : Fin k → Nat) (I J : Finset (Fin k)) (n : Nat) : Nat :=
  ((Finset.univ : Finset (Finset (Fin k))).filter
    (fun U => U ⊆ Iᶜ ∧ U.sum A + J.sum A = n)).card

/-- 補助: S を I の内外で分けると和が復元する -/
theorem sum_inter_add_sum_sdiff (A : Fin k → Nat) (S I : Finset (Fin k)) :
    (S ∩ I).sum A + (S \ I).sum A = S.sum A := by
  classical
  have hsub : S ∩ I ⊆ S := Finset.inter_subset_left
  have h2 := Finset.sum_sdiff (f := A) hsub
  rw [Finset.sdiff_inter_self_left] at h2
  rw [Nat.add_comm]
  exact h2

/-- 定理21(主張20a): 層の濃度は切断列の表現数に等しい -/
theorem fiber_card_eq_repCount (A : Fin k → Nat) (n : Nat)
    {I J : Finset (Fin k)} (hJ : J ⊆ I) :
    ((Finset.univ : Finset (Finset (Fin k))).filter
      (fun S => S.sum A = n ∧ S ∩ I = J)).card = repCount A I J n := by
  classical
  unfold repCount
  set F : Finset (Finset (Fin k)) :=
    (Finset.univ : Finset (Finset (Fin k))).filter
      (fun U => U ⊆ Iᶜ ∧ U.sum A + J.sum A = n) with hF
  have hUJ : ∀ U ∈ F, Disjoint U J := by
    intro U hU
    simp only [hF, Finset.mem_filter, Finset.mem_univ, true_and] at hU
    refine Finset.disjoint_left.mpr (fun a haU haJ => ?_)
    have : a ∈ Iᶜ := hU.1 haU
    simp only [Finset.mem_compl] at this
    exact this (hJ haJ)
  have himg : (Finset.univ : Finset (Finset (Fin k))).filter
      (fun S => S.sum A = n ∧ S ∩ I = J) = F.image (fun U => U ∪ J) := by
    ext S
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_image, hF]
    constructor
    · intro ⟨hsum, hint⟩
      refine ⟨S \ I, ⟨?_, ?_⟩, ?_⟩
      · exact fun a ha => by
          simp only [Finset.mem_compl]
          exact (Finset.mem_sdiff.mp ha).2
      · rw [← hint]
        have := sum_inter_add_sum_sdiff A S I
        omega
      · rw [← hint, Finset.sdiff_union_inter]
    · rintro ⟨U, ⟨hsub, hsum⟩, rfl⟩
      have hdisj : Disjoint U J := by
        refine Finset.disjoint_left.mpr (fun a haU haJ => ?_)
        have : a ∈ Iᶜ := hsub haU
        simp only [Finset.mem_compl] at this
        exact this (hJ haJ)
      constructor
      · rw [Finset.sum_union hdisj]; exact hsum
      · ext a
        simp only [Finset.mem_inter, Finset.mem_union]
        constructor
        · rintro ⟨hU | hJa, hI⟩
          · exact absurd hI (by
              have := hsub hU
              simpa using this)
          · exact hJa
        · intro ha
          exact ⟨Or.inr ha, hJ ha⟩
  rw [himg, Finset.card_image_of_injOn]
  intro U1 h1 U2 h2 heq
  have d1 := hUJ U1 h1
  have d2 := hUJ U2 h2
  have e1 : (U1 ∪ J) \ J = U1 := Finset.union_sdiff_cancel_right d1
  have e2 : (U2 ∪ J) \ J = U2 := Finset.union_sdiff_cancel_right d2
  have heq' : U1 ∪ J = U2 ∪ J := heq
  rw [← e1, ← e2, heq']

/-- 定理22(定理20の左辺の完成形): 基底状態数は、小要素部 J を走らせた
    切断列の表現数の総和である。deg(n) = Σ_{J ⊆ I} r_{B}(n − σ(J))。
    定理20(挟み撃ち)はこの右辺の各項に平坦性を当てて得られる。 -/
theorem degCount_eq_sum_repCount (A : Fin k → Nat) (n : Nat) (I : Finset (Fin k)) :
    degCount A n = I.powerset.sum (fun J => repCount A I J n) := by
  rw [degCount_fiberwise A n I]
  exact Finset.sum_congr rfl
    (fun J hJ => fiber_card_eq_repCount A n (Finset.mem_powerset.mp hJ))

end Fiber

/- 数値クロスチェック: A6 = (3,5,7,11,13,17), n = 28, I = {i : a_i ≤ 6} = {3,5}(添字0,1) -/
#eval degCount A6 28
#eval (({0, 1} : Finset (Fin 6)).powerset).sum (fun J => repCount A6 {0, 1} J 28)
#eval (List.range 57).all (fun n =>
  degCount A6 n == (({0, 1} : Finset (Fin 6)).powerset).sum
    (fun J => repCount A6 {0, 1} J n))          -- 期待 true

end ALT

#print axioms ALT.sum_inter_add_sum_sdiff
#print axioms ALT.fiber_card_eq_repCount
#print axioms ALT.degCount_eq_sum_repCount
