import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { TbWorldSearch } from "react-icons/tb";

/**
 * Component for rendering the search input area and search button.
 *
 * @component
 * @param {Object} props - Component props
 * @param {string} props.inputValue - Current value of the search input
 * @param {Function} props.setInputValue - Function to update the input value
 * @param {Function} props.handleSearch - Callback to trigger the search operation
 * @param {boolean} props.isLoadingResponse - Indicates if a search response is currently being fetched
 * @returns {JSX.Element} Rendered SearchBar component
 */
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
