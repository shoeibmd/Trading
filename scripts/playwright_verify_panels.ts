import { test, expect } from '@playwright/test';
import { exec } from 'child_process';
import util from 'util';

const execPromise = util.promisify(exec);

test('Frontend UI verification with Market Panels', async ({ page }) => {
  console.log('Starting backend and frontend servers...');
  const backend = exec('cd backend && uvicorn app.main:app --port 8000');
  const frontend = exec('cd frontend && npm run dev -- --port 5174');

  // Wait for server to be ready
  await new Promise(resolve => setTimeout(resolve, 8000));

  try {
    await page.goto('http://localhost:5174');

    // Default workspace should be auto-created
    await expect(page.getByText('Default Workspace')).toBeVisible({ timeout: 10000 });

    // Add Market Overview Panel
    await page.click('button:has-text("Add Panel")');
    await expect(page.getByText('Market Overview')).toBeVisible();
    await page.click('text=Market Overview >> .. >> button:has-text("Add")');

    // Wait for the panel loading state to finish
    await page.waitForTimeout(1500);

    // Verify panel rendered and data fetched (Fallback data from mock endpoint)
    await expect(page.getByText('NIFTY 50', { exact: true })).toBeVisible();
    await expect(page.getByText('SENSEX', { exact: true })).toBeVisible();

    // Take screenshot of the configured workspace
    await page.screenshot({ path: '/tmp/market_panels_verification.png', fullPage: true });

  } finally {
    backend.kill();
    frontend.kill();
  }
});
