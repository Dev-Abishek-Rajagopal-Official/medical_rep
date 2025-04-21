import React from 'react';
import ReactMarkdown from 'react-markdown';

const StreamedContent = ({ streamedContent }) => (
  <div>
    <ReactMarkdown>{streamedContent}</ReactMarkdown>
  </div>
);

export default StreamedContent;
