import React from 'react';
import TimelineChart from './TimelineChart.jsx';

const TimelineSection = ({ arrayData }) => (
  <div>
    {arrayData && <TimelineChart arrayData={arrayData} />}
  </div>
);

export default TimelineSection;
