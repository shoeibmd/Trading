import { useEffect } from 'react';
import { wsClient, WebSocketCallback } from '@/services/websocketClient';

export function useWebSocket(channel: string | null, callback: WebSocketCallback) {
  useEffect(() => {
    // Ensure the global connection is started
    wsClient.connect();

    if (channel) {
      wsClient.subscribe(channel, callback);
    }

    return () => {
      if (channel) {
        wsClient.unsubscribe(channel, callback);
      }
    };
  }, [channel, callback]);
}
