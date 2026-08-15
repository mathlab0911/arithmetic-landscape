/-
  OrEvasive_e1b.lean — P≠NP研究: 下界証明の形式化・第1号
  =========================================================
  テーマ: 決定木計算量 (query complexity) における OR_n の厳密な下界

  背景:
    P≠NP の核心的困難は「計算量の下界」を証明することにある。
    一般のチューリング機械モデルでの下界証明は現在の数学では手が届かないが、
    決定木 (decision tree) という制限モデルなら、下界を厳密に証明できる。
    下界証明の基本技法「敵対者論法 (adversary argument)」を Lean で
    機械検証可能な形にすることが本ファイルの目的。

  主結果: D(OR_n) = n  (OR_n は evasive — 最悪ケースでは全 n 変数を
    読まない限り OR は計算できない)
    * 下界 orN_lower_bound : OR_n を計算する任意の決定木は深さ ≥ n
    * 上界 orTree_correct / orTree_depth : 深さちょうど n の決定木が存在
    * まとめ orN_evasive : 両者の合併

  依存: Lean 4 コアのみ (mathlib 不使用)。sorry なし。
-/

namespace Pnp
namespace Query

/-- 決定木: 葉 `leaf b` は出力 b を返す。内部ノード `node i f t` は
    変数 x_i を問い合わせ、false なら f、true なら t に進む。 -/
inductive DTree where
  | leaf (b : Bool)
  | node (i : Nat) (f : DTree) (t : DTree)
deriving Repr

namespace DTree

/-- 入力 `x` に対する決定木の評価 -/
def eval (x : Nat → Bool) : DTree → Bool
  | leaf b => b
  | node i f t => if x i then eval x t else eval x f

/-- 深さ = 最悪ケースの質問回数 -/
def depth : DTree → Nat
  | leaf _ => 0
  | node _ f t => 1 + Nat.max (depth f) (depth t)

/-- 入力 `x` の下で実際に問い合わせられる変数の列 (根から葉への経路) -/
def path (x : Nat → Bool) : DTree → List Nat
  | leaf _ => []
  | node i f t => i :: (if x i then path x t else path x f)

/-- 経路の長さは深さを超えない -/
theorem length_path_le_depth (x : Nat → Bool) (t : DTree) :
    (path x t).length ≤ depth t := by
  induction t with
  | leaf b => simp [path, depth]
  | node i f t ihf iht =>
    have h1 : (path x f).length ≤ Nat.max (depth f) (depth t) :=
      Nat.le_trans ihf (Nat.le_max_left _ _)
    have h2 : (path x t).length ≤ Nat.max (depth f) (depth t) :=
      Nat.le_trans iht (Nat.le_max_right _ _)
    cases hx : x i <;> simp [path, depth, hx] <;> omega

end DTree

/-- 1点更新: 座標 i の値だけ b に変えた入力 -/
def update (x : Nat → Bool) (i : Nat) (b : Bool) : Nat → Bool :=
  fun j => if j = i then b else x j

/-- 敵対者補題: 経路上に現れない変数を反転しても評価結果は変わらない。
    (決定木は読んでいない変数の値を知り得ない、という直観の形式化) -/
theorem eval_update_of_not_mem_path (x : Nat → Bool) (i : Nat) (b : Bool)
    (t : DTree) (h : i ∉ DTree.path x t) :
    DTree.eval (update x i b) t = DTree.eval x t := by
  induction t with
  | leaf c => rfl
  | node j f tt ihf iht =>
    simp only [DTree.path, List.mem_cons, not_or] at h
    obtain ⟨hij, hmem⟩ := h
    have hji : update x i b j = x j := by
      simp [update, Ne.symm hij]
    cases hxj : x j with
    | true =>
      simp [hxj] at hmem
      simp [DTree.eval, hji, hxj]
      exact iht hmem
    | false =>
      simp [hxj] at hmem
      simp [DTree.eval, hji, hxj]
      exact ihf hmem

/-- 補助 (鳩の巣の相棒): 重複のないリストが別のリストに含まれるなら、
    長さもそのリスト以下。 -/
theorem length_le_of_nodup_subset :
    ∀ (l₁ l₂ : List Nat), l₁.Nodup → (∀ a, a ∈ l₁ → a ∈ l₂) →
      l₁.length ≤ l₂.length := by
  intro l₁
  induction l₁ with
  | nil => intro l₂ _ _; exact Nat.zero_le _
  | cons a l ih =>
    intro l₂ hnd hsub
    have ha : a ∈ l₂ := hsub a List.mem_cons_self
    have hal : a ∉ l := (List.nodup_cons.mp hnd).1
    have hnd' : l.Nodup := (List.nodup_cons.mp hnd).2
    have hsub' : ∀ b, b ∈ l → b ∈ l₂.erase a := by
      intro b hb
      have hba : b ≠ a := fun he => hal (he ▸ hb)
      exact (List.mem_erase_of_ne hba).mpr (hsub b (List.mem_cons_of_mem a hb))
    have h1 := ih (l₂.erase a) hnd' hsub'
    have h2 : (l₂.erase a).length = l₂.length - 1 :=
      List.length_erase_of_mem ha
    have h3 : 0 < l₂.length := List.length_pos_of_mem ha
    simp only [List.length_cons]
    omega

