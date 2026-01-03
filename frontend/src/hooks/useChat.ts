import { useState, useEffect, useRef, useCallback } from 'react';
import { apiClient, ChatMessage, ChatRequest } from '../api/client';

interface UseChatOptions {
  onError?: (error: Error) => void;
}

export const useChat = (options: UseChatOptions = {}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessage: ChatMessage = {
      role: 'assistant',
      content: "Hi! I'm the support assistant. What can I help you with?",
      timestamp: new Date().toISOString(),
    };
    setMessages([welcomeMessage]);
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      setError(null);
      const userMessage: ChatMessage = {
        role: 'user',
        content: content.trim(),
        timestamp: new Date().toISOString(),
      };

      // Optimistically add user message
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const request: ChatRequest = {
          message: content.trim(),
          session_id: sessionId || undefined,
          metadata: {
            locale: navigator.language,
          },
        };

        const response = await apiClient.sendMessage(request);

        // Save session ID
        if (!sessionId) {
          setSessionId(response.session_id);
        }

        // Add bot response
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.reply,
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, assistantMessage]);

        // Show handoff notification if recommended
        if (response.handoff?.recommended) {
          const systemMessage: ChatMessage = {
            role: 'system',
            content: response.handoff.ticket_id
              ? `Escalation created. Ticket ID: ${response.handoff.ticket_id}`
              : 'Your request will be routed to a support agent.',
            timestamp: new Date().toISOString(),
          };
          setMessages((prev) => [...prev, systemMessage]);
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
        setError(errorMessage);
        
        // Add error message to chat
        const errorChatMessage: ChatMessage = {
          role: 'system',
          content: `Error: ${errorMessage}. Please try again.`,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, errorChatMessage]);

        if (options.onError) {
          options.onError(err instanceof Error ? err : new Error(errorMessage));
        }
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId, options]
  );

  return {
    messages,
    isLoading,
    error,
    sessionId,
    sendMessage,
    messagesEndRef,
  };
};
