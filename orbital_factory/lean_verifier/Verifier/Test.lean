import Mathlib

-- Test 1: Basic number theory Lean can verify
example : Nat.gcd 3 5 = 1 := by norm_num

-- Test 2: Verify a number theory fact
example : Nat.gcd 21 7 = 7 := by norm_num

-- Test 3: ZMod 15 is cyclic (as an additive group)
example : IsCyclic (Multiplicative (ZMod 15)) := by infer_instance

-- Test 4: Lean rejects false claims - uncomment to see failure:
-- example : Nat.gcd 3 5 = 2 := by norm_num
