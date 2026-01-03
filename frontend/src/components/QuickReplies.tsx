import React from 'react';

interface QuickReply {
  label: string;
  value: string;
}

interface QuickRepliesProps {
  replies: QuickReply[];
  onSelect: (value: string) => void;
}

export const QuickReplies: React.FC<QuickRepliesProps> = ({ replies, onSelect }) => {
  if (!replies.length) return null;

  return (
    <div className="flex flex-wrap gap-2 mb-4 px-4">
      {replies.map((reply, index) => (
        <button
          key={index}
          onClick={() => onSelect(reply.value)}
          className="px-4 py-2 bg-white border border-blue-600 text-blue-600 rounded-full hover:bg-blue-50 transition-colors text-sm"
        >
          {reply.label}
        </button>
      ))}
    </div>
  );
};
