import React from 'react';

/**
 * Displays a list of tools that were used in the current process.
 *
 * @component
 * @param {Object} props - Component props.
 * @param {Array<string>} props.toolsUsed - List of tools that were used.
 * @returns {JSX.Element} A list of tools used, displayed only if the list is not empty.
 */
const ToolsUsed = ({ toolsUsed }) => (
  <>
    {toolsUsed.length > 0 && (
      <>
        <hr />
        <h6>Tools Used</h6>
        <ul className="mb-2">
          {toolsUsed.map((tool, index) => (
            <li key={index}>{tool}</li>
          ))}
        </ul>
      </>
    )}
  </>
);

export default ToolsUsed;
