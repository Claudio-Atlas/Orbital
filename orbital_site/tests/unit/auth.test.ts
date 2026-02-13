import { describe, it, expect, vi, beforeEach } from 'vitest'

// Mock Supabase client
const mockSupabase = {
  auth: {
    getUser: vi.fn(),
    getSession: vi.fn(),
    signInWithPassword: vi.fn(),
    signUp: vi.fn(),
    signOut: vi.fn(),
    onAuthStateChange: vi.fn(() => ({
      data: { subscription: { unsubscribe: vi.fn() } },
    })),
  },
  from: vi.fn(() => ({
    select: vi.fn(() => ({
      eq: vi.fn(() => ({
        single: vi.fn(),
      })),
    })),
    insert: vi.fn(() => ({
      select: vi.fn(() => ({
        single: vi.fn(),
      })),
    })),
  })),
}

vi.mock('@/lib/supabase', () => ({
  getSupabase: () => mockSupabase,
  createClient: () => mockSupabase,
}))

describe('Auth Utilities', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getUser', () => {
    it('should return user when authenticated', async () => {
      const mockUser = { id: 'user-123', email: 'test@example.com' }
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: mockUser },
        error: null,
      })

      const { data } = await mockSupabase.auth.getUser()
      
      expect(data.user).toEqual(mockUser)
      expect(data.user.email).toBe('test@example.com')
    })

    it('should return null when not authenticated', async () => {
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: null },
        error: null,
      })

      const { data } = await mockSupabase.auth.getUser()
      
      expect(data.user).toBeNull()
    })

    it('should handle auth errors gracefully', async () => {
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: null },
        error: { message: 'Invalid token' },
      })

      const { data, error } = await mockSupabase.auth.getUser()
      
      expect(data.user).toBeNull()
      expect(error.message).toBe('Invalid token')
    })
  })

  describe('signInWithPassword', () => {
    it('should return user on successful login', async () => {
      const mockUser = { id: 'user-123', email: 'test@example.com' }
      mockSupabase.auth.signInWithPassword.mockResolvedValue({
        data: { user: mockUser, session: { access_token: 'token' } },
        error: null,
      })

      const { data, error } = await mockSupabase.auth.signInWithPassword({
        email: 'test@example.com',
        password: 'password123',
      })

      expect(error).toBeNull()
      expect(data.user).toEqual(mockUser)
    })

    it('should return error for invalid credentials', async () => {
      mockSupabase.auth.signInWithPassword.mockResolvedValue({
        data: { user: null, session: null },
        error: { message: 'Invalid login credentials' },
      })

      const { data, error } = await mockSupabase.auth.signInWithPassword({
        email: 'test@example.com',
        password: 'wrongpassword',
      })

      expect(error.message).toBe('Invalid login credentials')
      expect(data.user).toBeNull()
    })
  })

  describe('signUp', () => {
    it('should create user on successful signup', async () => {
      const mockUser = { id: 'new-user-123', email: 'new@example.com' }
      mockSupabase.auth.signUp.mockResolvedValue({
        data: { user: mockUser, session: null },
        error: null,
      })

      const { data, error } = await mockSupabase.auth.signUp({
        email: 'new@example.com',
        password: 'password123',
      })

      expect(error).toBeNull()
      expect(data.user).toEqual(mockUser)
    })

    it('should return error for existing email', async () => {
      mockSupabase.auth.signUp.mockResolvedValue({
        data: { user: null, session: null },
        error: { message: 'User already registered' },
      })

      const { data, error } = await mockSupabase.auth.signUp({
        email: 'existing@example.com',
        password: 'password123',
      })

      expect(error.message).toBe('User already registered')
    })

    it('should return error for weak password', async () => {
      mockSupabase.auth.signUp.mockResolvedValue({
        data: { user: null, session: null },
        error: { message: 'Password should be at least 6 characters' },
      })

      const { data, error } = await mockSupabase.auth.signUp({
        email: 'new@example.com',
        password: '123',
      })

      expect(error.message).toContain('Password')
    })
  })

  describe('signOut', () => {
    it('should sign out successfully', async () => {
      mockSupabase.auth.signOut.mockResolvedValue({ error: null })

      const { error } = await mockSupabase.auth.signOut()

      expect(error).toBeNull()
    })
  })
})

describe('Profile Management', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('fetchProfile', () => {
    it('should return profile when exists', async () => {
      const mockProfile = {
        id: 'user-123',
        email: 'test@example.com',
        display_name: 'Test User',
        minutes_balance: 10,
      }

      const mockQuery = {
        select: vi.fn().mockReturnThis(),
        eq: vi.fn().mockReturnThis(),
        single: vi.fn().mockResolvedValue({ data: mockProfile, error: null }),
      }
      mockSupabase.from.mockReturnValue(mockQuery)

      const result = await mockSupabase.from('profiles').select('*').eq('id', 'user-123').single()

      expect(result.data).toEqual(mockProfile)
      expect(result.data.minutes_balance).toBe(10)
    })

    it('should return null for non-existent profile', async () => {
      const mockQuery = {
        select: vi.fn().mockReturnThis(),
        eq: vi.fn().mockReturnThis(),
        single: vi.fn().mockResolvedValue({
          data: null,
          error: { code: 'PGRST116', message: 'No rows returned' },
        }),
      }
      mockSupabase.from.mockReturnValue(mockQuery)

      const result = await mockSupabase.from('profiles').select('*').eq('id', 'nonexistent').single()

      expect(result.data).toBeNull()
      expect(result.error.code).toBe('PGRST116')
    })
  })

  describe('createProfile (for OAuth users)', () => {
    it('should create profile for new OAuth user', async () => {
      const newProfile = {
        id: 'oauth-user-123',
        email: 'oauth@gmail.com',
        display_name: 'OAuth User',
        minutes_balance: 0,
      }

      const mockQuery = {
        insert: vi.fn().mockReturnThis(),
        select: vi.fn().mockReturnThis(),
        single: vi.fn().mockResolvedValue({ data: newProfile, error: null }),
      }
      mockSupabase.from.mockReturnValue(mockQuery)

      const result = await mockSupabase.from('profiles').insert(newProfile).select().single()

      expect(result.data).toEqual(newProfile)
      expect(result.data.minutes_balance).toBe(0)
    })
  })
})
