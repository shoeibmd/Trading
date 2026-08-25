import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PanelContainer } from '../../components/panels/PanelContainer';
import { testPanelDefinition } from '../../components/panels/examples/TestPanel';
import * as usePanelDataModule from '../../hooks/usePanelData';

// Mock the hook to control states synchronously
vi.mock('../../hooks/usePanelData', () => ({
  usePanelData: vi.fn()
}));

describe('PanelContainer', () => {
  it('renders loading state initially', () => {
    vi.mocked(usePanelDataModule.usePanelData).mockReturnValue({ status: 'loading' });

    render(
      <PanelContainer
        panelId="test-1"
        definition={testPanelDefinition}
        initialConfiguration={{}}
        onClose={vi.fn()}
      />
    );

    expect(screen.getByTestId('panel-loading')).toBeInTheDocument();
  });

  it('renders error state correctly', () => {
    vi.mocked(usePanelDataModule.usePanelData).mockReturnValue({
      status: 'error',
      error: 'Test error message'
    });

    render(
      <PanelContainer
        panelId="test-1"
        definition={testPanelDefinition}
        initialConfiguration={{}}
        onClose={vi.fn()}
      />
    );

    expect(screen.getByTestId('panel-error')).toBeInTheDocument();
    expect(screen.getByText('Test error message')).toBeInTheDocument();
  });

  it('renders empty state correctly', () => {
    vi.mocked(usePanelDataModule.usePanelData).mockReturnValue({ status: 'empty' });

    render(
      <PanelContainer
        panelId="test-1"
        definition={testPanelDefinition}
        initialConfiguration={{}}
        onClose={vi.fn()}
      />
    );

    expect(screen.getByTestId('panel-empty')).toBeInTheDocument();
  });

  it('renders the component on success', () => {
    vi.mocked(usePanelDataModule.usePanelData).mockReturnValue({
      status: 'success',
      data: { message: 'Loaded' }
    });

    render(
      <PanelContainer
        panelId="test-1"
        definition={testPanelDefinition}
        initialConfiguration={{ message: 'Custom Test Message' }}
        onClose={vi.fn()}
      />
    );

    expect(screen.getByText('Custom Test Message')).toBeInTheDocument();
  });
});
