import { describe, it, expect, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { usePanelData } from '../../hooks/usePanelData';

describe('usePanelData hook', () => {
  it('should initially return loading state', () => {
    const { result } = renderHook(() => usePanelData([], {}, 0));
    expect(result.current.status).toBe('loading');
  });

  it('should transition to success state with data', async () => {
    const { result } = renderHook(() => usePanelData([], { message: 'Test data' }, 0));

    await waitFor(() => {
      expect(result.current.status).toBe('success');
    });

    expect(result.current.data?.message).toBe('Test data');
  });

  it('should handle simulated error state based on config', async () => {
    const { result } = renderHook(() => usePanelData([], { simulateError: true }, 0));

    await waitFor(() => {
      expect(result.current.status).toBe('error');
    });

    expect(result.current.error).toContain('Simulated error');
  });

  it('should handle simulated empty state based on config', async () => {
    const { result } = renderHook(() => usePanelData([], { simulateEmpty: true }, 0));

    await waitFor(() => {
      expect(result.current.status).toBe('empty');
    });
  });

  it('should refetch data when refreshTrigger changes', async () => {
    const { result, rerender } = renderHook(
      ({ trigger }) => usePanelData([], {}, trigger),
      { initialProps: { trigger: 0 } }
    );

    await waitFor(() => {
      expect(result.current.status).toBe('success');
    });

    rerender({ trigger: 1 });

    expect(result.current.status).toBe('loading');

    await waitFor(() => {
      expect(result.current.status).toBe('success');
    });
  });
});
