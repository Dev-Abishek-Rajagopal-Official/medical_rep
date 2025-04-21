import React from 'react';
import ReactMarkdown from 'react-markdown';

/**
 * Component for displaying streamed content in Markdown format.
 *
 * @component
 * @param {Object} props - Component props
 * @param {string} props.streamedContent - Markdown-formatted string to display
 * @returns {JSX.Element} Rendered StreamedContent component
 */
const StreamedContent = ({ streamedContent }) => (
  <div>
    <ReactMarkdown>{streamedContent}</ReactMarkdown>
  </div>
);

export default StreamedContent;
