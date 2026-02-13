import { test as base, Page } from '@playwright/test'

// Test user credentials (create these in Supabase for testing)
export const TEST_USER = {
  email: 'test@orbital-test.com',
  password: 'testpassword123',
}

// Fixture that provides an authenticated page
export const test = base.extend<{ authenticatedPage: Page }>({
  authenticatedPage: async ({ page }, use) => {
    // Login before test
    await page.goto('/login')
    await page.getByPlaceholder(/email|you@/i).fill(TEST_USER.email)
    await page.getByPlaceholder(/password|••••/i).fill(TEST_USER.password)
    await page.getByRole('button', { name: /sign in|log in/i }).click()
    
    // Wait for redirect to dashboard
    await page.waitForURL(/dashboard/, { timeout: 10000 })
    
    // Use the authenticated page
    await use(page)
  },
})

export { expect } from '@playwright/test'

// Helper to login programmatically
export async function login(page: Page, email: string = TEST_USER.email, password: string = TEST_USER.password) {
  await page.goto('/login')
  await page.getByPlaceholder(/email|you@/i).fill(email)
  await page.getByPlaceholder(/password|••••/i).fill(password)
  await page.getByRole('button', { name: /sign in|log in/i }).click()
  await page.waitForURL(/dashboard/, { timeout: 10000 })
}

// Helper to logout
export async function logout(page: Page) {
  // Click user menu and logout
  const userMenu = page.getByRole('button', { name: /account|profile|settings/i })
  if (await userMenu.isVisible()) {
    await userMenu.click()
    await page.getByRole('button', { name: /log out|sign out/i }).click()
  } else {
    // Try direct logout link/button
    await page.getByRole('link', { name: /log out|sign out/i }).click()
  }
  await page.waitForURL(/login/)
}

// Helper to clear all auth state
export async function clearAuth(page: Page) {
  await page.context().clearCookies()
  await page.evaluate(() => {
    localStorage.clear()
    sessionStorage.clear()
  })
}
