import { describe, it, expect } from 'vitest'

// Test utility functions that exist or should exist in the app

describe('Utility Functions', () => {
  
  describe('Email Validation', () => {
    const isValidEmail = (email: string): boolean => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(email)
    }

    it('should accept valid email formats', () => {
      expect(isValidEmail('test@example.com')).toBe(true)
      expect(isValidEmail('user.name@domain.org')).toBe(true)
      expect(isValidEmail('user+tag@example.co.uk')).toBe(true)
    })

    it('should reject invalid email formats', () => {
      expect(isValidEmail('notanemail')).toBe(false)
      expect(isValidEmail('missing@domain')).toBe(false)
      expect(isValidEmail('@nodomain.com')).toBe(false)
      expect(isValidEmail('spaces in@email.com')).toBe(false)
    })
  })

  describe('Password Validation', () => {
    const isValidPassword = (password: string): boolean => {
      return password.length >= 6
    }

    it('should accept passwords with 6+ characters', () => {
      expect(isValidPassword('123456')).toBe(true)
      expect(isValidPassword('password123')).toBe(true)
      expect(isValidPassword('verylongpassword')).toBe(true)
    })

    it('should reject passwords with less than 6 characters', () => {
      expect(isValidPassword('12345')).toBe(false)
      expect(isValidPassword('abc')).toBe(false)
      expect(isValidPassword('')).toBe(false)
    })
  })

  describe('Minutes Formatting', () => {
    const formatMinutes = (minutes: number): string => {
      if (minutes < 60) return `${minutes} min`
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`
    }

    it('should format minutes under 60 correctly', () => {
      expect(formatMinutes(5)).toBe('5 min')
      expect(formatMinutes(30)).toBe('30 min')
      expect(formatMinutes(59)).toBe('59 min')
    })

    it('should format hours correctly', () => {
      expect(formatMinutes(60)).toBe('1h')
      expect(formatMinutes(120)).toBe('2h')
    })

    it('should format hours and minutes correctly', () => {
      expect(formatMinutes(90)).toBe('1h 30m')
      expect(formatMinutes(150)).toBe('2h 30m')
    })
  })

  describe('Price Formatting', () => {
    const formatPrice = (cents: number): string => {
      return `$${(cents / 100).toFixed(2)}`
    }

    it('should format cents to dollars correctly', () => {
      expect(formatPrice(499)).toBe('$4.99')
      expect(formatPrice(999)).toBe('$9.99')
      expect(formatPrice(1999)).toBe('$19.99')
      expect(formatPrice(100)).toBe('$1.00')
    })
  })

  describe('Date Formatting', () => {
    const formatDate = (dateString: string): string => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        timeZone: 'UTC', // Use UTC to avoid timezone issues
      })
    }

    it('should format dates correctly', () => {
      // Use ISO format with explicit UTC to avoid timezone issues
      expect(formatDate('2026-02-11T12:00:00Z')).toBe('Feb 11, 2026')
      expect(formatDate('2026-12-25T12:00:00Z')).toBe('Dec 25, 2026')
    })
  })

  describe('Video Expiration', () => {
    const isExpired = (expiresAt: string): boolean => {
      return new Date(expiresAt) < new Date()
    }

    const hoursUntilExpiry = (expiresAt: string): number => {
      const diff = new Date(expiresAt).getTime() - new Date().getTime()
      return Math.max(0, Math.floor(diff / (1000 * 60 * 60)))
    }

    it('should detect expired videos', () => {
      const pastDate = new Date(Date.now() - 86400000).toISOString() // 1 day ago
      expect(isExpired(pastDate)).toBe(true)
    })

    it('should detect non-expired videos', () => {
      const futureDate = new Date(Date.now() + 86400000).toISOString() // 1 day from now
      expect(isExpired(futureDate)).toBe(false)
    })

    it('should calculate hours until expiry', () => {
      const in24Hours = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
      expect(hoursUntilExpiry(in24Hours)).toBeGreaterThanOrEqual(23)
      expect(hoursUntilExpiry(in24Hours)).toBeLessThanOrEqual(24)
    })
  })
})

describe('Stripe Utilities', () => {
  describe('Tier Mapping', () => {
    type Tier = 'starter' | 'standard' | 'pro'
    
    const tierMinutes: Record<Tier, number> = {
      starter: 10,
      standard: 30,
      pro: 100,
    }

    const tierPriceCents: Record<Tier, number> = {
      starter: 499,
      standard: 999,
      pro: 2499,
    }

    it('should map tiers to correct minutes', () => {
      expect(tierMinutes.starter).toBe(10)
      expect(tierMinutes.standard).toBe(30)
      expect(tierMinutes.pro).toBe(100)
    })

    it('should map tiers to correct prices', () => {
      expect(tierPriceCents.starter).toBe(499)
      expect(tierPriceCents.standard).toBe(999)
      expect(tierPriceCents.pro).toBe(2499)
    })

    it('should calculate price per minute correctly', () => {
      const starterPerMin = tierPriceCents.starter / tierMinutes.starter
      const proPerMin = tierPriceCents.pro / tierMinutes.pro
      
      // Pro should be cheaper per minute
      expect(proPerMin).toBeLessThan(starterPerMin)
    })
  })
})

describe('Error Handling', () => {
  describe('Supabase Error Codes', () => {
    const isProfileNotFound = (errorCode: string): boolean => {
      return errorCode === 'PGRST116'
    }

    const isAuthError = (errorCode: string): boolean => {
      return errorCode.startsWith('auth/')
    }

    it('should identify profile not found errors', () => {
      expect(isProfileNotFound('PGRST116')).toBe(true)
      expect(isProfileNotFound('PGRST100')).toBe(false)
    })
  })
})
