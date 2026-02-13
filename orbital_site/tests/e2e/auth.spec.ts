import { test, expect } from '@playwright/test'

test.describe('Authentication Flow', () => {
  
  test.describe('Login Page', () => {
    test('should display login form', async ({ page }) => {
      await page.goto('/login')
      
      // Check for email and password inputs by placeholder
      await expect(page.getByPlaceholder(/email|you@/i)).toBeVisible()
      await expect(page.getByPlaceholder(/password|••••/i)).toBeVisible()
      await expect(page.getByRole('button', { name: /sign in|log in/i })).toBeVisible()
    })

    test('should show error for invalid credentials', async ({ page }) => {
      await page.goto('/login')
      
      await page.getByPlaceholder(/email|you@/i).fill('invalid@example.com')
      await page.getByPlaceholder(/password|••••/i).fill('wrongpassword')
      await page.getByRole('button', { name: /sign in|log in/i }).click()
      
      // Should show error message
      await expect(page.getByText(/invalid|incorrect|error/i)).toBeVisible({ timeout: 10000 })
    })

    test('should show error for empty fields', async ({ page }) => {
      await page.goto('/login')
      
      await page.getByRole('button', { name: /sign in|log in/i }).click()
      
      // HTML5 validation or custom error
      const emailInput = page.getByPlaceholder(/email|you@/i)
      await expect(emailInput).toHaveAttribute('required', '')
    })

    test('should have link to signup page', async ({ page }) => {
      await page.goto('/login')
      
      const signupLink = page.getByRole('link', { name: /sign up|create account|register/i })
      await expect(signupLink).toBeVisible()
      
      await signupLink.click()
      await expect(page).toHaveURL(/signup/)
    })

    test('should have link to forgot password', async ({ page }) => {
      await page.goto('/login')
      
      const forgotLink = page.getByRole('link', { name: /forgot|reset/i })
      await expect(forgotLink).toBeVisible()
      
      await forgotLink.click()
      await expect(page).toHaveURL(/forgot/)
    })

    test('should have Google OAuth button', async ({ page }) => {
      await page.goto('/login')
      
      const googleButton = page.getByRole('button', { name: /google/i })
      await expect(googleButton).toBeVisible()
    })

    test('Google OAuth button should trigger auth flow', async ({ page }) => {
      await page.goto('/login')
      
      const googleButton = page.getByRole('button', { name: /google/i })
      await expect(googleButton).toBeEnabled()
      
      // Just verify the button exists and is clickable
      // Full OAuth flow requires real Google credentials
      // In CI, this would use a mock or be skipped
      await googleButton.click()
      
      // Should navigate away from login page (to Google or Supabase)
      await page.waitForURL((url) => !url.pathname.includes('/login'), { timeout: 10000 })
    })
  })

  test.describe('Signup Page', () => {
    test('should display signup form', async ({ page }) => {
      await page.goto('/signup')
      
      await expect(page.getByPlaceholder(/email|you@/i)).toBeVisible()
      await expect(page.getByPlaceholder(/password|••••/i).first()).toBeVisible()
    })

    test('should have link to login page', async ({ page }) => {
      await page.goto('/signup')
      
      const loginLink = page.getByRole('link', { name: /sign in|log in|already have/i })
      await expect(loginLink).toBeVisible()
      
      await loginLink.click()
      await expect(page).toHaveURL(/login/)
    })

    test('should validate email format', async ({ page }) => {
      await page.goto('/signup')
      
      const emailInput = page.getByPlaceholder(/email|you@/i)
      await emailInput.fill('notanemail')
      
      // Check HTML5 validation
      const validationMessage = await emailInput.evaluate((el: HTMLInputElement) => el.validationMessage)
      expect(validationMessage).toBeTruthy()
    })

    test('should require password', async ({ page }) => {
      await page.goto('/signup')
      
      // The signup form has password requirements - just verify the field is required
      const passwordInput = page.getByPlaceholder(/password|••••/i).first()
      await expect(passwordInput).toHaveAttribute('required', '')
    })
  })

  test.describe('Forgot Password Page', () => {
    test('should display forgot password form', async ({ page }) => {
      await page.goto('/forgot-password')
      
      await expect(page.getByPlaceholder(/email|you@/i)).toBeVisible()
      await expect(page.getByRole('button', { name: /reset|send|submit/i })).toBeVisible()
    })

    test('should show confirmation after submit', async ({ page }) => {
      await page.goto('/forgot-password')
      
      await page.getByPlaceholder(/email|you@/i).fill('test@example.com')
      await page.getByRole('button', { name: /reset|send|submit/i }).click()
      
      // Should show confirmation message
      await expect(page.getByText(/check your email|sent|instructions/i)).toBeVisible({ timeout: 10000 })
    })
  })

  test.describe('Protected Routes', () => {
    test('should redirect unauthenticated user from dashboard', async ({ page }) => {
      await page.goto('/dashboard')
      
      // Should redirect to login
      await expect(page).toHaveURL(/login/, { timeout: 10000 })
    })

    test('should redirect unauthenticated user from settings', async ({ page }) => {
      await page.goto('/settings')
      
      await expect(page).toHaveURL(/login/, { timeout: 10000 })
    })

    test('should redirect unauthenticated user from videos', async ({ page }) => {
      await page.goto('/videos')
      
      await expect(page).toHaveURL(/login/, { timeout: 10000 })
    })

    test('should redirect unauthenticated user from purchases', async ({ page }) => {
      await page.goto('/purchases')
      
      await expect(page).toHaveURL(/login/, { timeout: 10000 })
    })
  })

  test.describe('Public Routes', () => {
    test('homepage should be accessible', async ({ page }) => {
      await page.goto('/')
      
      await expect(page).toHaveURL('/')
      // Should have some content
      await expect(page.locator('body')).not.toBeEmpty()
    })

    test('terms page should be accessible', async ({ page }) => {
      await page.goto('/terms')
      
      await expect(page).toHaveURL('/terms')
    })

    test('privacy page should be accessible', async ({ page }) => {
      await page.goto('/privacy')
      
      await expect(page).toHaveURL('/privacy')
    })
  })
})
