import React, { useEffect, useRef, useState } from 'react';
import './App.css';
import { Card, Container, Row, Col } from 'react-bootstrap';
import { fetchConversations, fetchConversationById } from './api/conversationAPI.jsx';
import SearchBar from './components/SearchBar.jsx';
import ToolsUsed from './components/ToolsUsed.jsx';
import PreviousConversations from './components/PreviousConversations.jsx';
import StreamedContent from './components/StreamedContent.jsx';
import ChartSection from './components/ChartSection.jsx';
import TimelineSection from './components/TimelineSection.jsx';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [streamedContent, setStreamedContent] = useState('');
  const [jsonData, setJsonData] = useState(null);
  const [arrayData, setArrayData] = useState(null);
  const socketRef = useRef(null);
  const [conversations, setConversations] = useState([]);
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);
  const [toolsUsed, setToolsUsed] = useState([]);
  const [isLoadingResponse, setIsLoadingResponse] = useState(false);

  useEffect(() => {
    socketRef.current = new WebSocket('ws://localhost:8000/ws/agent/');
    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.combined_text) {
        setStreamedContent(data.combined_text.content);
        setJsonData(data.combined_text.json_data_response);
        setArrayData(data.combined_text.array_data_response);
        setToolsUsed(data.combined_text.tools_used || []);
      }
      if (data.done) setIsLoadingResponse(false);
    };

    socketRef.current.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => socketRef.current.close();
  }, []);

  useEffect(() => {
    fetchConversationsList();
  }, []);

  const fetchConversationsList = async () => {
    setIsLoadingConversations(true);
    const data = await fetchConversations();
    setConversations(data);
    setIsLoadingConversations(false);
  };

  const handlePreviousQueryClick = async (id) => {
    const data = await fetchConversationById(id);
    setInputValue(data.query);
    setStreamedContent(data.response);
    setJsonData(data.json_data);
    setArrayData(data.array_data);
    setToolsUsed(data.tools_used);
  };

  const handleSearch = async () => {
    setStreamedContent('');
    setJsonData(null);
    setArrayData(null);
    setToolsUsed([]);
    setIsLoadingResponse(true);
    fetchConversationsList();
    const payload = { search_str: inputValue };
    socketRef.current.send(JSON.stringify(payload));
  };

  return (
    <Container fluid className="p-0 fullscreen-container">
      <Card className="h-100 w-100 border-2">
        <Card.Body>
          <Row className="h-100">
            <Col xs={12} md={3}>
              <Card className="h-100 border-1">
                <Card.Body>
                  <SearchBar 
                    inputValue={inputValue} 
                    setInputValue={setInputValue} 
                    handleSearch={handleSearch} 
                    isLoadingResponse={isLoadingResponse} 
                  />
                  <ToolsUsed toolsUsed={toolsUsed} />
                  <PreviousConversations 
                    conversations={conversations} 
                    isLoadingConversations={isLoadingConversations} 
                    handlePreviousQueryClick={handlePreviousQueryClick} 
                  />
                </Card.Body>
              </Card>
            </Col>
            <Col xs={12} md={9}>
              <Card className="h-100 border-1">
                <Card.Body>
                  <StreamedContent streamedContent={streamedContent} />
                  <ChartSection jsonData={jsonData} />
                  <TimelineSection arrayData={arrayData} />
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </Container>
  );
}

export default App;
