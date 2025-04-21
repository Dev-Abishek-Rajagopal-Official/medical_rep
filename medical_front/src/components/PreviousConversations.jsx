import React from 'react';
import { Button } from 'react-bootstrap';

/**
 * Component to display a list of previous conversations as clickable buttons.
 *
 * @component
 * @param {Object} props - Component props
 * @param {Array} props.conversations - List of previous conversation objects
 * @param {boolean} props.isLoadingConversations - Loading state for conversations
 * @param {Function} props.handlePreviousQueryClick - Callback when a previous conversation is clicked
 * @returns {JSX.Element} Rendered previous conversations section
 */
const PreviousConversations = ({
  conversations,
  isLoadingConversations,
  handlePreviousQueryClick
}) => (
  <div>
    <hr />
    <h6>Previous Conversations</h6>
    {isLoadingConversations ? (
      <p>Loading...</p>
    ) : (
      <div className="previous-conversations">
        {conversations.map((conv) => (
          <Button
            key={conv.id}
            variant="outline-secondary"
            size="sm"
            className="mb-2 w-100 text-start"
            onClick={() => handlePreviousQueryClick(conv.id)}
          >
            {conv.query}
          </Button>
        ))}
      </div>
    )}
  </div>
);

export default PreviousConversations;
