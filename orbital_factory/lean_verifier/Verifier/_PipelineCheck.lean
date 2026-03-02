import Mathlib

-- Claim 1: ℝ is uncountable
theorem real_uncountable : ¬ Set.Countable (Set.univ : Set ℝ) := by
  apply Cardinal.not_countable_real

-- Claim 2: Nested intervals — find correct bddAbove lemma
theorem nested_intervals_nonempty
    (a b : ℕ → ℝ)
    (hab : ∀ n, a n ≤ b n)
    (ha_mono : Monotone a)
    (hb_anti : Antitone b)
    (hab_cross : ∀ m n, a m ≤ b n) :
    ∃ x : ℝ, ∀ n, a n ≤ x ∧ x ≤ b n := by
  have hbdd : BddAbove (Set.range a) := by
    use b 0
    rintro _ ⟨m, rfl⟩
    exact hab_cross m 0
  use sSup (Set.range a)
  intro n
  constructor
  · exact le_csSup hbdd ⟨n, rfl⟩
  · exact csSup_le (Set.range_nonempty a) (fun _ ⟨m, hm⟩ => hm ▸ hab_cross m n)
