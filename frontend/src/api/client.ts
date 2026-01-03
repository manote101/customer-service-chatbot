// API client for chatbot backend

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface ChatUser {
  id?: string;
  is_authenticated: boolean;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  user?: ChatUser;
  metadata?: Record<string, any>;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

export interface Handoff {
  recommended: boolean;
  reason?: string;
  ticket_id?: string;
}

export interface ChatResponse {
  session_id: string;
  reply: string;
  messages?: ChatMessage[];
  handoff?: Handoff;
}

export interface HealthResponse {
  status: 'ok';
  service: string;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async health(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseURL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: { message: 'Request failed' } }));
      throw new Error(error.error?.message || 'Failed to send message');
    }

    return response.json();
  }
}

export const apiClient = new ApiClient();
