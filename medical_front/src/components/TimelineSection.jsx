import React from 'react';
import TimelineChart from './TimelineChart.jsx';

/**
 * Renders a section containing a timeline chart.
 *
 * @component
 * @param {Object} props - Component props.
 * @param {Array<Object>} props.arrayData - Array of data points for the timeline chart.
 * @returns {JSX.Element} A section containing the TimelineChart component if data is provided.
 */
const TimelineSection = ({ arrayData }) => (
  <div>
    {arrayData && <TimelineChart arrayData={arrayData} />}
  </div>
);

export default TimelineSection;
