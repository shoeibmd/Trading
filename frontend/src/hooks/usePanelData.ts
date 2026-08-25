import { useState, useEffect } from 'react';
import { DataRequirement, PanelConfiguration, PanelState } from '../types/panel';

/**
 * Hook to manage data fetching and realtime subscriptions for panels.
 * Currently returns mocked data for Phase 9 framework validation.
 * In Phase 11+, this will be replaced with real React Query / WebSocket logic.
 */
export function usePanelData(
  requirements: DataRequirement[],
  configuration: PanelConfiguration,
  refreshTrigger: number
): PanelState {
  const [state, setState] = useState<PanelState>({ status: 'loading' });

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      setState({ status: 'loading' });

      try {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 800));

        if (!isMounted) return;

        // Simulate an error state for testing based on a specific config
        if (configuration.simulateError) {
          setState({
            status: 'error',
            error: 'Failed to load panel data. (Simulated error)',
            lastUpdated: new Date()
          });
          return;
        }

        // Simulate an empty state for testing
        if (configuration.simulateEmpty) {
          setState({
            status: 'empty',
            lastUpdated: new Date()
          });
          return;
        }

        // Return mocked success data
        setState({
          status: 'success',
          data: {
            message: configuration.message || 'Hello from mocked data!',
            requirements: requirements,
            timestamp: new Date().toISOString()
          },
          lastUpdated: new Date()
        });
      } catch (error) {
        if (isMounted) {
          setState({
            status: 'error',
            error: error instanceof Error ? error.message : 'Unknown error',
            lastUpdated: new Date()
          });
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [requirements, configuration, refreshTrigger]);

  return state;
}
