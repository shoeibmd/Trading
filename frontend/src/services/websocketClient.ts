export type WebSocketCallback = (data: any) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private isConnecting: boolean = false;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private heartbeatInterval: ReturnType<typeof setInterval> | null = null;

  private callbacks: Map<string, Set<WebSocketCallback>> = new Map();

  constructor(url: string) {
    this.url = url;
  }

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN || this.isConnecting) return;

    this.isConnecting = true;
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.isConnecting = false;
      this.reconnectAttempts = 0;
      this.startHeartbeat();
      console.log('WebSocket Connected');

      // Resubscribe to channels
      this.callbacks.forEach((_, channel) => {
        this.send({ action: 'subscribe', channel });
      });
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'heartbeat_ack') return;

        const channel = message.channel;
        if (channel && this.callbacks.has(channel)) {
          this.callbacks.get(channel)!.forEach(cb => cb(message.data));
        }
      } catch (err) {
        console.error('WebSocket parse error', err);
      }
    };

    this.ws.onclose = () => {
      this.isConnecting = false;
      this.stopHeartbeat();
      this.handleReconnect();
    };

    this.ws.onerror = (err) => {
      console.error('WebSocket error', err);
    };
  }

  private handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('Max WebSocket reconnects reached');
    }
  }

  private startHeartbeat() {
    this.stopHeartbeat();
    this.heartbeatInterval = setInterval(() => {
      this.send({ action: 'heartbeat' });
    }, 30000);
  }

  private stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  send(payload: object) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(payload));
    }
  }

  subscribe(channel: string, callback: WebSocketCallback) {
    if (!this.callbacks.has(channel)) {
      this.callbacks.set(channel, new Set());
      this.send({ action: 'subscribe', channel });
    }
    this.callbacks.get(channel)!.add(callback);
  }

  unsubscribe(channel: string, callback: WebSocketCallback) {
    if (this.callbacks.has(channel)) {
      const channelCbs = this.callbacks.get(channel)!;
      channelCbs.delete(callback);
      if (channelCbs.size === 0) {
        this.callbacks.delete(channel);
        this.send({ action: 'unsubscribe', channel });
      }
    }
  }

  disconnect() {
    this.stopHeartbeat();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

const wsUrl = import.meta.env.VITE_WS_URL || `ws://${window.location.host}/api/v1/ws`;
export const wsClient = new WebSocketClient(wsUrl);
