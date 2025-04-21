import React from 'react';
import { Button } from 'react-bootstrap';

const PreviousConversations = ({ conversations, isLoadingConversations, handlePreviousQueryClick }) => (
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
