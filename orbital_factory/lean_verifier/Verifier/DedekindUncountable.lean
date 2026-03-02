import Mathlib

/-!
# The Reals are Uncountable

Verified for Orbital Verification Pipeline.
The main theorem: ℝ is not countable.
This uses Mathlib's `Cardinal.not_countable_real` or equivalent.
-/

-- Claim 1: ℝ is uncountable (not countable)
theorem real_uncountable : ¬ Set.Countable (Set.univ : Set ℝ) := by
  exact Set.uncountable_univ_iff.mpr Cardinal.not_countable_real

-- Claim 2: The set of Dedekind cuts on ℚ defines ℝ
-- (This is definitional in Mathlib's construction — ℝ is defined via Cauchy sequences,
-- but is order-isomorphic to Dedekind cuts. We verify the key property used in the proof:
-- that nested closed intervals with rational endpoints yield a real number.)

-- Nested intervals property: used in the proof to construct α*
theorem nested_intervals_nonempty
    (a b : ℕ → ℝ)
    (hab : ∀ n, a n ≤ b n)
    (ha_mono : Monotone a)
    (hb_anti : Antitone b)
    (hab_cross : ∀ m n, a m ≤ b n) :
    ∃ x : ℝ, ∀ n, a n ≤ x ∧ x ≤ b n := by
  use sSup (Set.range a)
  intro n
  constructor
  · exact le_csSup (Set.bddAbove_range_of_forall_le_of_antitone hab hab_cross hb_anti) ⟨n, rfl⟩
  · exact csSup_le (Set.range_nonempty a) (fun _ ⟨m, hm⟩ => hm ▸ hab_cross m n)

