import React, { useState } from 'react';
import { MessageBubble } from '../components/MessageBubble';
import { ChatInput } from '../components/ChatInput';
import { TypingIndicator } from '../components/TypingIndicator';
import { QuickReplies } from '../components/QuickReplies';
import { useChat } from '../hooks/useChat';

const SUGGESTED_TOPICS = [
  { label: 'Track an order', value: 'Where is my order?' },
  { label: 'Returns & refunds', value: 'How do I return an item?' },
  { label: 'Shipping info', value: 'How long does shipping take?' },
  { label: 'Product help', value: 'I need help with a product' },
];

export const ChatPage: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [showQuickReplies, setShowQuickReplies] = useState(true);
  const { messages, isLoading, error, sendMessage, messagesEndRef } = useChat();

  const handleSend = () => {
    if (inputValue.trim()) {
      sendMessage(inputValue);
      setInputValue('');
      setShowQuickReplies(false);
    }
  };

  const handleQuickReply = (value: string) => {
    setInputValue(value);
    sendMessage(value);
    setInputValue('');
    setShowQuickReplies(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
            CS
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Support Chat</h1>
            <p className="text-sm text-gray-500">We're here to help</p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}
        
        <TypingIndicator show={isLoading} />
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Replies (shown only initially) */}
      {showQuickReplies && messages.length === 1 && (
        <QuickReplies replies={SUGGESTED_TOPICS} onSelect={handleQuickReply} />
      )}

      {/* Input Area */}
      <ChatInput
        value={inputValue}
        onChange={setInputValue}
        onSend={handleSend}
        disabled={isLoading}
      />

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-t border-red-200 px-4 py-2 text-sm text-red-700">
          {error}
        </div>
      )}
    </div>
  );
};
