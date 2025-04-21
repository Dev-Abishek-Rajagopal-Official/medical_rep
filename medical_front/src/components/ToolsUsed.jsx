import React from 'react';

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
