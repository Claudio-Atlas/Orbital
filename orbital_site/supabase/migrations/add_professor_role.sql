-- Add role column to profiles table
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS role text DEFAULT 'student' CHECK (role IN ('student', 'professor'));

-- Index for role-based queries
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);