/-- 鳩の巣: 長さ < n のリストは {0,…,n−1} の全要素を含むことはできない。 -/
theorem exists_lt_not_mem_of_length_lt (n : Nat) (l : List Nat)
    (h : l.length < n) : ∃ i, i < n ∧ i ∉ l := by
  refine Classical.byContradiction fun hc => ?_
  have hsub : ∀ a, a ∈ List.range n → a ∈ l := by
    intro a ha
    by_cases hm : a ∈ l
    · exact hm
    · exact absurd ⟨a, List.mem_range.mp ha, hm⟩ hc
  have hle := length_le_of_nodup_subset (List.range n) l (List.nodup_range) hsub
  simp only [List.length_range] at hle
  omega

/-- OR_n : 最初の n 変数の論理和 -/
def orN (n : Nat) (x : Nat → Bool) : Bool := (List.range n).any x

/-- 「決定木 t が n 変数ブール関数 F を計算する」 -/
def Computes (t : DTree) (F : (Nat → Bool) → Bool) : Prop :=
  ∀ x, DTree.eval x t = F x

/-- 全ゼロ入力 (敵対者の初期戦略) -/
def zeros : Nat → Bool := fun _ => false

theorem orN_zeros (n : Nat) : orN n zeros = false := by
  simp [orN, zeros]

theorem orN_update_zeros {n i : Nat} (hi : i < n) :
    orN n (update zeros i true) = true := by
  simp only [orN, List.any_eq_true]
  exact ⟨i, List.mem_range.mpr hi, by simp [update]⟩

/-- 下界定理 (敵対者論法): OR_n を計算する任意の決定木は深さ ≥ n。
    証明: 全ゼロ入力での経路長は深さ以下。深さ < n なら未質問の変数
    i < n が存在し (鳩の巣)、それを true に反転しても木の答えは変わらない
    (敵対者補題)。しかし OR の正しい値は false から true に変わる。矛盾。 -/
theorem orN_lower_bound {n : Nat} {t : DTree} (h : Computes t (orN n)) :
    n ≤ t.depth := by
  cases Nat.lt_or_ge t.depth n with
  | inr hge => exact hge
  | inl hlt =>
    exfalso
    have hlen : (DTree.path zeros t).length < n :=
      Nat.lt_of_le_of_lt (DTree.length_path_le_depth zeros t) hlt
    obtain ⟨i, hin, hnot⟩ := exists_lt_not_mem_of_length_lt n _ hlen
    have h1 : DTree.eval (update zeros i true) t = DTree.eval zeros t :=
      eval_update_of_not_mem_path zeros i true t hnot
    have h3 := h (update zeros i true)
    rw [h1, h zeros, orN_zeros, orN_update_zeros hin] at h3
    exact Bool.false_ne_true h3

/-- 上界の構成: 変数を n−1, n−2, …, 0 の順に読む素朴な決定木 -/
def orTree : Nat → DTree
  | 0 => .leaf false
  | n + 1 => .node n (orTree n) (.leaf true)

theorem orTree_depth (n : Nat) : (orTree n).depth = n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [orTree, DTree.depth, ih, Nat.max_zero]
    omega

theorem orTree_correct (n : Nat) : Computes (orTree n) (orN n) := by
  intro x
  induction n with
  | zero => simp [orTree, DTree.eval, orN]
  | succ n ih =>
    have hsplit : orN (n + 1) x = (orN n x || x n) := by
      simp [orN, List.range_succ]
    rw [hsplit]
    cases hx : x n with
    | true => simp [orTree, DTree.eval, hx]
    | false => simp [orTree, DTree.eval, hx, ih]

/-- 主定理: OR_n の決定木計算量はちょうど n (OR_n は evasive)。
    下界と上界が一致する、完全な計算量決定の機械検証。 -/
theorem orN_evasive (n : Nat) :
    (∀ t : DTree, Computes t (orN n) → n ≤ t.depth) ∧
    (∃ t : DTree, Computes t (orN n) ∧ t.depth = n) :=
  ⟨fun _ h => orN_lower_bound h,
   ⟨orTree n, orTree_correct n, orTree_depth n⟩⟩

-- 動作確認 (具体例): 5 変数の OR 決定木
#eval DTree.depth (orTree 5)                 -- 5
#eval DTree.eval (fun j => j == 3) (orTree 5) -- true  (x_3 = 1)
#eval DTree.eval (fun _ => false) (orTree 5)  -- false (全ゼロ)

-- 検証: 使用公理の確認 (sorryAx が無いこと)
#print axioms orN_lower_bound
#print axioms orN_evasive

end Query
end Pnp
