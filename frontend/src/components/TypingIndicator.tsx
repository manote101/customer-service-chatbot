import React from 'react';

interface TypingIndicatorProps {
  show: boolean;
}

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ show }) => {
  if (!show) return null;

  return (
    <div className="flex justify-start mb-4">
      <div className="bg-gray-200 px-4 py-3 rounded-2xl rounded-bl-sm">
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
};
