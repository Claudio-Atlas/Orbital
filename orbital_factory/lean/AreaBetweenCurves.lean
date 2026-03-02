/-
  Orbital Verification: Area Between Curves
  Problem: Area enclosed by y = x + 2 and y = x²
  Claims:
    1. Intersection at x = -1 and x = 2
    2. Line above parabola on (-1, 2)
    3. ∫₋₁² [(x+2) - x²] dx = 9/2
-/
import Mathlib.Analysis.SpecialFunctions.Integrals
import Mathlib.Tactic

open MeasureTheory Real Set intervalIntegral

-- Claim 1: Intersection points
theorem intersections :
    ∀ x : ℝ, x + 2 = x ^ 2 ↔ x = -1 ∨ x = 2 := by
  intro x
  constructor
  · intro h
    have : x ^ 2 - x - 2 = 0 := by linarith
    have : (x - 2) * (x + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp this with h1 | h1
    · right; linarith
    · left; linarith
  · rintro (rfl | rfl) <;> ring

-- Claim 2: Line above parabola on (-1, 2)
theorem line_above_parabola :
    ∀ x : ℝ, -1 < x → x < 2 → x ^ 2 < x + 2 := by
  intro x hx1 hx2
  nlinarith [sq_nonneg (x + 1), sq_nonneg (x - 2)]

-- Claim 3: The integral equals 9/2
theorem integral_value :
    ∫ x in (-1 : ℝ)..2, ((x + 2) - x ^ 2) = 9 / 2 := by
  have h1 : ∀ x : ℝ, (x + 2) - x ^ 2 = -x ^ 2 + x + 2 := by intro x; ring
  simp_rw [h1]
  simp only [integral_add (by fun_prop) (by fun_prop),
             integral_sub (by fun_prop) (by fun_prop),
             integral_neg, integral_pow, integral_id, integral_const,
             integral_mul_left]
  norm_num
