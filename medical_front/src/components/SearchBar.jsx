import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { TbWorldSearch } from "react-icons/tb";

const SearchBar = ({ inputValue, setInputValue, handleSearch, isLoadingResponse }) => (
  <div>
    <h5>AI-Medi Search <TbWorldSearch /></h5>
    <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
      <Form.Control
        as="textarea"
        rows={3}
        className='border-1 field-border'
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
    </Form.Group>
    <Button variant="primary" onClick={handleSearch}>Search</Button>
    {isLoadingResponse && (
      <>
        <hr />
        <p className="text-muted mb-2">Fetching results...</p>
      </>
    )}
  </div>
);

export default SearchBar;
