import React, { useEffect, useRef, useState } from 'react';
import './App.css';
import { Card, Container, Row, Col, Form, Button } from 'react-bootstrap';
import { fetchConversations, fetchConversationById } from './api/conversationAPI.jsx';
import SearchBar from './components/SearchBar.jsx';
import ToolsUsed from './components/ToolsUsed.jsx';
import PreviousConversations from './components/PreviousConversations.jsx';
import StreamedContent from './components/StreamedContent.jsx';
import ChartSection from './components/ChartSection.jsx';
import TimelineSection from './components/TimelineSection.jsx';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [streamedContent, setStreamedContent] = useState('');
  const [jsonData, setJsonData] = useState(null);
  const [arrayData, setArrayData] = useState(null);
  const socketRef = useRef(null);
  const [conversations, setConversations] = useState([]);
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);
  const [toolsUsed, setToolsUsed] = useState([]);
  const [isLoadingResponse, setIsLoadingResponse] = useState(false);

  /**
   * Initializes WebSocket and fetches conversation list when user logs in.
   */
  useEffect(() => {
    if (isLoggedIn) {
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

      fetchConversationsList();

      return () => {
        if (socketRef.current) {
          socketRef.current.close();
        }
      };
    }
  }, [isLoggedIn]);

  /**
   * Fetches all conversations from the server and updates the state.
   */
  const fetchConversationsList = async () => {
    setIsLoadingConversations(true);
    const data = await fetchConversations();
    setConversations(data);
    setIsLoadingConversations(false);
  };

  /**
   * Handles click on a previous query to load its conversation data.
   * @param {string} id - ID of the previous conversation to fetch.
   */
  const handlePreviousQueryClick = async (id) => {
    const data = await fetchConversationById(id);
    setInputValue(data.query);
    setStreamedContent(data.response);
    setJsonData(data.json_data);
    setArrayData(data.array_data);
    setToolsUsed(data.tools_used);
  };

  /**
   * Sends search input to the WebSocket and resets relevant states.
   */
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

  /**
   * Handles login validation.
   */
  const handleLogin = () => {
    if (userId === 'user' && password === 'password') {
      setIsLoggedIn(true);
    } else {
      alert('Invalid credentials');
    }
  };

  if (!isLoggedIn) {
    return (
      <Container fluid className="p-0 fullscreen-container d-flex justify-content-center align-items-center">
        <Card className="p-4 w-50">
          <Card.Body>
            <h3 className="mb-4 text-center">Login</h3>
            <Form>
              <Form.Group controlId="formUserId" className="mb-3">
                <Form.Label>User ID</Form.Label>
                <Form.Control
                  type="text"
                  value={userId}
                  onChange={(e) => setUserId(e.target.value)}
                  placeholder="Enter user ID"
                />
              </Form.Group>
              <Form.Group controlId="formPassword" className="mb-4">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                />
              </Form.Group>
              <div className="d-grid">
                <Button variant="primary" onClick={handleLogin}>
                  Login
                </Button>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </Container>
    );
  }

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
                  <Row className="h-100">
                    {
                      jsonData == null && arrayData == null ?
                        (<Col xs={12} md={12}>
                          <StreamedContent streamedContent={streamedContent} />
                        </Col>) : (<>
                          <Col xs={12} md={7}>
                            <StreamedContent streamedContent={streamedContent} />
                          </Col>
                          <Col xs={12} md={5}>
                            <ChartSection jsonData={jsonData} />
                            <TimelineSection arrayData={arrayData} />
                          </Col>
                        </>)
                    }
                  </Row>
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
