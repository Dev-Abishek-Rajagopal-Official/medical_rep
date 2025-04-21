export const fetchConversations = async () => {
    try {
      const response = await fetch('http://localhost:8000/conversations/');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };
  
  export const fetchConversationById = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/conversations/${id}`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching conversation:', error);
    }
  };
  