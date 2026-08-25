import { test, expect } from '@playwright/test';
import { exec } from 'child_process';
import util from 'util';

const execPromise = util.promisify(exec);

test('Frontend UI verification with Panel Framework', async ({ page }) => {
  console.log('Starting frontend dev server...');
  const server = exec('cd frontend && npm run dev -- --port 5174');

  // Wait for server to be ready
  await new Promise(resolve => setTimeout(resolve, 5000));

  try {
    await page.goto('http://localhost:5174');

    // Check if empty state exists
    await expect(page.getByText('Workspace is empty')).toBeVisible();

    // Add a panel
    await page.click('button:has-text("Add Test Panel")');

    // Wait for the panel loading state to finish (it has an 800ms simulated delay)
    await page.waitForTimeout(1000);

    // Verify panel header
    await expect(page.getByText('Test Panel', { exact: true })).toBeVisible();

    // Verify default panel message
    await expect(page.getByText('Hello World')).toBeVisible();

    // Open settings modal
    await page.click('button[title="Settings"]');

    // Verify modal is open and has fields
    await expect(page.getByText('Panel Configuration')).toBeVisible();
    await expect(page.getByLabel('Custom Message')).toBeVisible();

    // Change a setting
    await page.fill('input[id="message"]', 'Updated Test Data');
    await page.click('button:has-text("Save changes")');

    // Verify setting was applied
    await expect(page.getByText('Updated Test Data')).toBeVisible();

    // Take screenshot of the configured workspace
    await page.screenshot({ path: '/tmp/panel_framework_verification.png', fullPage: true });

  } finally {
    server.kill();
  }
});
