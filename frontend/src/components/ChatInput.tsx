import React from 'react';

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  disabled?: boolean;
  placeholder?: string;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  value,
  onChange,
  onSend,
  disabled = false,
  placeholder = 'Type your message...',
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !disabled) {
        onSend();
      }
    }
  };

  return (
    <div className="border-t bg-white p-4">
      <div className="text-xs text-gray-500 mb-2">
        Do not share passwords or payment card numbers.
      </div>
      <div className="flex gap-2 items-end">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          className="flex-1 resize-none border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 max-h-32"
          rows={1}
          style={{
            minHeight: '44px',
            maxHeight: '128px',
          }}
          aria-label="Message input"
        />
        <button
          onClick={onSend}
          disabled={!value.trim() || disabled}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors h-11"
          aria-label="Send message"
        >
          Send
        </button>
      </div>
      <div className="mt-2">
        <button
          onClick={() => onChange('agent')}
          className="text-sm text-blue-600 hover:text-blue-700 underline"
        >
          Talk to a person
        </button>
      </div>
    </div>
  );
};
