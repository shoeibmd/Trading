import { test, expect } from '@playwright/test';
import { exec } from 'child_process';
import util from 'util';

const execPromise = util.promisify(exec);

test('Frontend Workspace System E2E', async ({ page }) => {
  console.log('Starting backend and frontend servers...');
  // Need backend to test persistence
  const backend = exec('cd backend && uvicorn app.main:app --port 8000');
  const frontend = exec('cd frontend && npm run dev -- --port 5174');

  // Wait for servers
  await new Promise(resolve => setTimeout(resolve, 8000));

  try {
    await page.goto('http://localhost:5174');

    // Default workspace should be auto-created
    await expect(page.getByText('Default Workspace')).toBeVisible({ timeout: 10000 });

    // Empty state should be visible
    await expect(page.getByText('Workspace is empty')).toBeVisible();

    // Add a panel
    await page.click('button:has-text("Add Panel")');
    await expect(page.getByText('Add Panel')).toBeVisible();
    await page.click('button:has-text("Add")'); // Click the first "Add" button in the modal

    // Wait for the panel loading state to finish (800ms)
    await page.waitForTimeout(1500);

    // Verify panel rendered in the grid
    await expect(page.getByText('Test Panel', { exact: true })).toBeVisible();

    // Create new workspace
    await page.click('button:has-text("Manage")');
    await page.click('button:has-text("+ Create New Workspace")');
    await page.fill('input[id="ws-name"]', 'Research Layout');
    await page.click('button:has-text("Create")');

    // The modal should show Research Layout now
    await expect(page.getByText('Research Layout')).toBeVisible();
    // Click on Research Layout to switch to it
    await page.click('h4:has-text("Research Layout")');

    // Should be an empty workspace
    await expect(page.getByText('Workspace is empty')).toBeVisible();

    // Switch back to Default Workspace
    await page.selectOption('select', { label: 'Default Workspace' });

    // Should still have our panel because of persistence
    await expect(page.getByText('Test Panel', { exact: true })).toBeVisible();

    await page.screenshot({ path: '/tmp/workspace_system.png', fullPage: true });

  } finally {
    backend.kill();
    frontend.kill();
  }
});
