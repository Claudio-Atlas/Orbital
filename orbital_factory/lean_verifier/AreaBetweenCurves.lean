/-
  Orbital Verification: Area Between Curves
  Problem: Area enclosed by y = x + 2 and y = x²
  Claims:
    1. Intersection at x = -1 and x = 2
    2. Line above parabola on (-1, 2)
    3. ∫₋₁² [(x+2) - x²] dx = 9/2
-/
import Mathlib

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
  have : ∀ x : ℝ, HasDerivAt (fun x => x ^ 2 / 2 + 2 * x - x ^ 3 / 3)
      ((x + 2) - x ^ 2) x := by
    intro x
    have h1 := hasDerivAt_pow 2 x  -- deriv x^2 = 2*x
    have h2 := hasDerivAt_pow 3 x  -- deriv x^3 = 3*x^2
    have h3 := hasDerivAt_id x     -- deriv x = 1
    have hd := ((h1.div_const 2).add (h3.const_mul 2)).sub (h2.div_const 3)
    convert hd using 1
    ring
  rw [integral_eq_sub_of_hasDerivAt (fun x _ => this x)
      (by apply Continuous.intervalIntegrable; fun_prop)]
  norm_num
